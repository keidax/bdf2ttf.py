from helpers import utils

def test_default_version(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 10
        FONT_DESCENT 2
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)

    utils.assert_font_names(font, {
        5: "Version 1.000"
    })

    head = font["head"]
    assert head.fontRevision == 1.0


def test_version_less_than_one(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FONT_VERSION "0.123"
        FONT_ASCENT 10
        FONT_DESCENT 2
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)

    utils.assert_font_names(font, {
        5: "Version 0.123"
    })

    head = font["head"]
    assert round(head.fontRevision, ndigits=3) == 0.123


def test_version_greater_than_one(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FONT_VERSION "987.654"
        FONT_ASCENT 10
        FONT_DESCENT 2
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)

    utils.assert_font_names(font, {
        5: "Version 987.654"
    })

    head = font["head"]
    assert round(head.fontRevision, ndigits=3) == 987.654


def test_invalid_version(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FONT_VERSION "asdfasdf"
        FONT_ASCENT 10
        FONT_DESCENT 2
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)

    utils.assert_font_names(font, {
        5: "Version 1.000"
    })

    head = font["head"]
    assert head.fontRevision == 1.0
