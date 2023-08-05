"""
cli module for lazy doc
"""

import argparse

def main():
    """
    Run the main function
    """
    from lazydoc.lazydoc import generate, document
    parser = argparse.ArgumentParser(description='Generate documentation - the lazy way')
    parser.add_argument('-g', '--gen', '--generate',
                        help="generate sphinx doc directories",
                        action='store_true')
    parser.add_argument('-d', '--doc', '--document',
                        help="based on sphinx config, generate all documentation",
                        action='store_true')
    args = parser.parse_args()
    print(args)

    if args.gen:
        generate()
    if args.doc:
        document()
