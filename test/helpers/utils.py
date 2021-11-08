# Assert that font contains name entries matching the given mappings.
# Platform, language, etc. are not considered.
#
# For more information on name IDs:
# https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids
def assert_font_names(font, name_mapping):
    for name_id, expected_value in name_mapping.items():
        name_value = font["name"].getDebugName(name_id)
        assert name_value == expected_value, f"wrong value for name entry {name_id}"


def assert_font_weight(font, expected_weight_value):
    weight_value = font["OS/2"].usWeightClass
    assert weight_value == expected_weight_value


def assert_font_style(font, bold, italic, regular):
    mac_style = font["head"].macStyle
    fs_selection = font["OS/2"].fsSelection

    bold_bit = 1 if bold else 0
    italic_bit = 1 if italic else 0
    regular_bit = 1 if regular else 0

    assert get_bit(mac_style, bit=0) == bold_bit
    assert get_bit(fs_selection, bit=5) == bold_bit

    assert get_bit(mac_style, bit=1) == italic_bit
    assert get_bit(fs_selection, bit=0) == italic_bit

    assert get_bit(fs_selection, bit=6) == regular_bit


def get_bit(number, bit):
    return (number & (1 << bit)) >> bit
