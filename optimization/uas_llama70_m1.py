import json
from deep_translator import GoogleTranslator
from method1 import Method1
import os

def get_current_max_no(key):
    try:
        with open("../assets/results/uas_llama70_m1_id.json", "r") as file:
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

        method1 = Method1(
            temperature=0,
            groq_api_key="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",
            model_name="llama3-8b-8192"
        )
        print("Question : ", question['question'])
        print("Rubric : ", question['rubric'])
        print("Ground Truth : ", question['answer'])
        print("Student Answer : ", translated_response)
        print("====================================")
        response = method1.evaluate(
            rubric=question['rubric'],
            question=question['question'],
            context=question['answer'],
            student_answer=translated_response
        )

        # remove the rating from the reasoning
        score = response['rubric_score']
        reasoning = response['reason']
        translated_reasoning = GoogleTranslator(source='en', target='id').translate(response['reason'])
        print("Student Answer : ", translated_response)
        print("Score : ", score)
        print("Reasoning : ", translated_reasoning)
        print("====================================")

        # Prepare result dictionaries
        result_english = {
            "no": answer["no"],
            "raw": response,
            "question": question['question'],
            "ground_truth": question["answer"],
            "answer": translated_response,
            "rubric": question["rubric"],
            "score": score,
            "key": question['key'],
            "reasoning": response['reason'],
        }

        result_id = {
            "no": answer["no"],
            "raw": response,
            "question": question_id['question'],
            "ground_truth": question["answer"],
            "answer": answer["response"],
            "rubric": question_id["rubric"],
            "score": score,
            "key": question['key'],
            "reasoning": translated_reasoning
        }

        # Write results to file
        append_to_json("../assets/results/uas_llama70_m1_id.json", result_id)
        append_to_json("../assets/results/uas_llama70_m1_english.json", result_english)