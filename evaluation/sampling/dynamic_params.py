from sklearn.metrics import cohen_kappa_score
import numpy as np
import json

MODEL_NAME = "llama3-70b-8192"


# open scores_per_user.json
scores_per_user = []
with open('../assets/taken_data/scores_per_user_transformed.json') as f:
    scores_per_user = json.load(f)

rater1_scores = np.array(scores_per_user[0]["scores"])
rater2_scores = np.array(scores_per_user[1]["scores"])
rater3_scores = np.array(scores_per_user[2]["scores"])
rater4_scores = np.array(scores_per_user[3]["scores"])
rater5_scores = np.array(scores_per_user[4]["scores"])

# load model scores from assets/results/kuis_mistral_id.json and assets/results/uas_mistral_id.json

# open kuis_mistral_id.json
kuis_mistral_scores = []
kuis_mistral_no = []
with open('../assets/results/kuis_gemma_english_transformed.json') as f:
    kuis_mistral_scores = json.load(f)
#     get only scores
kuis_mistral_no = [x['no'] for x in kuis_mistral_scores]
kuis_mistral_scores = [x['score'] for x in kuis_mistral_scores]

# a = [1,2,3]
# b = [1,2,2]
# print(a == b)
# open uas_mistral_id.json
uas_mistral_scores = []
uas_mistral_no = []
with open('../assets/results/uas_gemma_english_transformed.json') as f:
    uas_mistral_scores = json.load(f)
#     get only scores
uas_mistral_no = [x['no'] for x in uas_mistral_scores]
uas_mistral_scores = [x['score'] for x in uas_mistral_scores]

# combine kuis_mistral_scores and uas_mistral_scores
mistral_scores = kuis_mistral_scores + uas_mistral_scores
mistral_no = kuis_mistral_no + uas_mistral_no
print(f'kuis_mistral_scores: {mistral_scores}')
print(f'kuis_mistral_no: {mistral_no}')

# answerrater 1 no
answer_rater1_no = [x['no'] for x in scores_per_user[0]["score_objs"]]
answer_rater2_no = [x['no'] for x in scores_per_user[1]["score_objs"]]
answer_rater3_no = [x['no'] for x in scores_per_user[2]["score_objs"]]
answer_rater4_no = [x['no'] for x in scores_per_user[3]["score_objs"]]
answer_rater5_no = [x['no'] for x in scores_per_user[4]["score_objs"]]

print(f'answer_rater1_no: {answer_rater1_no}')
print(f'answer_rater2_no: {answer_rater2_no}')
print(f'answer_rater3_no: {answer_rater3_no}')
print(f'answer_rater4_no: {answer_rater4_no}')
print(f'answer_rater5_no: {answer_rater5_no}')

# check if the no is the same
print(f'answer_rater1_no == mistral_no: {answer_rater1_no == mistral_no}')

mean_scores = np.mean([rater1_scores, rater2_scores, rater3_scores, rater4_scores, rater5_scores], axis=0)
rounded_mean_scores = np.round(mean_scores).astype(int).tolist()
print(f'rater1_scores: {rater1_scores.tolist()}')
print(f'rater2_scores: {rater2_scores.tolist()}')
print(f'rater3_scores: {rater3_scores.tolist()}')
print(f'rater4_scores: {rater4_scores.tolist()}')
print(f'rater5_scores: {rater5_scores.tolist()}')
print(f'rounded_mean_: {rounded_mean_scores}')
# rater1_scores = [1,1,1,1,1,1]
# rater2_scores = [1,2,2,2,2,1]
# rater3_scores = [1,3,3,3,3,1]
# rater4_scores = [1,4,4,4,4,1]
# rater5_scores = [1,1,1,1,1,1]


qwk_scores12 = cohen_kappa_score(rater1_scores, rater2_scores, weights='quadratic')
qwk_scores13 = cohen_kappa_score(rater1_scores, rater3_scores, weights='quadratic')
qwk_scores14 = cohen_kappa_score(rater1_scores, rater4_scores, weights='quadratic')
qwk_scores15 = cohen_kappa_score(rater1_scores, rater5_scores, weights='quadratic')
qwk_scores23 = cohen_kappa_score(rater2_scores, rater3_scores, weights='quadratic')
qwk_scores24 = cohen_kappa_score(rater2_scores, rater4_scores, weights='quadratic')
qwk_scores25 = cohen_kappa_score(rater2_scores, rater5_scores, weights='quadratic')
qwk_scores34 = cohen_kappa_score(rater3_scores, rater4_scores, weights='quadratic')
qwk_scores35 = cohen_kappa_score(rater3_scores, rater5_scores, weights='quadratic')
qwk_scores45 = cohen_kappa_score(rater4_scores, rater5_scores, weights='quadratic')

# qwk raters with mistral
qwk_scores_mistral1 = cohen_kappa_score(mistral_scores, rater1_scores, weights='quadratic')
qwk_scores_mistral2 = cohen_kappa_score(mistral_scores, rater2_scores, weights='quadratic')
qwk_scores_mistral3 = cohen_kappa_score(mistral_scores, rater3_scores, weights='quadratic')
qwk_scores_mistral4 = cohen_kappa_score(mistral_scores, rater4_scores, weights='quadratic')
qwk_scores_mistral5 = cohen_kappa_score(mistral_scores, rater5_scores, weights='quadratic')

print("========================================")
print(f'QWK model-rater1: {qwk_scores_mistral1}')
diff_mistral_rater1 = np.array(mistral_scores) - np.array(rater1_scores)

print(f'QWK model-rater2: {qwk_scores_mistral2}')
diff_mistral_rater2 = np.array(mistral_scores) - np.array(rater2_scores)

print(f'QWK model-rater3: {qwk_scores_mistral3}')
diff_mistral_rater3 = np.array(mistral_scores) - np.array(rater3_scores)

print(f'QWK model-rater4: {qwk_scores_mistral4}')
diff_mistral_rater4 = np.array(mistral_scores) - np.array(rater4_scores)

print(f'QWK model-rater5: {qwk_scores_mistral5}')
diff_mistral_rater5 = np.array(mistral_scores) - np.array(rater5_scores)
print("========================================")

print(f'diff mistral-rater1: {diff_mistral_rater1.tolist()}')
print(f'diff mistral-rater2: {diff_mistral_rater2.tolist()}')
print(f'diff mistral-rater3: {diff_mistral_rater3.tolist()}')
print(f'diff mistral-rater4: {diff_mistral_rater4.tolist()}')
print(f'diff mistral-rater5: {diff_mistral_rater5.tolist()}')

print("========================================")
print(f'QWK rater1-rater2: {qwk_scores12}')
print(f'QWK rater1-rater3: {qwk_scores13}')
print(f'QWK rater1-rater4: {qwk_scores14}')
print(f'QWK rater1-rater5: {qwk_scores15}')
print(f'QWK rater2-rater3: {qwk_scores23}')
print(f'QWK rater2-rater4: {qwk_scores24}')
print(f'QWK rater2-rater5: {qwk_scores25}')
print(f'QWK rater3-rater4: {qwk_scores34}')
print(f'QWK rater3-rater5: {qwk_scores35}')
print(f'QWK rater4-rater5: {qwk_scores45}')

# # Sample data
# llama2_scores = [1, 2, 3, 4, 5]
# mistral_scores = [1, 3, 3, 4, 5]
#
# rater1_scores = [1, 2, 4, 3, 5]
# rater2_scores = [2, 1, 3, 3, 4]
# rater3_scores = [3, 1, 3, 2, 5]
# rater4_scores = [2, 2, 2, 4, 5]
# rater5_scores = [5, 3, 4, 5, 5]
#
#
# def extend_array(arr, target_length):
#     repeat_times = target_length // len(arr)
#     extra_elements = target_length % len(arr)
#     extended_array = arr * repeat_times + arr[:extra_elements]
#     return np.array(extended_array)
#
#
# # Extending each array to have a length of 100
# llama2_scores = extend_array(llama2_scores, 2763)
# mistral_scores = extend_array(mistral_scores, 2763)
# rater1_scores = extend_array(rater1_scores, 2763)
# rater2_scores = extend_array(rater2_scores, 2763)
# rater3_scores = extend_array(rater3_scores, 2763)
# rater4_scores = extend_array(rater4_scores, 2763)
# rater5_scores = extend_array(rater5_scores, 2763)
#
# # Calculating the average human score
# human_scores = np.mean([rater1_scores, rater2_scores, rater3_scores, rater4_scores, rater5_scores], axis=0)
#
# rounded_human_scores = np.round(human_scores).astype(int).tolist()
# # Calculating QWK
# qwk_score_mistral = cohen_kappa_score(mistral_scores, rounded_human_scores, weights='quadratic')
# qwk_score_llama2 = cohen_kappa_score(llama2_scores, rounded_human_scores, weights='quadratic')
#
# print(f'Mistral - Quadratic Weighted Kappa: {qwk_score_mistral}')
# print(f'llama2 - Quadratic Weighted Kappa: {qwk_score_llama2}')
#
# # make data:
# height = [qwk_score_mistral, qwk_score_llama2]
# bars = ('Mistral', 'llama2')
# y_pos = np.arange(len(bars))
# # make plot
# plt.bar(y_pos, height)
# plt.xticks(y_pos, bars)
# plt.show()
