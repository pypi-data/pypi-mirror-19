#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from wa_kat.analyzers.language_detector import get_lang_tags


# Variables ===================================================================
TEST_TEMPLATE = """
<HTML>
<head>
    <title>HTML title</title>

    <meta name    = "DC.Language"
          content = "cs">

    <meta http-equiv="Content-language"
          content="cs">
</head>
<body>
Zde je nějaký ten obsah, který by měl být rozpoznaný jako čeština.
</body>
</HTML>
"""


# Tests =======================================================================
def test_get_lang_tags():
    lang_tags = get_lang_tags(TEST_TEMPLATE)

    assert lang_tags[0] == "cze"
    assert lang_tags[0].source == "HTML"

    assert lang_tags[1] == "cze"
    assert lang_tags[1].source == "DC"

    assert lang_tags[2] == "cze"
    assert lang_tags[2].source == "langdetect"
