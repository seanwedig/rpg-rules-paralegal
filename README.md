# rpg-rules-paralegal
The RPG Rules Paralegal - the chat assistant for all you D&D rules lawyers

This is a demonstration of using Retrieval-Augmented Generation to work with an LLM.

# Repo Structure
This repo is broken into a few submodules:

* [investigations](./investigations) - notebooks and scripts for experimenting or investigating things like PDF structure
* [indexing](./indexing) - indexing scripts for building vector databases of RPG rules content; necessary to build a local DB first in order to run the chatbot
* [rules_paralegal](./rules_paralegal) - the chatbot itself

# Discussion
## What's RAG?
RAG is a means of providing additional context during prompting based on a knowledge-base of some sort.  While the user of the system may only be presented with a basic chat prompt, a system using RAG actually provides a more complex, context-rich prompt to the LLM itself.  Using contextual information about the user and their raw prompt, relevant information is retrieved from whatever document store is appropriate.  The relevant information is then supplied alongside the user's prompt to produce a richer, more accurate prompt.

Since LLMs are themselves rich, statistical models - the presence of specific, retrieved information contained in the prompt tends to lead to referncing that information in the response.  As a result, the users are more likely to receive relevant, specific information in the reponse that _they_ see.

For something such as RPG rules where the precise wording matters, this can significantly help reduce hallucinations and incorrect responses.

## How is RAG applied for the RPG Rules Paralegal?

In this system, we're taking the 5th Edition Dungeons & Dragons SRD rules, breaking down the PDF into a series of sections, and using them as our context database.  The context documents have metadata that make them _citable_, so that as documents are referenced, the information referenced can be supplied back to the user... because most of the time, us nerds will want to look it up ourselves anyway. 😉 

# Acknowledgments
Much of the inspiration and an early prototype of this project came from https://github.com/Tublian/langchain-rag-template/blob/codemash, and the accompanying talk at CodeMash 2024: _Building Applications on Top of Large Language Models (LLMs)_ by Nilanjan Raychaudhuri and BJ Allmon.