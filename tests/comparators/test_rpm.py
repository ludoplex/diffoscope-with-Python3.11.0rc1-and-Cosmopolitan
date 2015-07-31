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
from debbindiff.comparators.rpm import RpmFile
from conftest import tool_missing

TEST_FILE1_PATH = os.path.join(os.path.dirname(__file__), '../data/test1.rpm')
TEST_FILE2_PATH = os.path.join(os.path.dirname(__file__), '../data/test2.rpm')

@pytest.fixture
def rpm1():
    return specialize(FilesystemFile(TEST_FILE1_PATH))

@pytest.fixture
def rpm2():
    return specialize(FilesystemFile(TEST_FILE2_PATH))

def test_identification(rpm1):
    assert isinstance(rpm1, RpmFile)

def test_no_differences(rpm1):
    difference = rpm1.compare(rpm1)
    assert difference is None

@pytest.fixture
def differences(rpm1, rpm2):
    return rpm1.compare(rpm2).details

@pytest.mark.skipif(tool_missing('rpm2cpio'), reason='missing rpm2cpio')
def test_header(differences):
    assert differences[0].source1 == 'header'
    expected_diff = open(os.path.join(os.path.dirname(__file__), '../data/rpm_header_expected_diff')).read()
    assert differences[0].unified_diff == expected_diff

@pytest.mark.skipif(tool_missing('rpm2cpio'), reason='missing rpm2cpio')
def test_listing(differences):
    assert differences[1].source1 == 'content'
    assert differences[1].details[0].source1 == 'file list'
    expected_diff = open(os.path.join(os.path.dirname(__file__), '../data/rpm_listing_expected_diff')).read()
    assert differences[1].details[0].unified_diff == expected_diff

@pytest.mark.skipif(tool_missing('rpm2cpio'), reason='missing rpm2cpio')
def test_content(differences):
    assert differences[1].source1 == 'content'
    assert differences[1].details[1].source1 == './dir/text'
    expected_diff = open(os.path.join(os.path.dirname(__file__), '../data/text_ascii_expected_diff')).read()
    assert differences[1].details[1].unified_diff == expected_diff