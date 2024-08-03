import json
import numpy as np
from sklearn.metrics import cohen_kappa_score

NUM_OF_ANSWER_PER_QUESTION = 20


def calculate_qwk(rater_scores, model_scores):
    return cohen_kappa_score(rater_scores, model_scores, weights='quadratic')


# Generate for kuis
kuis_answers = []
with open("../assets/kuis.json", "r") as f:
    kuis = json.load(f)
    kuis_keys = list(set([kuis_item['key'] for kuis_item in kuis]))
    kuis_keys.sort()

    for kuis_key in kuis_keys:
        kuis_per_key = list(filter(lambda x: x['key'] == kuis_key, kuis))
        kuis_per_key = kuis_per_key[:NUM_OF_ANSWER_PER_QUESTION]
        kuis_answers.extend(kuis_per_key)

with open("../assets/sampling/kuis_answers.json", "w") as f:
    json.dump(kuis_answers, f, indent=4)

# Generate for uas
uas_answers = []
with open("../assets/uas.json", "r") as f:
    uas = json.load(f)
    uas_keys = list(set([uas_item['key'] for uas_item in uas]))
    uas_keys.sort()

    for uas_key in uas_keys:
        uas_per_key = list(filter(lambda x: x['key'] == uas_key, uas))
        uas_per_key = uas_per_key[:NUM_OF_ANSWER_PER_QUESTION]
        uas_answers.extend(uas_per_key)

with open("../assets/sampling/uas_answers.json", "w") as f:
    json.dump(uas_answers, f, indent=4)

# Generate for scores_per_user
score_per_users = []
with open("../assets/taken_data/scores_per_user.json", "r") as f:
    scores = json.load(f)
    for score in scores:
        item = {
            'user_id': score['user_id'],
            'email': score['email']
        }
        item_score_objs = score['score_objs']

        kuis_score_objs = list(filter(lambda x: x['subject'] == 'kuis', item_score_objs))
        new_kuis_score_objs = []

        for kuis_key in kuis_keys:
            kuis_per_key = list(filter(lambda x: x['key'] == kuis_key, kuis_score_objs))
            kuis_per_key = kuis_per_key[:NUM_OF_ANSWER_PER_QUESTION]
            new_kuis_score_objs.extend(kuis_per_key)

        uas_score_objs = list(filter(lambda x: x['subject'] == 'uas', item_score_objs))
        new_uas_score_objs = []
        for uas_key in uas_keys:
            uas_per_key = list(filter(lambda x: x['key'] == uas_key, uas_score_objs))
            uas_per_key = uas_per_key[:NUM_OF_ANSWER_PER_QUESTION]
            new_uas_score_objs.extend(uas_per_key)

        all_score_objs = new_kuis_score_objs + new_uas_score_objs
        item['score_objs'] = all_score_objs
        item['scores'] = [obj['score'] for obj in all_score_objs]  # Ensure scores are included

        score_per_users.append(item)

with open("../assets/sampling/scores_per_user.json", "w") as f:
    json.dump(score_per_users, f, indent=4)

# Calculate and print QWK scores per rater
raters_scores = [np.array(user["scores"]) for user in score_per_users[:5]]

# QWK Rater-Rater
qwk_rater_rater = {}
for i in range(len(raters_scores)):
    for j in range(i + 1, len(raters_scores)):
        qwk_rater_rater[f'Rater{i + 1}-Rater{j + 1}'] = calculate_qwk(raters_scores[i], raters_scores[j])

print("\nRater-Rater QWK Scores:")
for key, value in qwk_rater_rater.items():
    print(f'{key}: {value}')
