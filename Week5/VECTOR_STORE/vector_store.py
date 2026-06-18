# pip install langchain langchain-community faiss-cpu sentence-transformers

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# =====================================================
# 1. CREATE BASIC DOCUMENTS
# =====================================================

docs = [
    Document(
        page_content="Python is a programming language",
        metadata={"source": "doc1"}
    ),

    Document(
        page_content="Machine learning predicts patterns from data",
        metadata={"source": "doc2"}
    ),

    Document(
        page_content="Deep learning uses neural networks",
        metadata={"source": "doc3"}
    ),

    Document(
        page_content="Cricket is a famous sport in India",
        metadata={"source": "doc4"}
    )
]


# =====================================================
# 2. LOAD EMBEDDING MODEL
# =====================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# =====================================================
# 3. from_documents()
# Create Vector Store
# =====================================================

vectorstore = FAISS.from_documents(
    documents=docs,
    embedding=embeddings
)

print("Vector Store Created Successfully")


# =====================================================
# 4. similarity_search()
# Retrieve similar documents
# =====================================================

print("\n===== similarity_search() =====")

results = vectorstore.similarity_search(
    query="How does AI predict?",
    k=2
)

for doc in results:
    print(doc.page_content)


# =====================================================
# 5. similarity_search_with_score()
# Retrieve docs + similarity score
# =====================================================

print("\n===== similarity_search_with_score() =====")

results = vectorstore.similarity_search_with_score(
    query="How does AI predict?",
    k=2
)

for doc, score in results:
    print("Document:", doc.page_content)
    print("Score:", score)
    print()


# =====================================================
# 6. as_retriever()
# Convert VectorStore → Retriever
# =====================================================

print("\n===== as_retriever() =====")

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

retrieved_docs = retriever.invoke(
    "What is machine learning?"
)

for doc in retrieved_docs:
    print(doc.page_content)


# =====================================================
# 7. add_documents()
# Add new documents
# =====================================================

print("\n===== add_documents() =====")

new_docs = [
    Document(
        page_content="Artificial Intelligence is transforming healthcare",
        metadata={"source": "doc5"}
    )
]

vectorstore.add_documents(new_docs)

results = vectorstore.similarity_search(
    "AI in healthcare",
    k=1
)

for doc in results:
    print(doc.page_content)


# =====================================================
# 8. delete()
# Delete documents
# =====================================================

print("\n===== delete() =====")

# First add IDs manually
ids = vectorstore.add_documents([
    Document(
        page_content="Temporary document",
        metadata={"source": "temp"}
    )
])

print("Added temp doc")

# Delete using ID
vectorstore.delete(ids=ids)

print("Temporary document deleted")


# =====================================================
# 9. save_local()
# Save vector store
# =====================================================

print("\n===== save_local() =====")

vectorstore.save_local("my_faiss_db")

print("Vector DB saved locally")


# =====================================================
# 10. load_local()
# Load saved vector store
# =====================================================

print("\n===== load_local() =====")

loaded_db = FAISS.load_local(
    folder_path="my_faiss_db",
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)

print("Vector DB Loaded Successfully")


# =====================================================
# TEST loaded DB
# =====================================================

print("\n===== Testing Loaded DB =====")

results = loaded_db.similarity_search(
    "What predicts patterns?",
    k=1
)

for doc in results:
    print(doc.page_content)