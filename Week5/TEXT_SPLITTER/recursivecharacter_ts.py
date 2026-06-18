from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
LangChain is a framework for building LLM applications.
It helps build RAG pipelines, agents, and workflows.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10
)

chunks = splitter.split_text(text)

print(chunks)