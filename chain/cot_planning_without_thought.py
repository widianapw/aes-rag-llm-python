from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

llm = Ollama(model="mistral")

# prompt_template = PromptTemplate.from_template("""
# Classify the question as 'open' or 'closed' based on the criteria and examples provided.
#
# A 'closed' question is one whose answer can be found specifically and explicitly in the existing knowledge base. These questions typically have clear right or wrong answers, or are limited to a set number of answer choices. Answers to closed questions are generally factual and do not require interpretation or personal opinion.
#
# Question: {question}
# desire answer format: open or closed
# """)

rubric = """Score 1: The answer does not explain the actuator in IoT and does not provide an example.
Score 2: The answer explains the actuator in IoT but does not provide an example.
Score 3: The answer explains the actuator in IoT and provides only one example.
Score 4: The answer explains the actuator in IoT and provides two examples.
Score 5: The answer explains the actuator in IoT and provides three examples."""

question = "Explain Actuators in the Internet of Things (IoT) and give examples!"
retrieved_answer = "Actuators are devices that enable IoT applications to carry out real actions in the physical world. They are used to control the flow of liquids or gases, regulate temperature, and ventilate or cool air. Examples of actuators include water pumps, electric valves, heaters, and electric fans. These devices are crucial in home automation, industry, smart agriculture, healthcare, and many other areas where IoT is used to monitor environmental conditions and automatically take appropriate action."

student_answer = "Actuator is one form of Physical component in the Internet of Things IoT. Actuator is a component or equipment to move or control a mechanism or system. Example of Actuator:  Actuators in cars that function to move the car system.  Actuator on a robot that functions to produce movement on the robot Actuator on a light search engine that functions to move the machine following the direction of the light source."


def classifying():
    prompt_template = PromptTemplate.from_template("""You are an assistant tasked with classifying questions into two categories: subjective or objective. Your task involves a systematic approach to analyze the nature of each question presented to you.

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
"points": "<array_of_point_category_string>""")
    output = llm.invoke(prompt_template.format(question=question))
    return output


def planner(classifying_output):
    type = classifying_output['type']
    explanation = classifying_output['explanation']
    points = ", ".join(classifying_output['points'])
    prompt_template = PromptTemplate.from_template("""You are an assistant to help creating thinking step about student answer based on question, context, and rubric.

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

output format desire:
json array object with following key:
step : <number>,
about: <string>,
thought: <string>""")
    prompt_final = prompt_template.format(rubric=rubric, question=question, type=type, explanation=explanation,
                                          points=points, retrieved_answer=retrieved_answer,
                                          student_answer=student_answer)
    print(prompt_final)
    output = llm.invoke(prompt_final)
    return output


def response_per_step(classifying_output, planner_output_string):
    type = classifying_output['type']
    explanation = classifying_output['explanation']
    points = ", ".join(classifying_output['points'])

    prompt_template = PromptTemplate.from_template("""You are an assistant to give response based on the following steps.

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
response: <string>""")
    prompt_final = prompt_template.format(rubric=rubric, question=question, type=type, explanation=explanation,
                                          points=points, retrieved_answer=retrieved_answer,
                                          student_answer=student_answer, steps=planner_output_string)
    print(prompt_final)
    output = llm.invoke(prompt_final)
    return output


def scoring(classifying_output, response_per_step_output_string):
    type = classifying_output['type']
    explanation = classifying_output['explanation']
    points = ", ".join(classifying_output['points'])

    prompt_template = PromptTemplate.from_template("""You are an academic expert to give score and reason for the student answer.

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
reasoning: <string>""")
    prompt_final = prompt_template.format(rubric=rubric, question=question, type=type, explanation=explanation,
                                          points=points, retrieved_answer=retrieved_answer,
                                          student_answer=student_answer, thoughts=response_per_step_output_string)
    print(prompt_final)
    output = llm.invoke(prompt_final)
    return output


classifying_output = classifying()
planner_output = planner(eval(classifying_output))
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
