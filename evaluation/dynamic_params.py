import json
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

IS_FULL_DATA = False
MODEL_NAME = "llama3-70b-8192"
IS_COMPARE_WITH_METHOD = True
METHOD = "m1"

def get_paths():
    base_path = '../assets/taken_data/' if IS_FULL_DATA else '../assets/sampling/'
    result_path = f'../assets/results/' if IS_FULL_DATA else f'../assets/sampling/results/'
    paths = {
        "scores_per_user": base_path + 'scores_per_user.json',
        "transformed_scores_per_user": base_path + 'scores_per_user_transformed.json',
        "kuis_result": result_path + f'kuis_{MODEL_NAME}_english.json',
        "uas_result": result_path + f'uas_{MODEL_NAME}_english.json',
        "kuis_result_transformed": result_path + f'kuis_{MODEL_NAME}_english_transformed.json',
        "uas_result_transformed": result_path + f'uas_{MODEL_NAME}_english_transformed.json',
        "method_kuis_result": result_path + f'{METHOD}kuis_{MODEL_NAME}_english.json',
        "method_uas_result": result_path + f'{METHOD}uas_{MODEL_NAME}_english.json',
        "method_kuis_result_transformed": result_path + f'{METHOD}kuis_{MODEL_NAME}_english_transformed.json',
        "method_uas_result_transformed": result_path + f'{METHOD}uas_{MODEL_NAME}_english_transformed.json'
    }
    return paths

paths = get_paths()

df_kuis_question = pd.read_json('../assets/kuis_question.json')
df_uas_question = pd.read_json('../assets/uas_question.json')
df_kuis = pd.read_json(paths["kuis_result"])
df_uas = pd.read_json(paths["uas_result"])

def transform_to_three_rubric(score):
    return {5: 3, 3: 2}.get(score, score)

def transform_scores(df, question_df):
    transformed_scores = []
    for _, row in df.iterrows():
        question = question_df.loc[question_df['key'] == row['key']].iloc[0]
        score = transform_to_three_rubric(row['score']) if question['is_three_rubric'] else row['score']
        transformed_scores.append({
            "no": row["no"],
            "raw": {"question": question['question'], "score": score, "reasoning": row['reasoning']},
            "question": question['question'],
            "ground_truth": row["ground_truth"],
            "answer": row["answer"],
            "rubric": question["rubric"],
            "score": score,
            "key": row['key'],
            "reasoning": row['reasoning'],
        })
    return transformed_scores

transformed_kuis_model = transform_scores(df_kuis, df_kuis_question)
transformed_uas_model = transform_scores(df_uas, df_uas_question)

with open(paths["kuis_result_transformed"], "w") as outfile:
    json.dump(transformed_kuis_model, outfile, indent=4)

with open(paths["uas_result_transformed"], "w") as outfile:
    json.dump(transformed_uas_model, outfile, indent=4)

df_scores_per_user = pd.read_json(paths["scores_per_user"])

def transform_scores_per_user(df, kuis_questions, uas_questions):
    transformed_users = []
    for _, row in df.iterrows():
        transformed_score_objs = []
        for score_obj in row['score_objs']:
            question_df = kuis_questions if score_obj['subject'] == 'kuis' else uas_questions
            question = question_df.loc[question_df['key'] == score_obj['key']].iloc[0]
            score = transform_to_three_rubric(score_obj['score']) if question['is_three_rubric'] else score_obj['score']
            transformed_score_objs.append({
                "question_id": score_obj['question_id'],
                "no": score_obj['no'],
                "key": score_obj['key'],
                "question": question['question'],
                "score": score,
                "subject": question['subject'],
            })
        transformed_users.append({
            "user_id": row['user_id'],
            "score_objs": transformed_score_objs,
            "email": row['email'],
            "scores": [obj['score'] for obj in transformed_score_objs],
        })
    return transformed_users

transformed_scores_per_user = transform_scores_per_user(df_scores_per_user, df_kuis_question, df_uas_question)

with open(paths["transformed_scores_per_user"], "w") as outfile:
    json.dump(transformed_scores_per_user, outfile, indent=4)

def calculate_qwk(rater_scores, model_scores):
    return cohen_kappa_score(rater_scores, model_scores, weights='quadratic')

with open(paths["transformed_scores_per_user"]) as f:
    scores_per_user = json.load(f)

raters_scores = [np.array(user["scores"]) for user in scores_per_user[:5]]

with open(paths["kuis_result_transformed"]) as f:
    kuis_model_scores = [x['score'] for x in json.load(f)]

with open(paths["uas_result_transformed"]) as f:
    uas_model_scores = [x['score'] for x in json.load(f)]

model_scores = kuis_model_scores + uas_model_scores
mean_scores = np.mean(raters_scores, axis=0)
rounded_mean_scores = np.round(mean_scores).astype(int)

# Rater-Rater QWK calculation
qwk_rater_rater = {}
for i in range(len(raters_scores)):
    for j in range(i + 1, len(raters_scores)):
        qwk_rater_rater[f'Rater{i+1}-Rater{j+1}'] = calculate_qwk(raters_scores[i], raters_scores[j])

# Model-Rater QWK calculation
qwk_model_rater = {}
for i in range(len(raters_scores)):
    qwk_model_rater[f'Model-Rater{i+1}'] = calculate_qwk(model_scores, raters_scores[i])

# Method-Rater QWK calculation (if applicable)
if IS_COMPARE_WITH_METHOD:
    df_method_kuis = pd.read_json(paths["method_kuis_result"])
    df_method_uas = pd.read_json(paths["method_uas_result"])
    transformed_method_kuis = transform_scores(df_method_kuis, df_kuis_question)
    transformed_method_uas = transform_scores(df_method_uas, df_uas_question)

    with open(paths["method_kuis_result_transformed"], "w") as outfile:
        json.dump(transformed_method_kuis, outfile, indent=4)

    with open(paths["method_uas_result_transformed"], "w") as outfile:
        json.dump(transformed_method_uas, outfile, indent=4)

    method_scores = [x['score'] for x in transformed_method_kuis + transformed_method_uas]

    qwk_method_rater = {}
    for i in range(len(raters_scores)):
        qwk_method_rater[f'Method-Rater{i+1}'] = calculate_qwk(method_scores, raters_scores[i])

# Print results
print("Quadratic Weighted Kappa Scores:")
print("\nRater-Rater QWK Scores:")
for key, value in qwk_rater_rater.items():
    print(f'{key}: {value}')

print("\nModel-Rater QWK Scores:")
for key, value in qwk_model_rater.items():
    print(f'{key}: {value}')

if IS_COMPARE_WITH_METHOD:
    print("\nMethod-Rater QWK Scores:")
    for key, value in qwk_method_rater.items():
        print(f'{key}: {value}')
