import argparse
from parsing.srd_5e import SrdParser


def main(srd_pdf, output, env):
    parser = SrdParser(srd_pdf)
    chunks = parser.chunk_srd_pdf()
    print(chunks[145])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Index the 5e SRD')
    parser.add_argument('--srd-pdf', type=str, required=True, help='The source PDF file of the 5e SRD (the CC version), avaialble here: https://dnd.wizards.com/resources/systems-reference-document')
    parser.add_argument('--output', type=str, required=True, help='The output directory for the SQLite vector store from indexing')
    parser.add_argument('--env', type=str, default='.env', help='The .env file for API keys and other sensitive information')

    args = parser.parse_args()
    srd_pdf = args.srd_pdf
    output = args.output
    env = args.env

    main(srd_pdf, output, env)