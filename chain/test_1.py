from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

chat = ChatGroq(temperature=0, groq_api_key="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",
                model_name="llama3-8b-8192")

# 1. extract the question
question = "What is meant by AI (Artificial Intelligence) and name 3 (three) examples"
student_answer = "Artificial Intelligence is an artificial intelligence system which is created as a simulation of human intelligence which is processed or executed by a machine, especially a computer system. Examples of AI: Apple Siri, Google Maps, and Face recognition on Facebook."
context = """- Artificial Intelligence (AI) refers to a branch of computer science that creates systems capable of performing tasks requiring human intelligence, such as language comprehension, learning, reasoning, and perception. 
- Three examples of AI applications are:
  1. Voice Recognition: Systems like Siri, Alexa, and Google Assistant that interpret and respond to voice commands.
  2. Computer Vision: Technology allowing computers to "see" and interpret visual content, such as facial recognition or autonomous vehicle systems.
  3. Natural Language Processing (NLP): Machines understanding and interacting with human language, used in chatbots, translators, and semantic search.
"""
system = "You are an academic assistant tasked with scoring and providing reasoning for student answers based on specific guidelines."
# rubric = """Score 5: The answer accurately describes Artificial Intelligence (AI) and includes more than two correct examples of AI.
# Score 4: The answer explains Artificial Intelligence (AI) accurately and includes two correct examples of AI.
# Score 3: The answer explains Artificial Intelligence (AI) accurately and includes one correct example of AI.
# Score 2: The answer describes Artificial Intelligence (AI) but does not include any examples.
# Score 1: The answer does not explain what Artificial Intelligence (AI) is and does not include examples."""

rubric = """Score 1: The answer does not explain what Artificial Intelligence (AI) is and does not include examples.
Score 2: The answer describes Artificial Intelligence (AI) but does not include any examples.
Score 3: The answer explains Artificial Intelligence (AI) accurately and includes one correct example of AI.
Score 4: The answer explains Artificial Intelligence (AI) accurately and includes two correct examples of AI.
Score 5: The answer accurately describes Artificial Intelligence (AI) and includes more than two correct examples of AI."""

rubric_array = rubric.split("\n")

rubrics = []
for rubric in rubric_array:
    # extract the rubric score
    score = rubric.split(":")[0].strip()
    # get the score value
    score = int(score.split(" ")[1])
    # extract the rubric description
    description = rubric.split(":")[1].strip()
    rubrics.append({"score": score, "description": description})


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
    return eval(llm_output)


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


def extract():
    human = """
    question: {question}

Read the following questions, then extract the following questions and determine the aspects that students must answer.

desired output format:
json array of string
"""
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    response = chain.invoke({"question": question})
    return make_output_json_array(response.content)


def evaluate_per_aspect(extraction_result):
    extraction_result_string = ""
    for result in extraction_result:
        extraction_result_string += result + "\n"

    human = """
Student answer:
{answer}

Question aspects:
{aspects}

Supporting Theory:
{context}

Use your knowledge to evaluate the student's answer based on the question aspects provided.
Evaluate the student's answer based on the question aspects provided.

desired output format:
json array with keys "aspect", "student_answer", "evaluation_level", and "evaluation" in one line
"""
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    response = chain.invoke({"answer": student_answer, "aspects": extraction_result_string, "context": context})
    return make_output_json_array(response.content)


def match_per_rubric(evaluation_per_aspect_result):
    evaluation_per_aspect_result_string = ""
    for result in evaluation_per_aspect_result:
        evaluation_per_aspect_result_string += f"""aspect: {result['aspect']}
evaluation_aspect: {result['evaluation']}
\n"""
    results = []
    for rubric in rubrics:
        rubcric_string = f"""rubric: {rubric['description']}
rubric_score: {rubric['score']}"""
        human = """
Score Guideline:
{rubric}

Evaluation aspects:
{evaluation_aspects}

Student answer: 
{student_answer}

Calculate the match rate between the rubric and student answer.

desired output format:
json object with keys "rubric", "rubric_score", "match_rate", and "reason" in one line
"""
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
        chain = prompt | chat
        response = chain.invoke({"rubric": rubcric_string, "student_answer": student_answer,
                                 "evaluation_aspects": evaluation_per_aspect_result_string})
        results.append(make_output_json(response.content))

    return results


def matching_rubric(evaluation_per_aspect_result):
    evaluation_per_aspect_result_string = ""
    for result in evaluation_per_aspect_result:
        evaluation_per_aspect_result_string += f"""
        aspect: {result['aspect']}
        student_answer: {result['student_answer']}
        evaluation: {result['evaluation']}
        \n
        """

    human = """
Scoring Guidelines:
{rubric}

Student evaluation aspects:
{evaluation_aspects}

student answer:
{student_answer}

Give the evaluation per scoring guidelines provided.

desired output format:
json array with keys "scoring_guideline", "student_answer", "match_level", and "match" in one line
"""
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | chat
    response = chain.invoke(
        {"rubric": rubric, "evaluation_aspects": evaluation_per_aspect_result_string, "student_answer": student_answer})
    return make_output_json_array(response.content)


def rubric_based_evaluation(evaluation_per_aspect_result):
    evaluation_per_aspect_result_string = ""

    for result in evaluation_per_aspect_result:
        evaluation_per_aspect_result_string += f"""
        aspect: {result['aspect']}
        student_answer: {result['student_answer']}
        evaluation: {result['evaluation']}
        \n
        """
    human = """
Scoring Guidelines:
{rubric}

Student evaluation aspects:
{evaluation_aspects}

Evaluate the student evaluation aspect based on Scoring guidelines provided,

desired output format:
json object with keys "question", "score", and "reasoning" in one line
"""
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt | chat
    response = chain.invoke({"rubric": rubric, "evaluation_aspects": evaluation_per_aspect_result_string})
    return make_output_json(response.content)


extraction_result = extract()
print("Extraction Result:")
for result in extraction_result:
    print(result)

evaluation_per_aspect_result = evaluate_per_aspect(extraction_result)
print("\nEvaluation Result:")
for result in evaluation_per_aspect_result:
    print(result)

matching_per_rubric_result = match_per_rubric(evaluation_per_aspect_result)
print("\nMatching per Rubric Result:")
for result in matching_per_rubric_result:
    print(result)

matching_rubric_result = matching_rubric(evaluation_per_aspect_result)
print("\nMatching Rubric Result:")
for result in matching_rubric_result:
    print(result)

# evaluation_result = rubric_based_evaluation(evaluation_per_aspect_result)
# print("\nEvaluation Result:")
# print(evaluation_result)
