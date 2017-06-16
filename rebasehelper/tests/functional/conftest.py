# -*- coding: utf-8 -*-
#
# This tool helps you to rebase package to the latest version
# Copyright (C) 2013-2014 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# he Free Software Foundation; either version 2 of the License, or
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

import os

import pytest

from rebasehelper.settings import REBASE_HELPER_RESULTS_DIR, REBASE_HELPER_DEBUG_LOG


def pytest_collection_modifyitems(items):
    for item in items:
        if os.path.dirname(__file__) in item.fspath.strpath:
            item.add_marker(pytest.mark.functional)


def make_logs_report():
    logs = [
        REBASE_HELPER_DEBUG_LOG,
        'old/SRPM/build.log',
        'old/RPM/build.log',
        'old/RPM/root.log',
        'old/RPM/mock_output.log',
        'new/SRPM/build.log',
        'new/RPM/build.log',
        'new/RPM/root.log',
        'new/RPM/mock_output.log',
    ]
    report = []
    for log in logs:
        try:
            with open(os.path.join(REBASE_HELPER_RESULTS_DIR, log)) as f:
                content = f.read()
                report.append(' {} '.format(log).center(80, '_'))
                report.append(content)
        except IOError:
            continue
    return '\n'.join(report)


@pytest.mark.hookwrapper
def pytest_runtest_makereport():
    outcome = yield
    report = outcome.get_result()
    report.sections.append(('Logs', make_logs_report()))
