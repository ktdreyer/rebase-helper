# -*- coding: utf-8 -*-
#
# This tool helps you to rebase package to the latest version
# Copyright (C) 2013-2014 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors: Petr Hracek <phracek@redhat.com>
#          Tomas Hozza <thozza@redhat.com>

import re

from rebasehelper.versioneer import BaseVersioneer
from rebasehelper.logger import logger
from rebasehelper.helpers.download_helper import DownloadHelper


class PyPIVersioneer(BaseVersioneer):

    CATEGORIES = ['python']

    BASE_URL = 'https://pypi.org'
    API_URL = '{}/pypi'.format(BASE_URL)

    @classmethod
    def _get_version(cls, package_name):
        r = DownloadHelper.request('{}/{}/json'.format(cls.API_URL, package_name))
        if r is None or not r.ok:
            # try to strip python prefix
            package_name = re.sub(r'^python[23]?-', '', package_name)
            r = DownloadHelper.request('{}/{}/json'.format(cls.API_URL, package_name))
            if r is None or not r.ok:
                return None

        data = r.json()
        try:
            return data['info']['version']
        except KeyError:
            return None

    @classmethod
    def run(cls, package_name):
        version = cls._get_version(package_name)
        if version:
            return version
        logger.error("Failed to determine latest upstream version!\n"
                     "Check that the package exists on %s.", cls.BASE_URL)
        return None
