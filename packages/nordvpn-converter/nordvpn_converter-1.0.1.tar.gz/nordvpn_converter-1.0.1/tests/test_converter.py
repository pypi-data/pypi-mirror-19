#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test converter.py
PYTHONPATH=. py.test tests/
"""
import pytest
import uuid

from nordvpn_converter.converter import Converter


@pytest.fixture
def a_converter():
    return Converter()


def test_initialization():
    ob = Converter(True)
    assert ob.debug_mode is True

    ob = Converter(debug_mode=False)
    assert ob.debug_mode is False


def test_set_source_folder_not_valid(a_converter):
    with pytest.raises(Exception):
        a_converter.set_source_folder('/tmp/some_invalid_path')


def test_set_source_folder_valid(a_converter, tmpdir):
    source_folder = tmpdir.mkdir("source")
    a_converter.set_source_folder(str(source_folder))

    assert str(source_folder) is a_converter._source_folder


def test_set_destination_folder_should_be_created(a_converter):
    # DO NOT use the below approach due to a bug in os.makedirs
    # https://bugs.python.org/issue13498
    # tmp_folder = tempfile.mkdtemp()
    tmp_folder = str(uuid.uuid4())
    a_converter.set_destination_folder(tmp_folder)

    assert tmp_folder == a_converter._destination_folder


def test_set_certs_folder_not_valid(a_converter):
    with pytest.raises(Exception):
        a_converter.set_certs_folder('/tmp/some_invalid_path')


def test_pprint_system_msg(a_converter, capsys):
    sys_msg = "This is a system message"

    a_converter.pprint(sys_msg, appmsg=True)
    out, err = capsys.readouterr()

    out = out.rstrip()
    assert out == sys_msg


def test_pprint_debug_msg_false(a_converter, capsys):
    debug_msg = "This is a debug message"

    a_converter.pprint(debug_msg, appmsg=False)
    out, err = capsys.readouterr()

    out = out.rstrip()
    assert a_converter.debug_mode is False
    assert out == ''


def test_pprint_debug_msg_true(a_converter, capsys):
    debug_msg = "This is a debug message"

    a_converter.debug_mode = True
    a_converter.pprint(debug_msg, appmsg=False)
    out, err = capsys.readouterr()

    out = out.rstrip()
    assert a_converter.debug_mode is True
    assert out == debug_msg


def test_extract_information(a_converter):
    """here maybe use a fixture to test the whole extract_information?"""
    pass



