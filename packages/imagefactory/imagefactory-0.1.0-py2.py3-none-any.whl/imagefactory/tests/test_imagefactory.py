#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests
"""
import string
import tempfile
from io import BytesIO, StringIO

import hypothesis.strategies as st
import pytest
from hypothesis import given, settings

from imagefactory import create_image

BITMAP = ('jpeg', 'png', 'gif')
SVG = ('svg',)


@settings(max_examples=10)
@given(
    name=st.text(string.ascii_letters, min_size=1, max_size=8),
    width=st.integers(min_value=1, max_value=1000),
    height=st.integers(min_value=1, max_value=1000),
    text=st.text(string.ascii_letters, min_size=1, max_size=8) or st.none(),
    choice=st.choices(),
)
def test_create_bitmap(name, width, height, text, choice):
    filetype = choice(BITMAP)
    image = create_image(name, filetype, width, height, text)
    assert isinstance(image, BytesIO)


@settings(max_examples=10)
@given(
    name=st.text(string.ascii_letters, min_size=1, max_size=8),
    width=st.integers(min_value=1, max_value=1000),
    height=st.integers(min_value=1, max_value=1000),
    text=st.text(string.ascii_letters, min_size=1, max_size=8) or st.none()
)
def test_create_svg(name, width, height, text):
    filetype = 'svg'
    image = create_image(name, filetype, width, height, text)
    assert isinstance(image, StringIO)


def test_create_bitmap_save():
    with tempfile.TemporaryDirectory() as tmpdir:
        image = create_image(filetype='png', savedir=tmpdir)
        assert isinstance(image, BytesIO)

        with pytest.raises(FileExistsError):
            create_image(filetype='png', savedir=tmpdir)


def test_create_bitmap_svg():
    with tempfile.TemporaryDirectory() as tmpdir:
        image = create_image(filetype='svg', savedir=tmpdir)
        assert isinstance(image, StringIO)

        with pytest.raises(FileExistsError):
            create_image(filetype='svg', savedir=tmpdir)
