from helpers import utils

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

    # First 3 glyphs are defaulted by FontForge
    assert font.getGlyphOrder() == [".notdef", ".null", "nonmarkingreturn", "bar"]

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

    # First 3 glyphs are defaulted by FontForge
    assert font.getGlyphOrder() == [".notdef", ".null", "nonmarkingreturn", "a", "a.alt"]

    # Unencoded glyphs don't have codepoints
    name_to_codepoints = font["cmap"].buildReversed()
    assert name_to_codepoints == {'a': {97}}

    # but they do exist
    glyphs = font.getGlyphSet()
    assert glyphs["a"]
    assert glyphs["a.alt"]
