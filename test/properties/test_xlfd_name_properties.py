from helpers import utils

def test_xlfd_properties_are_not_shadowed_by_face_name(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        FONT --Family-Bold-I-Expanded-Fancy-----C---
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

    utils.assert_font_names(font, {
        1: "Family Expanded Fancy",
        2: "Bold Italic",
        4: "Asdf Mono"
    })

    post = font["post"]
    assert post.isFixedPitch == 1
