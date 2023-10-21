from helpers import utils
from fontTools.pens.recordingPen import RecordingPen

def test_with_one_glyph(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 3 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 3
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR bar
        ENCODING 124
        SWIDTH 120 0
        DWIDTH 3 0
        BBX 1 3 1 0
        BITMAP
        8
        8
        8
        ENDCHAR
        ENDFONT
        """)

    assert font.getGlyphOrder() == [".notdef", "bar"]

    glyphs = font.getGlyphSet()
    bar = glyphs["bar"]
    assert bar

    name_to_codepoints = font["cmap"].buildReversed()
    assert name_to_codepoints["bar"] == {124}

def test_with_unencoded_glyphs(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 3 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 3
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 2
        STARTCHAR a
        ENCODING 97
        SWIDTH 120 0
        DWIDTH 3 0
        BBX 1 3 1 0
        BITMAP
        8
        8
        8
        ENDCHAR
        STARTCHAR a.alt
        ENCODING -1
        SWIDTH 120 0
        DWIDTH 3 0
        BBX 1 3 1 0
        BITMAP
        8
        8
        8
        ENDCHAR
        ENDFONT
        """)

    assert font.getGlyphOrder() == [".notdef", "a", "a.alt"]

    # Unencoded glyphs don't have codepoints
    name_to_codepoints = font["cmap"].buildReversed()
    assert name_to_codepoints == {'a': {97}}

    # but they do exist
    glyphs = font.getGlyphSet()
    assert glyphs["a"]
    assert glyphs["a.alt"]


def test_default_notdef_glyph(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 3 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 3
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        SWIDTH 120 0
        DWIDTH 3 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)

    assert font.getGlyphOrder() == [".notdef", "space"]

    name_to_codepoints = font["cmap"].buildReversed()
    assert name_to_codepoints == {'space': {32}}

    glyphs = font.getGlyphSet()
    notdef = glyphs[".notdef"]
    assert notdef.lsb == 0
    assert notdef.width == 1023

    pen = RecordingPen()
    notdef.draw(pen)
    assert pen.value == []


def test_default_notdef_glyph_average_width(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 6 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 4
        FONT_DESCENT 2
        ENDPROPERTIES
        CHARS 2
        STARTCHAR A
        ENCODING 65
        SWIDTH 120 0
        DWIDTH 3 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        STARTCHAR Z
        ENCODING 90
        SWIDTH 120 0
        DWIDTH 5 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)

    pixel = 170

    head = font["head"]
    assert head.unitsPerEm == pixel * 6

    glyphs = font.getGlyphSet()
    assert glyphs["A"].width == pixel * 3
    assert glyphs["Z"].width == pixel * 5
    assert glyphs[".notdef"].width == pixel * 4


def test_provided_notdef_glyph(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 5 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 4
        FONT_DESCENT 1
        ENDPROPERTIES
        CHARS 2
        STARTCHAR .notdef
        ENCODING -1
        SWIDTH 120 0
        DWIDTH 3 0
        BBX 1 3 1 0
        BITMAP
        8
        8
        8
        ENDCHAR
        STARTCHAR space
        ENCODING 32
        SWIDTH 120 0
        DWIDTH 3 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """)

    assert font.getGlyphOrder() == [".notdef", "space"]

    name_to_codepoints = font["cmap"].buildReversed()
    assert name_to_codepoints == {'space': {32}}

    head = font["head"]
    assert head.unitsPerEm == 1020
    pixel = 204

    glyphs = font.getGlyphSet()
    notdef = glyphs[".notdef"]
    assert notdef.lsb == pixel
    assert notdef.width == pixel*3

    pen = RecordingPen()
    notdef.draw(pen)
    assert pen.value == [
        ('moveTo', ((pixel, 0),)),
        ('lineTo', ((pixel, pixel*3),)),
        ('lineTo', ((pixel*2, pixel*3),)),
        ('lineTo', ((pixel*2, 0),)),
        ('closePath', ())
    ]
