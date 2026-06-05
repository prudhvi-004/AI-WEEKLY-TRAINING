from langchain_text_splitters import MarkdownHeaderTextSplitter

# Sample markdown text
markdown_text = """
# Introduction
LangChain is a framework for building LLM applications.

## What is RAG?
RAG stands for Retrieval-Augmented Generation.
It retrieves relevant context before answering.

## What is an Agent?
An Agent can use tools and reason step by step.

# Conclusion
LangChain helps build advanced AI applications.
"""

# Define markdown headers to split on
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2")
]

# Create splitter object
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

# Split markdown text
chunks = splitter.split_text(markdown_text)

# Print chunks
for i, chunk in enumerate(chunks, start=1):
    print(f"\n========== CHUNK {i} ==========")

    print("Content:")
    print(chunk.page_content)

    print("\nMetadata:")
    print(chunk.metadata)