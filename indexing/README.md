# Rules Paralegal Indexing App

Before we can start implement a RAG system for querying rules, we need to build our nice index of rules to retrieve _from_.  This is a small, self-contained application that parses the 5e SRD [available from Wizards of the Coast](https://dnd.wizards.com/resources/systems-reference-document).  It's specifically meant to parse the Creative Commons version of the PDF - the OGL version hasn't been tested, so YMMV.

It uses Langchain `Document`s to represent sections of the rules extracted from the PDF, organized with metadata for Chapter, Section, SubSection, Sub-_Sub_-Section, and page number.  Embeddings are generated for these documents that are then stored in a Chroma DB that you specify.

## Pre-requisites
1. Make sure to download the [5.1 SRD CC PDF](https://media.wizards.com/2023/downloads/dnd/SRD_CC_v5.1.pdf).
1. Hit [OpenAI's platform](https://platform.openai.com/api-keys) and get an API key that can generate embeddings.
1. Store the OpenAI API Key in a `.env` file with `OPENAI_API_KEY=...` as the only entry.


## Running the application
You'll need [Poetry](https://python-poetry.org/docs/) to install the dependencies of this sub-project.

```bash
poetry shell
poetry install
```

Once those are installed, you can run the application with something like this: (make sure you're in your Poetry virtual env)

```bash
python3 index_5e_srd.py --srd-pdf=./data/SRD_CC_v5.1.pdf --output=./output_dir_for_chromadb --env .env
```

Assuming all goes well, it should write a DB of the embeddings to the file system!  These can be used to enable RAG-based queries


### But how much will it cost???
With the settings in this code, as of February 2024, it was _pennies_ against OpenAI's APIs to generate all of the embeddings.  Over several test runs to generate full embeddings, it was less than $0.10 USD.