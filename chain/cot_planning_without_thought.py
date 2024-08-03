from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

chat = ChatGroq(temperature=0, groq_api_key="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",
                model_name="llama3-8b-8192")

# prompt_template = PromptTemplate.from_template("""
# Classify the question as 'open' or 'closed' based on the criteria and examples provided.
#
# A 'closed' question is one whose answer can be found specifically and explicitly in the existing knowledge base. These questions typically have clear right or wrong answers, or are limited to a set number of answer choices. Answers to closed questions are generally factual and do not require interpretation or personal opinion.
#
# Question: {question}
# desire answer format: open or closed
# """)

rubric = """Score 1: Answer does not explain what Artificial Intelligence (AI) is and does not include examples.
Score 2: Answer describes Artificial Intelligence (AI) and does not include any examples.
Score 3: Answer explains Artificial Intelligence (AI) and includes one example.
Score 4: The answer explains Artificial Intelligence (AI) and includes two examples of AI.
Score 5: The answer describes Artificial Intelligence (AI) and includes three or more examples of AI."""

question = "What is meant by AI (Artificial Intelligence) and name 3 (three) examples"
retrieved_answer = "Artificial Intelligence (AI) refers to a branch of computer science that creates systems capable of performing tasks requiring human intelligence, such as language comprehension, learning, reasoning, and perception. Three examples of AI applications are: 1. Voice Recognition: Systems like Siri, Alexa, and Google Assistant that interpret and respond to voice commands. 2. Computer Vision: Technology allowing computers to see and interpret visual content, such as facial recognition or autonomous vehicle systems. 3. Natural Language Processing (NLP): Machines understanding and interacting with human language, used in chatbots, translators, and semantic search."
student_answer = "Artificial Intelligence is an artificial intelligence system which is created as a simulation of human intelligence which is processed or executed by a machine, especially a computer system. Examples of AI: Apple Siri, Google Maps, and Face recognition on Facebook."



def classifying():
    human = """You are an assistant tasked with classifying questions into two categories: subjective or objective. Your task involves a systematic approach to analyze the nature of each question presented to you.

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
"points": "<array_of_point_category_string>"""
    prompt = ChatPromptTemplate.from_messages([("human", human)])
    chain = prompt | chat
    output = chain.invoke({
        "question": question
    })
    return make_output_json(output.content)


def planner(classifying_output):
    type = classifying_output['type']
    explanation = classifying_output['explanation']
    points = ", ".join(classifying_output['points'])

    human = """You are an assistant to help creating thinking step about student answer based on question, context, and rubric.

rubric:
{rubric}

question:
{question}

question category and key-points:
{type}
{explanation}
{points}

context retrieved from document:
{retrieved_answer}

student answer:
{student_answer}

please think it step by step about this rubric, question, question type, key points, context, and student answer

When evaluating answers to questions that include a request for examples, don't limit your assessment to just the examples provided in the provided context. Instead, consider a broad range of possible examples that could apply, ensuring a comprehensive evaluation.

Dont to be strict, be flexible and open-minded to consider various perspectives and interpretations.

output format desire:
json array object with following key:
step : <number>,
about: <string>,
thought: <string>"""
    prompt = ChatPromptTemplate.from_messages([("human", human)])
    chain = prompt | chat
    output = chain.invoke({
        "rubric": rubric,
        "question": question,
        "type": type,
        "explanation": explanation,
        "points": points,
        "retrieved_answer": retrieved_answer,
        "student_answer": student_answer
    })
    return make_output_json_array(output.content)


def response_per_step(classifying_output, planner_output_string):
    type = classifying_output['type']
    explanation = classifying_output['explanation']
    points = ", ".join(classifying_output['points'])
    human = """You are an assistant to give response based on the following steps.

rubric:
{rubric}

question:
{question}

question category and key-points:
{type}
{explanation}
{points}

context retrieved from document:
{retrieved_answer}

student answer:
{student_answer}

steps:
{steps}

please response the thought per step

output format desire:
json array object with following keys:
step: <number>,
about: <string>,
thought: <string>,
response: <string>"""

    prompt = ChatPromptTemplate.from_messages([("human", human)])
    chain = prompt | chat
    output = chain.invoke({
        "rubric": rubric,
        "question": question,
        "type": type,
        "explanation": explanation,
        "points": points,
        "retrieved_answer": retrieved_answer,
        "student_answer": student_answer,
        "steps": planner_output_string
    })
    return make_output_json(output.content)


def scoring(classifying_output, response_per_step_output_string):
    type = classifying_output['type']
    explanation = classifying_output['explanation']
    points = ", ".join(classifying_output['points'])

    human = """You are an academic expert to give score and reason for the student answer.

rubric:
{rubric}

question:
{question}

question category and keypoints:
{type}
{explanation}
{points}

context retrieved from document:
{retrieved_answer}

student answer:
{student_answer}

thoughts:
{thoughts}

Give score and reasoning for the student answer based on thoughts provided.

output desired format:
json object with following attibute:
question: <string>
answer: <student_answer>
score: <number>
reasoning: <string>"""
    prompt = ChatPromptTemplate.from_messages([("human", human)])
    chain = prompt | chat
    output = chain.invoke({
        "rubric": rubric,
        "question": question,
        "type": type,
        "explanation": explanation,
        "points": points,
        "retrieved_answer": retrieved_answer,
        "student_answer": student_answer,
        "thoughts": response_per_step_output_string
    })
    return make_output_json(output.content)


def make_output_json_array(output):
    llm_output = output
    # if llm_output is contains } or not
    if "[" in llm_output:
        llm_output = llm_output[llm_output.index("["):]
    else:
        if llm_output[0] != "[":
            llm_output = "[" + llm_output

    # check if llm_output is end with } or not
    if "]" in llm_output:
        llm_output = llm_output[:llm_output.index("]") + 1]
    else:
        if llm_output[-1] != "]":
            llm_output += "]"

    # print(llm_output)
    return llm_output

def make_output_json(output):
    llm_output = output
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
    return llm_output



classifying_output = classifying()
print(classifying_output)
planner_output = planner(eval(classifying_output))
print(planner_output)
# transform planner_output array to string

planner_output_string = ""
for item in eval(planner_output):
    planner_output_string += f"""step: {item['step']}
about: {item['about']}
thought: {item['thought']}"""
    #     if last item, don't add \n
    if item != eval(planner_output)[-1]:
        planner_output_string += "\n"

print(planner_output)
print(planner_output_string)
print("====================================")
# response_per_step_output = response_per_step(eval(classifying_output), planner_output_string)
# print(response_per_step_output)

# response_per_step_output_string = ""
# for item in eval(response_per_step_output):
#     response_per_step_output_string += f"""step: {item['step']}
# about: {item['about']}
# thought: {item['thought']}
# response: {item['response']}"""
#     #     if last item, don't add \n
#     if item != eval(response_per_step_output)[-1]:
#         response_per_step_output_string += "\n"
#
# print(response_per_step_output_string)
scoring_output = scoring(eval(classifying_output), planner_output_string)
print(scoring_output)

# response_per_step(eval(classifying_output), eval(planner_output))

# print(planner_output)
