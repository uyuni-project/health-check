# pylint: disable=import-error,too-few-public-methods
#
# Copyright (c) 2018 SUSE Linux Products GmbH
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
"""
Code for building packages in SUSE that need generated code not tracked in git.
"""
import os
import re

from tito.tagger import SUSETagger
from tito.common import run_command, get_latest_tagged_version


class SUSEHealthCheckTagger(SUSETagger):
    """
    Custom tito tagger to fix the version inside the Python health check module

    """

    def _update_package_metadata(self, new_version):
        old_version = get_latest_tagged_version(self.project_name)
        filename = os.path.join(
            self.git_root, "health-check/src/health_check/__init__.py"
        )
        parsed_old_version = re.findall(r"[0-9]+\.[0-9]+\.[0-9]+", old_version)[0]
        parsed_new_version = re.findall(r"[0-9]+\.[0-9]+\.[0-9]+", new_version)[0]
        run_command(
            f'sed -i "s/{parsed_old_version}/{parsed_new_version}/g" {filename}'
        )
        run_command(f"git add {filename}")
        super()._update_package_metadata(new_version)
