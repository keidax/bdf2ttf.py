from helpers import utils

def test_copyright(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        COPYRIGHT "Copyright (c) 1999 nobody"
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
        0: "Copyright (c) 1999 nobody"
    })

def test_notice(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --------------
        SIZE 12 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 3
        NOTICE "what even is a trademark"
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
        7: "what even is a trademark"
    })
