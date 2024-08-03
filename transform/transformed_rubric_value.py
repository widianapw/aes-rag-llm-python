import pandas as pd
import json

df_kuis_question = pd.read_json('../assets/kuis_question.json')
df_uas_question = pd.read_json('../assets/uas_question.json')

df_kuis_llama = pd.read_json('../assets/results/kuis_llama_english.json')
df_uas_llama = pd.read_json('../assets/results/uas_llama_english.json')


def transformToThreeRubric(score):
    if score == 5:
        return 3
    elif score == 3:
        return 2
    return score


transformed_kuis_llama = []
for index, row in df_kuis_llama.iterrows():
    question = df_kuis_question[df_kuis_question['key'] == row['key']]
    question = question.iloc[0]
    if question['is_three_rubric']:
        score = transformToThreeRubric(row['score'])
    else:
        score = row['score']
    raw = {
        "question": question['question'],
        "score": score,
        "reasoning": row['reasoning'],
    }
    transformed_kuis_llama.append({
        "no": row["no"],
        "raw": raw,
        "question": question['question'],
        "ground_truth": row["ground_truth"],
        "answer": row["answer"],
        "rubric": question["rubric"],
        "score": score,
        "key": row['key'],
        "reasoning": row['reasoning'],
    })

transformed_uas_llama = []
for index, row in df_uas_llama.iterrows():
    question = df_uas_question[df_uas_question['key'] == row['key']]
    question = question.iloc[0]
    if question['is_three_rubric'] == True:
        score = transformToThreeRubric(row['score'])
    else:
        score = row['score']
    raw = {
        "question": question['question'],
        "score": score,
        "reasoning": row['reasoning'],
    }
    transformed_uas_llama.append({
        "no": row["no"],
        "raw": raw,
        "question": question['question'],
        "ground_truth": row["ground_truth"],
        "answer": row["answer"],
        "rubric": question["rubric"],
        "score": score,
        "key": row['key'],
        "reasoning": row['reasoning'],
    })

print(transformed_kuis_llama)
json_object_kuis = json.dumps(transformed_kuis_llama, indent=4)
with open("../assets/results/kuis_llama_english_transformed.json", "w") as outfile:
    outfile.write(json_object_kuis)

json_object_uas = json.dumps(transformed_uas_llama, indent=4)
with open("../assets/results/uas_llama_english_transformed.json", "w") as outfile:
    outfile.write(json_object_uas)

df_scores_per_user = pd.read_json('../assets/taken_data/scores_per_user.json')

transformed_scores_per_user = []
for index, row in df_scores_per_user.iterrows():
    score_objs = row['score_objs']
    transformed_score_objs = []
    transformed_scores = []
    for score_obj in score_objs:
        if score_obj['subject'] == 'kuis':
            question = df_kuis_question[df_kuis_question['key'] == score_obj['key']]
        else:
            question = df_uas_question[df_uas_question['key'] == score_obj['key']]
        question = question.iloc[0]

        if question['is_three_rubric']:
            score = transformToThreeRubric(score_obj['score'])
        else:
            score = score_obj['score']

        item = {
            "question_id": score_obj['question_id'],
            "no": score_obj['no'],
            "key": score_obj['key'],
            "question": question['question'],
            "score": score,
            "subject": question['subject'],
        }
        transformed_scores.append(score)
        transformed_score_objs.append(item)

    transformed_scores_per_user.append({
        "user_id": row['user_id'],
        "score_objs": transformed_score_objs,
        "email": row['email'],
        "scores": transformed_scores,
    })


json_object_scores_per_user = json.dumps(transformed_scores_per_user, indent=4)
with open("../assets/taken_data/scores_per_user_transformed.json", "w") as outfile:
    outfile.write(json_object_scores_per_user)