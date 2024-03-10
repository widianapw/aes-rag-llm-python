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


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


llm = Ollama(model="mistral")
kuis_questions = []
question_with_answers = []
with open("../assets/kuis_question.json", "r") as f:
    kuis_questions = json.load(f)
    # kuis_questions = filter(lambda x: x['key'] == 'response-6', kuis_questions)
    kuis_questions = list(kuis_questions)

for index, question in enumerate(kuis_questions):
    asset_name = "kuis-" + str(index + 1)

    loader = PyPDFLoader("../assets/books/" + asset_name + ".pdf")
    pages = loader.load_and_split()

    chrome_store = Chroma.from_documents(documents=pages, embedding=OllamaEmbeddings(model="mistral"))
    retriever = chrome_store.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, verbose=True, chain_type="stuff",
                                     chain_type_kwargs={"document_separator": "<<<<>>>>>"})

    # prompt = hub.pull("rlm/rag-prompt")
    template = """Anda adalah asisten untuk menjawab soal dengan menggunakan konteks yang diberikan. Jawablah pertanyaan secara langsung dan ringkas.
{context}

Soal: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )
    print("=======================")
    print("question: " + question['question'])
    answer = rag_chain.invoke(question['question'])
    print("answer: " + answer)
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
