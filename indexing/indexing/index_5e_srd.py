import argparse
from parsing.srd_5e import SrdPdfDocumentLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import dotenv


def main(srd_pdf, output, env):
    dotenv.load_dotenv(env)

    print(f'Loading 5e SRD from {srd_pdf}...')
    parser = SrdPdfDocumentLoader(srd_pdf)
    docs = parser.load()

    print(f'Generating embeddings for {len(docs)} sections...')
    vectorstore = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings(), persist_directory=output)

    print(f'Persisting vector store to {output}...')
    vectorstore.persist()

    print('Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Index the 5e SRD')
    parser.add_argument('--srd-pdf', type=str, required=True, default='./data/SRC_CC_v5.1.pdf', help='The source PDF file of the 5e SRD (the CC version), avaialble here: https://dnd.wizards.com/resources/systems-reference-document')
    parser.add_argument('--output', type=str, default='./5e_srd_vectors', help='The output path for the SQLite vector store (default: ./5e_srd_vectors.db)')
    parser.add_argument('--env', type=str, default='.env', help='The .env file for API keys and other sensitive information (default: .env)')

    args = parser.parse_args()
    srd_pdf = args.srd_pdf
    output = args.output
    env = args.env

    main(srd_pdf, output, env)