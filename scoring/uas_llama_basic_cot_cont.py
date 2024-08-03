from langchain_community.llms import Ollama
import json
from langchain.evaluation import load_evaluator
from translator import mistral_translator
from utils import normalizer
from deep_translator import GoogleTranslator
from langchain.prompts import PromptTemplate

import os

prompt_template = PromptTemplate.from_template("""
You are an assistant to give score and reasoning for the student answer.

rubric:
{rubric}

question:
{question}

context retrieved from document:
{context}

student answer:
{answer}

Lets thinking step by step and evaluate the student answer based on the rubric and context.

Desired Output Format:
JSON object with keys "question", "score", and "reasoning" in one line.
""")

def get_current_max_no(key):
    try:
        with open("../assets/results/uas_llama_id.json", "r") as file:
            data = json.load(file)
            data_key = list(filter(lambda x: x['key'] == key, data))
            max_no = max([item["no"] for item in data_key], default=0)
            return max_no
    except FileNotFoundError:
        return 0

def append_to_json(file_path, result):
    data = []
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding JSON from file")
                return

    data.append(result)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


indonesian_translator = GoogleTranslator(target="id")
english_translator = GoogleTranslator(target="en")

llm = Ollama(model="llama3:8b")

questions = []
with open("../assets/uas_with_answers_english.json", "r") as f:
    questions = json.load(f)
    # questions = filter(lambda x: x['key'] == 'response-3', questions)
    questions = list(questions)
    # questions = questions[:2]

questions_id = []
with open("../assets/uas_question.json", "r") as f:
    questions_id = json.load(f)
    # questions = filter(lambda x: x['key'] == 'response-3', questions)
    questions_id = list(questions_id)

for question in questions:
    current_max_no = get_current_max_no(question['key'])
    question_id = list(filter(lambda x: x['key'] == question['key'], questions_id))[0]
    print("Rubric : ", question['rubric'])
    print("Question : ", question['question'])

    # evaluator = LabeledScoreStringEvalChain.from_llm(
    #     llm=llm,
    #     criteria=accuracy_criteria,
    #     prompt=evaluator_prompt
    # )

    answers = []
    with open("../assets/uas.json", "r") as f:
        answers = json.load(f)
        answers = filter(lambda x: x['key'] == question['key'] and x['subject'] == 'uas', answers)
        answers = filter(lambda x: x['no'] > current_max_no, answers)
        answers = list(answers)
        # answers = answers[:20]


    for answer in answers:
        translated_response = english_translator.translate(answer["response"])
        translated_ground_truth = indonesian_translator.translate(question["answer"])
        # evaluator without reference
        # eval_result_without_ref = evaluator_without_ref.evaluate_strings(
        #     prediction=translated_response,
        #     input=question['question'],
        # )
        # result_without_ref = dict(eval_result_without_ref)
        prompt=prompt_template.format(
            rubric=question['rubric'],
            question=question['question'],
            context=question['answer'],
            answer=translated_response
        )
        print("Prompt : ", prompt)
        llm_output = llm.invoke(prompt)
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

        print(llm_output)

        result = eval(llm_output)
        #
        # # remove the rating from the reasoning
        print("Raw : ", result)
        score = normalizer.normalize_score(question["rubric"], result['score'])
        reasoning = result['reasoning']
        translated_reasoning = GoogleTranslator(source='en', target='id').translate(result['reasoning'])
        print("Student Answer : ", answer["response"])
        print("Score : ", score)
        print("Reasoning : ", translated_reasoning)
        print("====================================")

        # Prepare result dictionaries
        result_english = {
            "no": answer["no"],
            "raw": result,
            "question": question['question'],
            "ground_truth": question["answer"],
            "answer": translated_response,
            "rubric": question["rubric"],
            "score": score,
            "key": question['key'],
            "reasoning": result['reasoning'],
        }

        result_id = {
            "no": answer["no"],
            "raw": result,
            "question": question_id['question'],
            "ground_truth": answer["response"],
            "answer": translated_ground_truth,
            "rubric": question_id["rubric"],
            "score": score,
            "key": question['key'],
            "reasoning": translated_reasoning
        }

        # Write results to file
        append_to_json("../assets/results/uas_llama_id.json", result_id)
        append_to_json("../assets/results/uas_llama_english.json", result_english)