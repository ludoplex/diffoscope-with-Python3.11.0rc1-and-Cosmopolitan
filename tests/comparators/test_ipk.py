#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# debbindiff: highlight differences between two builds of Debian packages
#
# Copyright © 2015 Jérémy Bobbio <lunar@debian.org>
#
# debbindiff is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# debbindiff is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with debbindiff.  If not, see <http://www.gnu.org/licenses/>.

import codecs
import os.path
import shutil
import pytest
from debbindiff.comparators import specialize
from debbindiff.comparators.binary import FilesystemFile
from debbindiff.comparators.ipk import IpkFile

TEST_FILE1_PATH = os.path.join(os.path.dirname(__file__), '../data/base-files_157-r45695_ar71xx.ipk')
TEST_FILE2_PATH = os.path.join(os.path.dirname(__file__), '../data/base-files_157-r45918_ar71xx.ipk')

@pytest.fixture
def ipk1():
    return specialize(FilesystemFile(TEST_FILE1_PATH))

@pytest.fixture
def ipk2():
    return specialize(FilesystemFile(TEST_FILE2_PATH))

def test_identification(ipk1):
    assert isinstance(ipk1, IpkFile)

def test_no_differences(ipk1):
    difference = ipk1.compare(ipk1)
    assert difference is None

@pytest.fixture
def differences(ipk1, ipk2):
    return ipk1.compare(ipk2).details

def test_metadata(differences):
    assert differences[0].source1 == 'metadata'
    expected_diff = open(os.path.join(os.path.dirname(__file__), '../data/ipk_metadata_expected_diff')).read()
    assert differences[0].unified_diff == expected_diff

def test_compressed_files(differences):
    assert differences[1].details[1].source1 == './control.tar.gz'
    assert differences[1].details[2].source1 == './data.tar.gz'