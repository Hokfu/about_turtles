from langchain_community.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)




 
