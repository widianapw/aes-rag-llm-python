from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

chat = ChatGroq(temperature=0, groq_api_key="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",
                model_name="llama3-70b-8192")

# Step 1: Extract key components and concepts
system_1 = "You are an academic assistant tasked with identifying key components and concepts from questions."
human_1 = """
Extract the key components and concepts from the following question: 
What is meant by AI (Artificial Intelligence) and name 3 (three) examples

Response format:
- Key Components: [list of key components]
- Concepts: [list of main concepts]
"""
prompt_1 = ChatPromptTemplate.from_messages([("system", system_1), ("human", human_1)])
chain_1 = prompt_1 | chat
response_1 = chain_1.invoke({}).content
print(response_1)

# Step 2: Identify ground truth based on extracted key components and concepts
system_2 = "You are an academic assistant tasked with identifying ground truth based on key components and concepts."
human_2 = f"""
Based on the key components and concepts extracted, identify the expected key points (ground truth) that a correct answer should include:
{response_1}

Response format:
- Ground Truth: [list of key points]
"""
prompt_2 = ChatPromptTemplate.from_messages([("system", system_2), ("human", human_2)])
chain_2 = prompt_2 | chat
response_2 = chain_2.invoke({}).content
print(response_2)

# Step 3: Evaluate the student answer based on the ground truth and rubric
system_3 = "You are an academic assistant tasked with evaluating student answers based on provided ground truth and rubric."
human_3 = f"""
Evaluate the following student answer based on the extracted ground truth and the provided rubric:
Question: What is meant by AI (Artificial Intelligence) and name 3 (three) examples
Student Answer: Artificial Intelligence adalah sebuah sistem kecerdasan buatan yang mana dibuat sebagai simulasi kecerdasan manusia yang diproses atau dijalankan oleh suatu mesin terutama sistem komputer. Contoh AI : Apple Siri, Google Maps, dan Face recognition pada Facebook.
Ground Truth: {response_2}
Rubric: 
Score 1: Answer does not explain what Artificial Intelligence (AI) is and does not include examples.
Score 2: Answer describes Artificial Intelligence (AI) and does not include any examples.
Score 3: Answer explains Artificial Intelligence (AI) and includes one relevant example.
Score 4: The answer explains Artificial Intelligence (AI) and includes two examples of AI.
Score 5: The answer describes Artificial Intelligence (AI) and includes more than two examples of AI.

Analyze the reasoning and examples provided in the student answer. Check for the presence of key arguments and their alignment with the expected answer.

Response format:
- Presence of Key Points: [list of identified key points from student answer]
- Missing Key Points: [list of missing key points]
- Number of Examples: [count of examples provided by student]
- Reasoning Quality: [evaluation of reasoning quality]
"""
prompt_3 = ChatPromptTemplate.from_messages([("system", system_3), ("human", human_3)])
chain_3 = prompt_3 | chat
response_3 = chain_3.invoke({}).content
print(response_3)

# Step 4: Adjust the evaluation based on flexible criteria
system_4 = "You are an academic assistant tasked with adjusting evaluations based on flexible criteria."
human_4 = f"""
Based on the evaluation, adjust the assessment using the following flexible criteria:
{response_3}

Response format:
- Adjusted Evaluation: [detailed evaluation with flexible criteria]
- Suggested Score: [score based on evaluation]
"""
prompt_4 = ChatPromptTemplate.from_messages([("system", system_4), ("human", human_4)])
chain_4 = prompt_4 | chat
response_4 = chain_4.invoke({}).content
print(response_4)

# Step 5: Finalize the score and provide justification
system_5 = "You are an academic assistant tasked with finalizing scores and providing justifications."
human_5 = f"""
Finalize the score by looping through the rubric criteria and provide a brief justification for the score assigned:
{response_4}

Response format:
- Final Score: [assigned score]
- Justification: [brief justification based on overall context]
"""
prompt_5 = ChatPromptTemplate.from_messages([("system", system_5), ("human", human_5)])
chain_5 = prompt_5 | chat
response_5 = chain_5.invoke({}).content
print(response_5)
