"""
Programmatically generate a feature file from declarative YAML.

Only a small subset of feature file syntax is supported. This is not a general
tool. It's meant to support the use case of contextual ligature substitution,
which involves a lot of repetition. Generated ligature lookups will be part of
the clig feature.

Expected YAML syntax::

    languages:
      - DFLT dflt
      - <more script/language pairs>
    ligatures:
      # Full syntax
      - name: <Name of ligature glyph. .liga will be appended if missing.>
        glyphs: <Space-separated list of component glyphs.>
        ignore: <Optional additional ignore rules, in full feature syntax.>
      # Simplified syntax. Substituted name will be component glyph names, joined by
      # underscores, followed by .liga.
      - <list of component glyphs>

For example, this YAML::

    languages:
    - DFLT dflt
    - latn dflt
    ligatures:
    - name: right_arrow.liga
      glyphs: equal greater
      ignore: |
        ignore sub less equal' greater;
    - equal equal equal

generates this feature file::

    languagesystem DFLT dflt;
    languagesystem latn dflt;

    feature clig {

    lookup right_arrow.liga {
    ignore sub equal equal' greater;
    ignore sub equal' greater greater;
    ignore sub less equal' greater;
    sub LIG greater' by right_arrow.liga;
    sub  equal' greater by LIG;
    } right_arrow.liga;

    lookup equal_equal_equal.liga {
    ignore sub equal equal' equal equal;
    ignore sub equal' equal equal equal;
    sub LIG LIG equal' by equal_equal_equal.liga;
    sub LIG equal' equal by LIG;
    sub  equal' equal equal by LIG;
    } equal_equal_equal.liga;

    } clig;
"""

import argparse
import sys
import yaml

def generate_languagesystems(stream, languagesystems):
    for lang_system in languagesystems:
        stream.write(b'languagesystem %b;\n' % lang_system)

# lookup is a dict with the following format:
#   b'glyphs': an iterable of glyph names, such as (a, b, c), which will be
#       replaced with a_b_c.liga
#   b'ignore': optional bytes to include in the lookup table
#   b'name': optional name override
def generate_lookup(stream, lookup):
    glyphs = lookup['glyphs']
    lookup_name = lookup['name']

    stream.write(b'\nlookup %b {\n' % lookup_name)

    # add ignores
    rest = b' '.join(glyphs[1:])
    stream.write(b'ignore sub %b %b\' %b;\n' % (glyphs[0], glyphs[0], rest))
    stream.write(b'ignore sub %b\' %b %b;\n' % (glyphs[0], rest, glyphs[-1]))

    # add extra ignores
    stream.write(lookup['ignore'])

    # add liga sub
    size = len(glyphs)
    stream.write(
        b'sub %b %b\' by %b;\n' % (ligs(size - 1), glyphs[-1], lookup_name)
    )

    # add remaining subs
    for pos in range(size - 2, -1, -1):
        rest = b' '.join(glyphs[pos + 1:])
        stream.write(
            b'sub %b %b\' %b by LIG;\n' % (ligs(pos), glyphs[pos], rest)
        )

    stream.write(b'} %b;\n' % lookup_name)

    return lookup_name

def ligs(count):
    return b' '.join([b'LIG'] * count)

# lookups is a list of lookup names, which will be included in the "clig"
# feature
def generate_feature(stream, lookups):
    stream.write(b'\nfeature clig {\n')

    for lookup in lookups:
        generate_lookup(stream, lookup)

    stream.write(b'\n} clig;\n')

def read_file(lig_file):
    languagesystems = []
    ligatures = []

    parsed = yaml.safe_load(lig_file)

    if parsed.get('languages'):
        for languagesystem in parsed['languages']:
            languagesystems.append(languagesystem.encode('ascii'))
    else:
        languagesystems.append(b'DFLT dflt')

    for ligature in parsed['ligatures']:
        if isinstance(ligature, str):
            glyphs = ligature
            ignore = ''
            name = None
        elif isinstance(ligature, dict):
            glyphs = ligature['glyphs']
            ignore = ligature.get('ignore') or ''
            name   = ligature.get('name')
        else:
            raise TypeError(
                'could not parse ligature: %s' % ligature
            )

        new_lig = {
            'glyphs': glyphs.encode('ascii').split(b' '),
            'ignore': ignore.encode('ascii'),
        }
        if name:
            name = name.encode('ascii')
        else:
            name = b'_'.join(new_lig['glyphs'])

        if not name.endswith(b'.liga'):
            name += b'.liga'

        new_lig['name'] = name

        ligatures.append(new_lig)

    return languagesystems, ligatures

def generate_feature_file(infile, outfile):
    languagesystems, ligatures = read_file(infile)
    infile.close()

    print(ligatures)
    generate_languagesystems(outfile, languagesystems)

    generate_feature(outfile, ligatures)
    outfile.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("infile", type=argparse.FileType("rb"), help="""
            The YAML file used for input.
            """)
    parser.add_argument("outfile", type=argparse.FileType("wb"), help="""
            The feature file used for output.
            """)

    args = parser.parse_args()
    generate_feature_file(args.infile, args.outfile)


if __name__ == '__main__':
    main()
