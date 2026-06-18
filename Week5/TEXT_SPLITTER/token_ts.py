from langchain_text_splitters import TokenTextSplitter

text = """
LangChain helps developers build applications using large language models.
"""

splitter = TokenTextSplitter(
    chunk_size=10,
    chunk_overlap=2
)

chunks = splitter.split_text(text)

print(chunks)