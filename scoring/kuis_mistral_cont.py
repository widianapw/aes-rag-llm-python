from langchain_community.llms import Ollama
import json
from langchain.evaluation import load_evaluator
from translator import mistral_translator
from utils import normalizer
from deep_translator import GoogleTranslator
import os

def get_current_max_no(key):
    try:
        with open("../assets/results/kuis_mistral_id.json", "r") as file:
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

llm = Ollama(model="mistral", temperature=0.1)

questions = []
with open("../assets/kuis_with_answers_english.json", "r") as f:
    questions = json.load(f)
    questions = filter(lambda x: x['key'] == 'response-3', questions)
    questions = list(questions)
    # questions = questions[:2]

questions_id = []
with open("../assets/kuis_question.json", "r") as f:
    questions_id = json.load(f)
    questions = filter(lambda x: x['key'] == 'response-3', questions)
    questions_id = list(questions_id)

for question in questions:
    current_max_no = get_current_max_no(question['key'])
    question_id = list(filter(lambda x: x['key'] == question['key'], questions_id))[0]
    print("Rubric : ", question['rubric'])
    print("Question : ", question['question'])
    accuracy_criteria = {
        "accuracy": question["rubric"]
    }

    evaluator = load_evaluator(
        "labeled_score_string",
        criteria=accuracy_criteria,
        llm=llm
    )

    evaluator_without_ref = load_evaluator(
        "score_string",
        criteria=accuracy_criteria,
        llm=llm,
    )

    # evaluator = LabeledScoreStringEvalChain.from_llm(
    #     llm=llm,
    #     criteria=accuracy_criteria,
    #     prompt=evaluator_prompt
    # )

    answers = []
    with open("../assets/kuis.json", "r") as f:
        answers = json.load(f)
        answers = filter(lambda x: x['key'] == question['key'] and x['subject'] == 'kuis', answers)
        answers = filter(lambda x: x['no'] > current_max_no, answers)
        answers = list(answers)
        answers = answers[:20]

    print(answers)

    for answer in answers:
        translated_response = mistral_translator.translate_to_english(answer["response"])
        translated_ground_truth = indonesian_translator.translate(question["answer"])
        # evaluator without reference
        # eval_result_without_ref = evaluator_without_ref.evaluate_strings(
        #     prediction=translated_response,
        #     input=question['question'],
        # )
        # result_without_ref = dict(eval_result_without_ref)



        print("Ground Truth : ", translated_ground_truth)
        print("Translated Response : ", translated_response)
        eval_result = evaluator.evaluate_strings(
            prediction=translated_response,
            reference=question["answer"],
            input=question['question'],
        )
        result = dict(eval_result)

        # remove the rating from the reasoning
        print("Raw : ", result)
        score = normalizer.normalize_score(question["rubric"], result['score'])
        try:
            result['reasoning'] = result['reasoning'].split("\n\n")[1]
        except Exception as e:
            result['reasoning'] = result['reasoning'].split("\n")[1]


        reasoning = result['reasoning']
        translated_reasoning = GoogleTranslator(source='en', target='id').translate(result['reasoning'])
        print("Student Answer : ", answer["response"])
        print("Score : ", score)
        print("Reasoning : ", translated_reasoning)
        print("====================================")

        # Prepare result dictionaries
        result_english = {
            "no": answer["no"],
            "raw": eval_result,
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
            "raw": eval_result,
            "question": question_id['question'],
            "ground_truth": answer["response"],
            "answer": translated_ground_truth,
            "rubric": question_id["rubric"],
            "score": score,
            "key": question['key'],
            "reasoning": translated_reasoning
        }

        # Write results to file
        append_to_json("../assets/results/kuis_mistral_id.json", result_id)
        append_to_json("../assets/results/kuis_mistral_english.json", result_english)