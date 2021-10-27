# Assert that font contains name entries matching the given mappings.
# Platform, language, etc. are not considered.
#
# For more information on name IDs:
# https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids
def assert_font_names(font, name_mapping):
    for name_id, expected_value in name_mapping.items():
        name_value = font["name"].getDebugName(name_id)
        assert name_value == expected_value, f"wrong value for name entry {name_id}"
