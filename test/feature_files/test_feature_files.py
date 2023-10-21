def test_with_empty_clig_feature_file(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 1
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 1
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """, """
        languagesystem DFLT dflt;
        languagesystem latn dflt;
        feature clig {
        } clig;
        """)

    assert font.getGlyphOrder() == [".notdef", "space"]

def test_with_clig_basic_sub_feature_file(convert_str):
    font = convert_str("""
        STARTFONT 2.1
        SIZE 1 72 72
        FONTBOUNDINGBOX 0 0 0 0
        STARTPROPERTIES 2
        FONT_ASCENT 1
        FONT_DESCENT 0
        ENDPROPERTIES
        CHARS 2
        STARTCHAR space
        ENCODING 32
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        STARTCHAR double_space
        ENCODING -1
        DWIDTH 1 0
        BBX 0 0 0 0
        BITMAP
        ENDCHAR
        ENDFONT
        """, """
        languagesystem DFLT dflt;
        languagesystem latn dflt;
        feature clig {
            lookup double_space {
              sub space space by double_space;
            } double_space;
        } clig;
        """)

    assert font.getGlyphOrder() == [".notdef", "space", "double_space"]

    gsub = font["GSUB"]

    features = gsub.table.FeatureList
    assert features.FeatureCount == 1

    featureRecord = features.FeatureRecord[0]
    assert featureRecord.FeatureTag == "clig"

    lookups = gsub.table.LookupList
    assert lookups.LookupCount == 1

    lookup = lookups.Lookup[0]
    ligature = lookup.SubTable[0].ligatures["space"][0]
    assert ligature.LigGlyph == "double_space"
    assert ligature.Component == ["space"]
