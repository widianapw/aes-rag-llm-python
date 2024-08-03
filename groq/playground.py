from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

chat = ChatGroq(temperature=1, groq_api_key="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",
                model_name="llama3-70b-8192")
system = "You are an academic assistant tasked with scoring and providing reasoning for student answers based on specific guidelines."
human = """
Scoring guideline:
The answer describes Artificial Intelligence (AI) and only include one examples of AI.

Student Answer:
Artificial Intelligence is an artificial intelligence system which is created as a simulation of human intelligence which is processed or executed by a machine, especially a computer system. Examples of AI: Face Recognition Facebook

Student Answer Breakdown:
1. Artificial Intelligence is an artificial intelligence system which is created as a simulation of human intelligence which is processed or executed by a machine, especially a computer system. 
2. Examples of AI: Face Recognition Facebook.

Take the following steps:
Breakdown the scoring guideline and determine whether or not the student answer and scoring guideline are match.

desired output format:
json object with key:
is_match: boolean
match_rate: number"""
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat

print(chain.invoke({}).content)