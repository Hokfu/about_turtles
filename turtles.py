from langchain_community.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
import os
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
query = "Turtles"
pages = WikipediaLoader(query=query, load_max_docs=2).load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


repo_id = "meta-llama/Meta-Llama-3-8B-Instruct"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_new_tokens=128,
    temperature=0.5,
    huggingfacehub_api_token=HF_TOKEN,
)
embeddings = HuggingFaceEndpointEmbeddings()

docs = text_splitter.split_documents(pages)
db = FAISS.from_documents(docs, embeddings)
retriever = db.as_retriever()

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    Question: {question} 

    Context: {context} 

    Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """,
    input_variables=["question", "document"],
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)




 
