from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
import json
from utils import normalizer
from deep_translator import GoogleTranslator

import os

chat = ChatGroq(temperature=0.1, groq_api_key="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",
                model_name="llama3-8b-8192")
system = "You are an academic assistant tasked with scoring and providing reasoning for student answers based on specific guidelines."
human = """
Scoring Guidelines:
Score 5: The answer accurately describes Artificial Intelligence (AI) and includes more than two correct examples of AI.
Score 4: The answer explains Artificial Intelligence (AI) accurately and includes two correct examples of AI.
Score 3: The answer explains Artificial Intelligence (AI) accurately and includes one correct example of AI.
Score 2: The answer describes Artificial Intelligence (AI) but does not include any examples.
Score 1: The answer does not explain what Artificial Intelligence (AI) is and does not include examples.

Input:
Question: What is meant by AI (Artificial Intelligence) and name 3 (three) examples
Context: 
- Artificial Intelligence (AI) refers to a branch of computer science that creates systems capable of performing tasks requiring human intelligence, such as language comprehension, learning, reasoning, and perception. 
- Three examples of AI applications are:
  1. Voice Recognition: Systems like Siri, Alexa, and Google Assistant that interpret and respond to voice commands.
  2. Computer Vision: Technology allowing computers to "see" and interpret visual content, such as facial recognition or autonomous vehicle systems.
  3. Natural Language Processing (NLP): Machines understanding and interacting with human language, used in chatbots, translators, and semantic search.

Student Answer: Artificial Intelligence is an artificial intelligence system which is created as a simulation of human intelligence which is processed or executed by a machine, especially a computer system. Examples of AI: Apple Siri, Google Maps, and Face recognition on Facebook.

Step-by-Step Evaluation:
1. Does the answer describe or explain AI accurately based on the provided context?
2. Count the number of correct examples provided in the answer (correct examples should align with the context provided).

Let's think step by step and then evaluate the student's answer.

Desired Output Format:
JSON object with keys "question", "score", and "reasoning" in one line."""
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat

indonesian_translator = GoogleTranslator(target="id")
english_translator = GoogleTranslator(target="en")

response = chain.invoke({})
llm_output = response.content
print(llm_output)
# if llm_output is contains } or not
if "{" in llm_output:
    llm_output = llm_output[llm_output.index("{"):]
else:
    if llm_output[0] != "{":
        llm_output = "{" + llm_output

# check if llm_output is end with } or not
if "}" in llm_output:
    llm_output = llm_output[:llm_output.index("}") + 1]
else:
    if llm_output[-1] != "}":
        llm_output += "}"

# print(llm_output)

result = eval(llm_output)
#
# # remove the rating from the reasoning
reasoning = result['reasoning']
translated_reasoning = GoogleTranslator(source='en', target='id').translate(result['reasoning'])
print("Question : What is meant by AI (Artificial Intelligence) and name 3 (three) examples")
print("Score : ", result['score'])
print("Reasoning : ", result['reasoning'])
print(result)
print("====================================")



