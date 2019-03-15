import argparse

from .convert import convert_bdf

def main():
    parser = argparse.ArgumentParser(description="Convert bitmap fonts into TTF format")
    parser.add_argument("infile", type=argparse.FileType("rb"), help="""
            The bitmap font to convert. Must be either a BDF font file, or an
            SFD file containing a bitmap font.
            """)
    parser.add_argument("-o", "--out", help="""
            The TTF font file to output. If not specified, will be generated
            based on the font name and weight.
            """)
    parser.add_argument("-f", "--feature-file", type=argparse.FileType("rb"), help="""
            Include feature information from an Adobe feature file in the final
            font.
            """)

    args = parser.parse_args()
    convert_bdf(args.infile, outfile=args.out, feature_file=args.feature_file)
