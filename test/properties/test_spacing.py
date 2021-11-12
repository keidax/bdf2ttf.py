from helpers import utils

def test_default_spacing(convert_str):
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

    post = font["post"]
    assert post.isFixedPitch == 0

def test_spacing_in_font_name(convert_str):
    mono_font = convert_str("""
        STARTFONT 2.1
        FONT -----------C---
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FONT_ASCENT 10
        FONT_DESCENT 2
        FACE_NAME "Asdf Mono"
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

    post = mono_font["post"]
    assert post.isFixedPitch == 1

    propertional_font = convert_str("""
        STARTFONT 2.1
        FONT -----------p---
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FONT_ASCENT 10
        FONT_DESCENT 2
        FACE_NAME "Asdf Mono"
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

    post = propertional_font["post"]
    assert post.isFixedPitch == 0


def test_spacing_in_property(convert_str):
    p_font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FONT_ASCENT 10
        FONT_DESCENT 2
        SPACING "P"
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

    post = p_font["post"]
    assert post.isFixedPitch == 0

    m_font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FONT_ASCENT 10
        FONT_DESCENT 2
        SPACING "M"
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

    post = m_font["post"]
    assert post.isFixedPitch == 1

    c_font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        FONT_ASCENT 10
        FONT_DESCENT 2
        SPACING "c"
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

    post = c_font["post"]
    assert post.isFixedPitch == 1
