from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


# ==========================================
# Step 1a - Indexing (Document Ingestion)
# ==========================================

video_id = "etnLX7m2MiA"

try:
    api = YouTubeTranscriptApi()
    transcript_data = api.fetch(video_id, languages=["hi"])

    # Combine transcript chunks into one string
    transcript = " ".join(chunk.text for chunk in transcript_data)

except TranscriptsDisabled:
    print("No captions available.")
    exit()


# ==========================================
# Step 1b - Text Splitting
# ==========================================

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.create_documents([transcript])


# ==========================================
# Step 1c & 1d - Embeddings + Vector Store
# ==========================================

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = FAISS.from_documents(chunks, embeddings)


# ==========================================
# Step 2 - Retrieval
# ==========================================

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})


# ==========================================
# Step 3 - Augmentation
# ==========================================

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.3
)

model = ChatHuggingFace(llm=llm)

prompt = PromptTemplate(
    template="""
You are a helpful assistant.

Answer ONLY from the provided transcript context.

If the answer is not available in context, just say:
"I don't know."

Context:
{context}

Question:
{question}
""",
    input_variables=["context", "question"]
)


# ==========================================
# Step 4 - Manual RAG Flow
# ==========================================

question = "Is the topic of nuclear fusion discussed in this video? If yes, what was discussed?"

retrieved_docs = retriever.invoke(question)

context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

final_prompt = prompt.invoke({
    "context": context_text,
    "question": question
})

answer = model.invoke(final_prompt)

print("\n========== ANSWER ==========\n")
print(answer.content)


# ==========================================
# Step 5 - LCEL Chain
# ==========================================

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


parallel_chain = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

parser = StrOutputParser()

main_chain = parallel_chain | prompt | model | parser

response = main_chain.invoke("Can you summarize the video?")

print("\n========== SUMMARY ==========\n")
print(response)