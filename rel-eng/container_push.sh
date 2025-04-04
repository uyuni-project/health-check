#!/usr/bin/bash

# SPDX-FileCopyrightText: 2025 SUSE LLC
#
# SPDX-License-Identifier: Apache-2.0

# This script is called by push-packages-to-obs
# To use it add the following to the tito.props of the package:
#
# [buildconfig]
# builder = custom.ContainerBuilder

PKG_NAME=$3

SRPM_PKG_DIR=$(dirname "$0")

if [ -f "${SRPM_PKG_DIR}/Dockerfile" ]; then
  rm ${SRPM_PKG_DIR}/${PKG_NAME}.spec
fi

