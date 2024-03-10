from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
import json
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

llm = Ollama(model="mistral", temperature=0.1)
loader = PyPDFLoader("../assets/books/kuis.pdf")
pages = loader.load_and_split()

chrome_store = Chroma.from_documents(documents=pages, embedding=OllamaEmbeddings(model="mistral"))
retriever = chrome_store.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, verbose=True, chain_type="stuff",
                                 chain_type_kwargs={"document_separator": "<<<<>>>>>"})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# prompt = hub.pull("rlm/rag-prompt")
template = """Anda adalah asisten untuk menjawab soal dengan menggunakan konteks yang diberikan. Jawablah pertanyaan secara langsung dan ringkas.
Konteks: {context}

Soal: {question}

"""
prompt = ChatPromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


# load json file
# kuis_responses = []
# with open("../assets/kuis.json", "r") as f:
#     kuis_responses = json.load(f)
#     kuis_responses = filter(lambda x: x['key'] == 'response-1', kuis_responses)
#     kuis_responses = list(kuis_responses)
# #     get the first 5 responses
# kuis_responses = kuis_responses[:5]

# kuis question
kuis_questions = []
with open("../assets/kuis_question.json", "r") as f:
    kuis_questions = json.load(f)
    # kuis_questions = filter(lambda x: x['key'] == 'response-6', kuis_questions)
    kuis_questions = list(kuis_questions)

question_with_answers = []
for question in kuis_questions:
    print("=======================")
    print("question: "+question['question'])
    answer = rag_chain.invoke(question['question'])
    print("answer: "+answer)
    print("=======================")
    question_with_answers.append({
        "question": question['question'],
        "answer": answer,
        "rubric": question['rubric'],
        "key": question['key'],
        "subject": question['subject']
    })

# save to json file
json_object = json.dumps(question_with_answers, indent=4)
with open("../assets/kuis_with_answers_1.json", "w") as outfile:
    outfile.write(json_object)