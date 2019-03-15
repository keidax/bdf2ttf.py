import argparse

def main():
    parser = argparse.ArgumentParser(description="Convert bitmap fonts into TTF format")
    parser.add_argument("infile", help="""
            The bitmap font to convert. Must be either a BDF font file, or an
            SFD file containing a bitmap font.
            """)
    parser.add_argument("outfile", help="""The TTF font file to output.""")
    parser.add_argument("-f", "--feature-file", help="""
            Include feature information from an Adobe feature file in the final
            font.
            """)

    args = parser.parse_args()
    print(args)
