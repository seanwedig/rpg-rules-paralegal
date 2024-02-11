import argparse
from parsing.srd_5e import SrdParser
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

import dotenv


def main(srd_pdf, output, env):
    dotenv.load_dotenv(env)

    parser = SrdParser(srd_pdf)
    chunks = parser.chunk_srd_pdf()

    docs = [Document(page_content=chunk.content, metadata=chunk_metadata(chunk)) for chunk in chunks]

    vectorstore = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings(), persist_directory=output)
    vectorstore.persist()

def chunk_metadata(chunk):
    return {
        "chapter": chunk.chapter if chunk.chapter is not None else '',
        "section": chunk.section if chunk.section is not None else '',
        "subsection": chunk.subsection if chunk.subsection is not None else '',
        "subsubsection": chunk.subsubsection if chunk.subsubsection is not None else '',
        "starting_page": chunk.starting_page if chunk.starting_page is not None else -1
    }



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