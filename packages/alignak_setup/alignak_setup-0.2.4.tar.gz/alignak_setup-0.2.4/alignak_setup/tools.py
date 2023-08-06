#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2016: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak project.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak Backend Import.  If not, see <http://www.gnu.org/licenses/>.

"""
alignak_setup utility functions for building setup
"""
from __future__ import print_function
import os
import re
import sys
from datetime import datetime
import fileinput

def get_alignak_cfg():
    """
        Search for an */usr/local/etc/default/alignak* or *etc/default/alignak* file
        and parse its content to find out Alignak main paths

        Returns a dict with the found elements and their respective value
    """
    alignak_cfg = {
        'ALIGNAKETC': '/usr/local/etc/alignak',
        'ALIGNAKVAR': '/usr/local/var/lib/alignak',
        'ALIGNAKBIN': '/usr/local/bin',
        'ALIGNAKRUN': '/usr/local/var/run/alignak',
        'ALIGNAKLOG': '/usr/local/var/log/alignak',
        'ALIGNAKLIB': '/usr/local/var/libexec/alignak',
        'ALIGNAKUSER': 'alignak',
        'ALIGNAKGROUP': 'alignak'
    }

    # Search Alignak main configuration file
    alignak_etc_default = "/"
    if os.path.isfile("/usr/local/etc/default/alignak"):
        alignak_etc_default = "/usr/local/etc/default/alignak"
    elif os.path.isfile("/etc/default/alignak"):
        alignak_etc_default = "/etc/default/alignak"
    else:
        print("Alignak 'default/alignak' file not found. "
              "You host is probably A BSD or DragonFly Unix system, else "
              "Alignak is not installed on this host!\n"
              "Assuming Unix standard file structure based on /usr/local")
        return alignak_cfg

    # Parse Alignak configuration file
    with open(alignak_etc_default, "r") as etc_file:
        for line in etc_file:
            line = line.strip()

            if line.startswith('ETC'):
                alignak_cfg['ALIGNAKETC'] = line.split('=')[1]
            elif line.startswith('VAR'):
                alignak_cfg['ALIGNAKVAR'] = line.split('=')[1]
            elif line.startswith('BIN'):
                alignak_cfg['ALIGNAKBIN'] = line.split('=')[1]
            elif line.startswith('RUN'):
                alignak_cfg['ALIGNAKRUN'] = line.split('=')[1]
            elif line.startswith('LOG'):
                alignak_cfg['ALIGNAKLOG'] = line.split('=')[1]
            elif line.startswith('LIB'):
                alignak_cfg['ALIGNAKLIB'] = line.split('=')[1]
            elif line.startswith('ALIGNAKUSER'):
                alignak_cfg['ALIGNAKUSER'] = line.split('=')[1]
            elif line.startswith('ALIGNAKGROUP'):
                alignak_cfg['ALIGNAKGROUP'] = line.split('=')[1]
        etc_file.close()

    # Check Alignak configuration directory
    if not os.path.exists(alignak_cfg['ALIGNAKETC']):
        print("Alignak configuration directory (%s) not found: "
              "does not seem to be installed on this host!" % alignak_cfg['ALIGNAKETC'])
        return None

    # Check Alignak plugins directory
    if not os.path.exists(alignak_cfg['ALIGNAKLIB']):
        print("Alignak plugins directory (%s) not found: "
              "does not seem to be installed on this host!" % alignak_cfg['ALIGNAKLIB'])
        return None

    print("Alignak config: ")
    for path in alignak_cfg:
        print(" %s = %s" % (path, alignak_cfg[path]))

    return alignak_cfg


def get_files(alignak_cfg, package_name, package_type, module=False):
    """
    Get the list of files to be installed:
     - data_files for setup.py
     -files to be installed
     -files to be parsed after installation
    :param alignak_cfg: alignak directories as returned by get_alignak_cfg function
    :param package_name: the package name (eg directory) where to search for files
    :param package_type: the package short name (eg. wmi)
    :param module: set this to True if the installation if for a module
    :return:
    """
    # Define installation paths
    # Get Alignak configuration packs directory
    alignak_cfg_path = os.path.join(alignak_cfg['ALIGNAKETC'], 'arbiter', 'packs', package_type)

    # Build list of all installable package files
    data_files = []
    to_be_parsed_files = []
    to_be_installed_files = []
    for subdir, dirs, files in os.walk(package_name):
        for file in files:
            # Ignore files which name starts with __
            if file.startswith('__'):
                continue

            # Files in plugins directory will be installed in the plugins directory of Alignak
            if subdir and 'plugins' in subdir:
                data_files.append(
                    (
                        os.path.join(
                            alignak_cfg['ALIGNAKLIB'],
                            re.sub(
                                r"^(%s\/|%s$)" % (
                                    os.path.join(package_name, 'plugins'),
                                    os.path.join(package_name, 'plugins')
                                ),
                                "",
                                subdir
                            )),
                        [os.path.join(subdir, file)]
                    )
                )
                to_be_installed_files.append(
                    (os.path.join(
                        alignak_cfg['ALIGNAKLIB'],
                        re.sub(
                            r"^(%s\/|%s$)" % (
                                os.path.join(package_name, 'plugins'),
                                os.path.join(package_name, 'plugins')
                            ),
                            "",
                            subdir
                        )
                    ),
                     file)
                )
                if file.endswith(".parse"):
                    to_be_parsed_files.append(
                        (os.path.join(
                            alignak_cfg['ALIGNAKLIB'],
                            re.sub(
                                r"^(%s\/|%s$)" % (
                                    os.path.join(package_name, 'plugins'),
                                    os.path.join(package_name, 'plugins')
                                ),
                                "",
                                subdir
                            )
                        ),
                         file)
                    )

            # Files in ALIGNAKETC directory will be installed
            # in the configuration directory of Alignak (etc/alignak)
            elif subdir and 'ALIGNAKETC' in subdir:
                data_files.append(
                    (os.path.join(
                        alignak_cfg['ALIGNAKETC'],
                        re.sub(
                            r"^(%s\/|%s$)" % (
                                os.path.join(package_name, 'ALIGNAKETC'),
                                os.path.join(package_name, 'ALIGNAKETC')
                            ),
                            "",
                            subdir
                        )
                    ),
                     [os.path.join(subdir, file)])
                )
                to_be_installed_files.append(
                    (os.path.join(
                        alignak_cfg['ALIGNAKETC'],
                        re.sub(
                            r"^(%s\/|%s$)" % (
                                os.path.join(package_name, 'ALIGNAKETC'),
                                os.path.join(package_name, 'ALIGNAKETC')
                            ),
                            "",
                            subdir
                        )
                    ),
                     file)
                )
                to_be_parsed_files.append(
                    (os.path.join(
                        alignak_cfg['ALIGNAKETC'],
                        re.sub(
                            r"^(%s\/|%s$)" % (
                                os.path.join(package_name, 'ALIGNAKETC'),
                                os.path.join(package_name, 'ALIGNAKETC')
                            ),
                            "",
                            subdir
                        )
                    ),
                     file)
                )
            # Other files will be installed in the pack created directory (etc/alignak/packs/ME)
            # in the configuration directory of Alignak
            else:
                if not module:
                    data_files.append(
                        (
                            os.path.join(
                                alignak_cfg_path,
                                re.sub(r"^(%s\/|%s$)" % (
                                package_name, package_name), "", subdir)
                            ),
                            [os.path.join(subdir, file)]
                        )
                    )
                    to_be_installed_files.append(
                        (
                            os.path.join(
                                alignak_cfg_path,
                                re.sub(r"^(%s\/|%s$)" % (
                                package_name, package_name), "", subdir)
                            ),
                            file
                        )
                    )
                    if file.endswith(".parse"):
                        to_be_parsed_files.append(
                            (
                                os.path.join(
                                    alignak_cfg_path,
                                    re.sub(r"^(%s\/|%s$)" % (
                                    package_name, package_name), "", subdir)
                                ),
                                file
                            )
                        )

    # to_be_installed_files contains tuples for the installed files
    if to_be_installed_files:
        print("Installable data files: ")
        for dir, file in to_be_installed_files:
            print(" %s = %s" % (dir, file))

    # to_be_parsed_files contains tuples for files to be parsed (directory, file)
    if to_be_parsed_files:
        print("Parsable files: ")
        for dir, file in to_be_parsed_files:
            print(" %s = %s" % (dir, file))

    return (data_files, to_be_parsed_files, to_be_installed_files)


def get_to_be_installed_files(data_files):
    """
    If backup is required, make a backup copy of the existing files
    According to replace required, determines the new data files list

    :param data_files: setup.py files to install
    :return: list of data files to replace
    """

    new_data_files = []
    if not data_files:
        return new_data_files

    if 'ALIGNAK_SETUP_BACKUP' in os.environ and os.environ['ALIGNAK_SETUP_BACKUP']:
        # Backup existing files if required
        installation_date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        print("---")
        print("Checking former existing files to backup...")
        for dir, files in data_files:
            for file in files:
                filename = os.path.join(dir, os.path.basename(os.path.abspath(file)))
                if os.path.isfile(filename):
                    bkp_file = "%s_%s%s_" % (
                        os.path.splitext(filename)[0],
                        installation_date,
                        os.path.splitext(filename)[1]
                    )
                    print(" -> backing up file: %s/%s to %s" % (dir, file, bkp_file))
                    os.rename(filename, bkp_file)
                    print(" -> backed up: %s/%s" % (dir, file))

    # Before data files installation ...
    # ... do not replace existing files
    print("---")
    print("Checking former existing files to replace...")
    for dir, files in data_files:
        for file in files:
            filename = os.path.join(dir, os.path.basename(os.path.abspath(file)))
            if filename.endswith(".parse"):
                filename = filename.replace('.parse', '')
            if not os.path.isfile(filename):
                print(" -> create: %s" % (filename))
                new_data_files.append((dir, [file]))
            else:
                if 'ALIGNAK_SETUP_REPLACE' in os.environ and \
                        os.environ['ALIGNAK_SETUP_REPLACE']:
                    print(" -> replace existing: %s" % (filename))
                    new_data_files.append((dir, [file]))
                else:
                    print(" -> ignore existing: %s" % (filename))

    if not new_data_files:
        print("---")
        print("No files to install")
        print("---")
    else:
        print("---")
        print("To be installed files:")
        for dir, files in new_data_files:
            for file in files:
                print(" - %s" % (os.path.join(dir, os.path.basename(os.path.abspath(file)))))
        print("---")

    return new_data_files


def parse_files(to_be_parsed_files, alignak_cfg):
    """
    Parse the files to replace Alignak variables patterns:
        - search each line with one of this pattern:
            ALIGNAKETC
            ALIGNAKVAR
            ALIGNAKBIN
            ALIGNAKRUN
            ALIGNAKLOG
            ALIGNAKLIB
            ALIGNAKUSER
            ALIGNAKGROUP
        - replace found pattern with the value determined for each variable
    :param to_be_parsed_files: list of files to be parsed
    :param: alignak_cfg: alignak variables for patterns
    :return:
    """
    if not to_be_parsed_files:
        return

    # Prepare pattern for alignak.cfg
    to_change = re.compile("|".join(alignak_cfg.keys()))

    print("---")
    print("Parsing files...")
    for dir, file in to_be_parsed_files:
        filename = os.path.join(dir, file)
        print(" -> parsing %s" % (filename))
        if os.path.isfile(filename):
            # Parse file
            for line in fileinput.input(filename, inplace=True):
                sys.stdout.write(to_change.sub(lambda m: alignak_cfg[re.escape(m.group(0))], line))

            # Rename .parse file
            # os.rename(os.path.join(dir, file), os.path.join(dir, file[:-6]))
            print(" -> parsed %s" % (filename))
    print("---")
