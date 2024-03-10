from langchain_community.llms import Ollama
import json
from langchain.evaluation import load_evaluator
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from translator import mistral_translator
from utils import normalizer

from deep_translator import GoogleTranslator

indonesian_translator = GoogleTranslator(target="id")

llm = Ollama(model="mistral", temperature=0.1)

questions = []
with open("../assets/kuis_with_answers_english.json", "r") as f:
    questions = json.load(f)
    # questions = filter(lambda x: x['key'] == 'response-6', questions)
    questions = list(questions)
    # questions = questions[:2]

questions_id = []
with open("../assets/kuis_question.json", "r") as f:
    questions_id = json.load(f)
    questions_id = list(questions_id)

results = []
results_english = []
for question in questions:

    question_id = list(filter(lambda x: x['key'] == question['key'], questions_id))[0]
    print("Question : ", question['question'])
    accuracy_criteria = {
        "accuracy": question["rubric"]
    }

    evaluator = load_evaluator(
        "labeled_score_string",
        criteria=accuracy_criteria,
        llm=llm
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
        answers = list(answers)
        answers = answers[:5]

    for answer in answers:
        translated_response = mistral_translator.translate_to_english(answer["response"])
        eval_result = evaluator.evaluate_strings(
            prediction=translated_response,
            reference=question["answer"],
            input=question['question'],
        )
        result = dict(eval_result)

        # remove the rating from the reasoning
        score = normalizer.normalize_score(question["rubric"], result['score'])
        print("Raw : ", result)
        try:
            result['reasoning'] = result['reasoning'].split("\n\n")[1]
        except:
            result['reasoning'] = result['reasoning'].split("\n")[1]

        reasoning = result['reasoning']
        translated_reasoning = GoogleTranslator(source='en', target='id').translate(result['reasoning'])
        print("Student Answer : ", answer["response"])
        print("Score : ", score)
        print("Reasoning : ", translated_reasoning)
        print("====================================")


        results_english.append({
            "no": answer["no"],
            "question": question['question'],
            "answer": translated_response,
            "rubric": question["rubric"],
            "score": score,
            "reasoning": reasoning
        })

        results.append({
            "no": answer["no"],
            "question": question_id['question'],
            "answer": answer["response"],
            "rubric": question_id["rubric"],
            "score": score,
            "reasoning": translated_reasoning
        })

# save to json file
json_object = json.dumps(results, indent=4)
with open("../assets/results/kuis_mistral_id.json", "w") as outfile:
    outfile.write(json_object)
    outfile.close()

json_object = json.dumps(results_english, indent=4)
with open("../assets/results/kuis_mistral_english.json", "w") as outfile:
    outfile.write(json_object)
    outfile.close()
