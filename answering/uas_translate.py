from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
import json
from langchain.prompts import ChatPromptTemplate
from translator import mistral_translator
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from deep_translator import GoogleTranslator
import re

english_translator = GoogleTranslator(target="en")
indonesian_translator = GoogleTranslator(target="id")

llm = Ollama(model="mistral", temperature=0.1)
loader = PyPDFLoader("../assets/books/uas.pdf")
pages = loader.load_and_split()
translated_pages = []

for page in pages:
    translated_content = english_translator.translate(page.page_content)
    # translated_content = mistral_translator.translate_to_english(page.page_content)
    translated_pages.append(Document(metadata=page.metadata, page_content=translated_content))

chrome_store = Chroma.from_documents(documents=translated_pages, embedding=OllamaEmbeddings(model="mistral"))
retriever = chrome_store.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, verbose=True, chain_type="stuff",
                                 chain_type_kwargs={"document_separator": "<<<<>>>>>"})
#
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def cleanAnswer(answer):
    # remove double new line, set to single new line
    response = re.sub(r'\n{2,}', '\n', answer)
    # remove extra spaces or tabs
    response = re.sub(r'\s+', ' ', response)
    # remove multiple dot (.), set to single dot
    response = re.sub(r'\.{2,}', '.', response)
    # trim leading and trailing whitespace
    response = response.strip()
    return response

# prompt = hub.pull("rlm/rag-prompt")
template = """You are the assistant to answer the questions using the given context. Answer questions directly and concisely.
{context}

Question: {question}
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
questions = []
with open("../assets/uas_question.json", "r") as f:
    questions = json.load(f)
    # kuis_questions = filter(lambda x: x['key'] == 'response-6', kuis_questions)
    questions = list(questions)

question_with_answers = []
question_with_answer_english = []
for question in questions:
    print("=======================")
    print("rubric: "+question['rubric'])
    print("question: "+question['question'])
    print("question for model: "+question['question_for_model'])
    translated_rubric = mistral_translator.translate_to_english(question["rubric"])
    translated_question = english_translator.translate(question['question_for_model'])
    # translated_question = mistral_translator.translate_to_english(question['question'])

    answer = rag_chain.invoke(translated_question)
    translated_answer = indonesian_translator.translate(answer)
    # translated_answer = mistral_translator.translate_to_indonesia(answer)
    # print("english answer: "+answer)
    print("answer: "+cleanAnswer(translated_answer))
    print("=======================")
    question_with_answer_english.append({
        "question": translated_question,
        "answer": cleanAnswer(answer),
        "rubric": translated_rubric,
        "key": question['key'],
        "subject": question['subject']
    })
    question_with_answers.append({
        "question": question['question'],
        "answer": cleanAnswer(translated_answer),
        "rubric": question['rubric'],
        "key": question['key'],
        "subject": question['subject']
    })

# save to json file
json_object = json.dumps(question_with_answers, indent=4)
with open("../assets/uas_with_answers.json", "w") as outfile:
    outfile.write(json_object)

json_object = json.dumps(question_with_answer_english, indent=4)
with open("../assets/uas_with_answers_english.json", "w") as outfile:
    outfile.write(json_object)