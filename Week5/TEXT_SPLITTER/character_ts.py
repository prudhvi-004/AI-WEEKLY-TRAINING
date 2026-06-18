from langchain_text_splitters import CharacterTextSplitter

text = """
LangChain is a framework for building LLM applications.
It helps create RAG systems and agents.
"""

splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=50,
    chunk_overlap=10
)

chunks = splitter.split_text(text)

print(chunks)