# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

import os
import pytest

REQUIREMENTS_TXT_PATH = os.path.abspath('requirements.txt')
SETUP_PY_PATH = os.path.abspath('setup.py')


def test_ensure_oci_dependency_consistency_between_setup_py_and_requirements_txt():
    if not os.path.exists(REQUIREMENTS_TXT_PATH):
        pytest.fail('Could not find file: {}. Ensure you are running the pytest from the root of the repository.'.format(REQUIREMENTS_TXT_PATH))

    if not os.path.exists(SETUP_PY_PATH):
        pytest.fail('Could not find file: {}. Ensure you are running the pytest from the root of the repository.'.format(SETUP_PY_PATH))

    requirements_txt_oci_version = get_oci_dependency_version_from_file(REQUIREMENTS_TXT_PATH)
    setup_py_oci_version = get_oci_dependency_version_from_file(SETUP_PY_PATH)
    assert requirements_txt_oci_version == setup_py_oci_version


def get_oci_dependency_version_from_file(path):
    version = None
    with open(path, 'r') as f:
        for dep in f.readlines():
            # remove all whitespace so it doesnt break on oci == {version}
            dep = ''.join(dep.split())

            # remove possible endings in setup.py
            dep = dep.replace("',", '').replace('",', '')
            if 'oci==' in dep:
                version = dep.split('==')[1].strip()

        if not version:
            raise ValueError('Could not find oci dependency version in {path}'.format(path=path))

    return version
