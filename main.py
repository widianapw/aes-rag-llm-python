import bs4
from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

llm = Ollama(model="mistral")
loader = WebBaseLoader(
    web_paths=("https://revou.co/kosakata/big-data",),
    # bs_kwargs=dict(
    #     parse_only=bs4.SoupStrainer(
    #         class_=("post-content", "post-title", "post-header")
    #     )
    # ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
# print(splits)
# qa_translator = DoctranTextTranslator(language="indonesian")
# translated_document = qa_translator.transform_documents(splits)

vector_store = Chroma.from_documents(documents=splits, embedding=GPT4AllEmbeddings())
retriever = vector_store.as_retriever()


template = """Anda adalah asisten untuk tugas menjawab soal. Gunakan potongan-potongan konteks yang diambil berikut ini untuk menjawab pertanyaan. Jika Anda tidak tahu jawabannya, katakan saja bahwa Anda tidak tahu. Buatlah jawaban yang ringkas.
{context}

Soal: {question}

"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("Chain is ready!")

print(chain.invoke("Sebutkan karakteristik dari big data!"))