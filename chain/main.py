from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

llm = Ollama(model="mistral", temperature=0)

# prompt_template = PromptTemplate.from_template("""
# Classify the question as 'open' or 'closed' based on the criteria and examples provided.
#
# A 'closed' question is one whose answer can be found specifically and explicitly in the existing knowledge base. These questions typically have clear right or wrong answers, or are limited to a set number of answer choices. Answers to closed questions are generally factual and do not require interpretation or personal opinion.
#
# Question: {question}
# desire answer format: open or closed
# """)

prompt_template = PromptTemplate.from_template("""
You are an assistant tasked with classifying questions into two categories: subjective or objective. Your task involves a systematic approach to analyze the nature of each question presented to you.

Question: "{question}"

Task Breakdown:
1. Identify if the question asks for factual, verifiable information or specific knowledge that has universally agreed-upon answers. This indicates an objective question.
2. Determine if the question seeks personal opinions, experiences, interpretations, or examples that may vary from one person to another. This indicates a subjective question.
3. Based on your analysis in steps 1 and 2, classify the question as either 'subjective' or 'objective'.
4. Categorize the keypoint requested in the question into specific types, such as asking for 'examples', 'explanations', 'definitions', 'comparisons', etc., to understand the nature of information or perspective needed.

Output Desired:
json object with the following keys:
"question": "{question}",
"type": <subjective_or_objective_lower_cased>,
"explanation: "<explanation>",
"points": "<array_of_point_category_string>"
""")

"""
Instructions:
Classify the question as 'open' or 'closed' based on the criteria provided.

Open questions need opinions or examples. They ask for more than just facts, inviting personal thoughts, experiences, or illustrative examples.

Closed questions have answers already in the knowledge book. They can be answered with specific facts or details that are directly available or known.

Question: "{question}"

desire format:
json object with the following keys:
"question": "{question}",
"answer": <open_or_closed_lower_cased>,
"explanation": <explanation_of_why_the_question_is_open_or_closed>
"""

# load json file
questions =[]
with open('../assets/uas_with_answers_english.json') as f:
    questions = f.read()
    questions = eval(questions)

# print(llm.invoke("""
# {
# "question": "The module explains the 3 characteristics of Big Data, namely Variety, Velocity and Volume. Name and explain the other 2Vs that have been explained in the module.",
# "answer": "closed"
# }
# {
# "question": "Give examples of Big Data implementation in your respective fields",
# "answer": "open"
# }
# {
# "question": "Mention and briefly explain the characteristics of a data collection called Big Data",
# "answer": "closed"
# }
# {
# "question": "What is meant by the velocity characteristic?",
# "answer": "closed"
# }
# {
# "question": "What are the 3 differences between a relational database and a data warehouse?",
# "answer": "open"
# }
# {
# "question": "What challenges exist when implementing Big Data?",
# "answer": "open"
# }
#
# please write me the definition of open and close question
# """))
for question in questions:
    prompt = prompt_template.format(question=question["question"])
    print(llm.invoke(prompt))
# prompt = prompt_template.format(question="What are the 5 (five) criteria for data to be called big data? and explain briefly and adequately.")
#
# # print(prompt)
#
# response = llm.invoke(prompt)
# # dict_response = eval(response)
# print(response)

# print(dict_response["answer"])  # Assuming 'response' is the variable that holds the LLM output.

