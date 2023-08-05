# -*- coding: utf-8 -*-
"""zest.releaser plugin to build JavaScript projects"""
from zest.releaser.utils import ask
from os.path import join
import logging
import os
import subprocess
import sys


LOGGER = logging.getLogger('yarn.build')


def find_package_json(path):
    """Find a ``packages.json`` file and run yarn on it"""
    for filename in os.listdir(path):
        dir_path = join(path, filename)
        if filename == 'packages.json':
            LOGGER.info('yarn: packages.json found!')
            build(dir_path)
        elif os.path.isdir(dir_path):
            find_package_json(dir_path)


def build(path):
    """Build the JavaScript project at the given location"""
    LOGGER.debug('yarn: Compile dependencies')
    subprocess.call(['yarn', ], cwd=path)
    LOGGER.debug('yarn: Build the project')
    subprocess.call(['yarn', 'run', 'release', ], cwd=path)


def build_project(data):
    """Build a JavaScript project from a zest.releaser tag directory"""
    tagdir = data.get('tagdir')
    if not tagdir:
        msg = 'yarn: Aborted building with yarn: no tagdir found in data.'
        LOGGER.warn(msg)
        return
    LOGGER.debug('yarn: Find and build JavaScript projects {0}'.format(tagdir))
    try:
        find_package_json(tagdir)
    except Exception:
        LOGGER.warn(
            'yarn: Building with a project with yarn failed.',
            exc_info=True,
        )
        if data:
            # We were called as an entry point of zest.releaser.
            if not ask('Error building project. Do you want to continue?'):
                sys.exit(1)
