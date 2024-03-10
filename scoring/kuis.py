from langchain_community.llms import Ollama
import json
from langchain.evaluation import load_evaluator
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from translator import mistral_translator

from deep_translator import GoogleTranslator

llm = Ollama(model="mistral", temperature=0.1)

questions = []
with open("../assets/kuis_with_answers_english.json", "r") as f:
    questions = json.load(f)
    # questions = filter(lambda x: x['key'] == 'response-1', questions)
    questions = list(questions)
    # questions = questions[:2]

results = []
for question in questions:
    accuracy_criteria = {
        "accuracy": question["rubric"]
    }
    evaluator = load_evaluator(
        "labeled_score_string",
        criteria=accuracy_criteria,
        llm=llm
    )

    evaluator_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            (
                "human",
                "[Instruction]\nPlease act as an impartial judge \
    and evaluate the quality of the response provided by an AI \
    assistant to the user question displayed below. {criteria}"
                '[Ground truth]\n{reference}\nBegin your evaluation \
    by providing a short explanation. Be as objective as possible. \
    After providing your explanation, you must rate the response on a scale of 1 to 10 \
    by strictly following this format: "[[rating]]", for example: "Rating: [[5]]".\n\n\
    [Question]\n{input}\n\n[The Start of Assistant\'s Answer]\n{prediction}\n\
    [The End of Assistant\'s Answer]',
            ),
        ]
    )

    # evaluator_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", "Anda adalah asisten yang membantu."),
    #         (
    #             "human",
    #             "[Instruction]\nSilakan bertindak sebagai hakim yang tidak memihak \
    #     dan menilai kualitas respons yang diberikan oleh asisten AI \
    #     kepada pertanyaan pengguna yang ditampilkan di bawah ini. {criteria}"
    #             '[Ground truth]\n{reference}\nMulai evaluasi Anda \
    #             dengan memberikan penjelasan singkat. Jadilah seobjektif mungkin. \
    #             Setelah memberikan penjelasan Anda, Anda harus memberikan nilai pada respons dengan skala 1 sampai 10 \
    #             dengan ketat mengikuti format ini: "[[rating]]", contohnya: "Rating: [[5]]".\n\n\
    #             [Question]\n{input}\n\n[The Start of Assistant\'s Answer]\n{prediction}\n\
    #             [The End of Assistant\'s Answer]',
    #         ),
    #     ]
    # )


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
        answers = answers[:10]

    for answer in answers:
        # used_question = "Sebutkan dan jelaskan mengenai karakteristik 'Veracity' dan 'Value' pada Big Data!"
        # print("Question : ", used_question)
        translated_response = mistral_translator.translate_to_english(answer["response"])
        eval_result = evaluator.evaluate_strings(
            prediction=translated_response,
            reference=question["answer"],
            input=question['question'],
        )
        # eval result data = {'reasoning': 'Rating: [[4]]\n\nThe response provided by the AI assistant is accurate and provides a clear explanation of the two concepts, Veracity and Value, in relation to Big Data. However, the response only explains one of the concepts in detail while briefly mentioning the other concept. The response could have been improved by providing more detailed explanations for both concepts or by providing examples to illustrate how these concepts are applied in practice.', 'score': 4}
        result = dict(eval_result)
        # print(result)
        # reasoning = "Rating: [[3]]\n\nThe assistant has provided a brief explanation of the two concepts, Veracity and Value, but it is not clear how these concepts relate to the question about additional characteristics of Big Data beyond Variety, Velocity, and Volume."

        # remove the rating from the reasoning
        result['reasoning'] = result['reasoning'].split("\n\n")[1]
        translated_reasoning = GoogleTranslator(source='en', target='id').translate(result['reasoning'])
        print("Student Answer : ", answer["response"])
        print("Score : ", result['score'])
        # translated_reasoning = mistral_translator.translate_to_indonesia(result['reasoning'])
        print("Reasoning : ", translated_reasoning)
        print("====================================")
        # results.append({
        #     "no": answer["no"],
        #     "question": used_question,
        #     "answer": answer["response"],
        #     "rubric": question["rubric"],
        #     "score": result["score"],
        #     "reasoning": result["reasoning"]
        # })

# save to json file
# json_object = json.dumps(results, indent=4)
# with open("../assets/results/kuis_mistral.json", "w") as outfile:
#     outfile.write(json_object)
#     outfile.close()
