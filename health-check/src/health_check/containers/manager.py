"""Module that contains podman-related functionality"""

from typing import List

from health_check import config
from health_check.utils import console, run_command


def podman(cmd: List[str], verbose=False, raise_exc=True) -> List:
    """
    Run a podman command

    :param cmd: the command in an array format without the initial "podman" part
    """
    return run_command(["podman"] + cmd, verbose, raise_exc)


def image_exists(image: str) -> bool:
    """
    Check if the image is present in podman images result

    :param image: the image name to check
    """
    stdout, _, _ = podman(
        ["images", "--quiet", "-f", f"reference={image}"],
        verbose=False,
        raise_exc=False,
    )
    return stdout.strip() != ""


def network_exists(network: str) -> bool:
    """
    Check if the podman network is up and running

    :param network: the network name to check
    """
    _, _, returncode = podman(
        ["network", "exists", f"{network}"], verbose=False, raise_exc=False
    )
    return returncode == 0


def stop_containers(verbose=False):
    """
    Stop and remove the containers we spawned on the server now
    that everything is finished

    :param verbose: increase verbosity
    """
    with console.status(status=None):
        console.log("[bold]Removing application containers")
        network = config.load_prop("podman.network_name")

        if network_exists(network):
            podman(
                [
                    "network",
                    "rm",
                    "-f",
                    "--time",
                    "0",
                    network,
                ],
                verbose,
            )
            console.log("[green]Containers have been removed")


def clean_containers_images(verbose=False):
    """
    Remove all the containers images

    :param verbose: increase verbosity
    """
    with console.status(status=None):
        console.log("[bold]Removing all container images")
        for image in config.get_all_container_image_names():
            if image_exists(image):
                podman(
                    [
                        "rmi",
                        image,
                    ],
                    verbose,
                )
                console.log(f"[green]Image {image} has been removed")


def create_podman_network(verbose=False):
    """
    Create health-check pod where we run the containers

    :param verbose: increase verbosity
    """
    console.log("[bold]Creating podman network")

    network = config.load_prop("podman.network_name")
    if network_exists(network):
        console.log(f"[yellow]Skipped; {network} already exists")
    else:
        podman(
            [
                "network",
                "create",
                network,
            ],
            verbose,
        )


def container_is_running(name: str) -> bool:
    """
    Check if a container with a given name is running in podman

    :param name: the container name to check
    """
    stdout, _, _ = podman(["ps", "--quiet", "-f", f"name={name}"])
    return stdout != ""
