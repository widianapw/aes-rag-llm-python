import pandas as pd
from sklearn.metrics import cohen_kappa_score
import numpy as np

THRESHOLD = 0.2

print('++++++++++++++++++++++++++++++++++++')
print('=====================================')
print("KUIS")
print('=====================================')
print('++++++++++++++++++++++++++++++++++++')

df = pd.read_json('../assets/results/kuis_gemma_english_transformed.json')
df.drop(['raw', 'ground_truth', 'rubric','reasoning','question'], axis=1, inplace=True)

df_user = pd.read_json('../assets/taken_data/scores_per_user_transformed.json')
df_user = pd.DataFrame(df_user)

# get user_id
user_ids = df_user['user_id'].unique()

# get unique value of key
keys = df['key'].unique()


kuis_results = []
for key in keys:
    filtered_df = df[df['key'] == key]
    for user_id in user_ids:
        filtered_df_user = df_user[df_user['user_id'] == user_id]['score_objs']
#         filter where subject is "kuis" and key is key
        filtered_df_user_score = filtered_df_user.apply(lambda x: [y['score'] for y in x])
        filtered_df_score = filtered_df['score']
        filtered_df_user = filtered_df_user.apply(lambda x: [y for y in x if y['subject'] == 'kuis' and y['key'] == key])
        list_filtered_df_user = filtered_df_user.apply(lambda x: [y['score'] for y in x])
        # flatten the list
        filtered_df_user_score_flat = [item for sublist in list_filtered_df_user for item in sublist]

        # print("filtered_df_score: ", filtered_df_user_score_flat)
        kuis_results.append({
            "key": key,
            "user_id": user_id,
            "cohen_kappa_score": cohen_kappa_score(filtered_df_score.tolist(), filtered_df_user_score_flat, weights="quadratic")
        })

        # print('=====================')
        # print(f'key: {key}')
        # print('user_id: ', user_id)
        # print(f'filtered_df_score: {filtered_df_score.tolist()}')
        # print(f'filtered_df_user_score: {filtered_df_user_score_flat}')
        # print(f'cohen kappa score: {cohen_kappa_score(filtered_df_score.tolist(), filtered_df_user_score_flat, weights="quadratic")}')
        # print('=====================')

# kuis results filter where cohen_kappa_score is less than threshold
kuis_results_filtered = list(filter(lambda x: x['cohen_kappa_score'] < THRESHOLD, kuis_results))
# sort by cohen_kappa_score
kuis_results_filtered = sorted(kuis_results_filtered, key=lambda x: x['cohen_kappa_score'])

df_mock = pd.DataFrame(kuis_results_filtered)
# Group by the 'key' column and count the occurrences of each unique key
grouped_df = df_mock.groupby('key').size().reset_index(name='count')

# Convert the grouped DataFrame to a list of dictionaries
grouped_list = grouped_df.to_dict(orient='records')
for result in grouped_list:
    print(result)

print('+++++++++++++++++++++++++++++++++++++')
print('=====================================')
print("UAS")
print('=====================================')
print('+++++++++++++++++++++++++++++++++++++')

df_uas = pd.read_json('../assets/results/uas_gemma_english_transformed.json')
df_uas.drop(['raw', 'ground_truth', 'rubric','reasoning','question'], axis=1, inplace=True)

keys= df_uas['key'].unique()

uas_results = []

for key in keys:
    filtered_df = df_uas[df_uas['key'] == key]
    for user_id in user_ids:
        filtered_df_user = df_user[df_user['user_id'] == user_id]['score_objs']
#         filter where subject is "kuis" and key is key
        filtered_df_user_score = filtered_df_user.apply(lambda x: [y['score'] for y in x])
        filtered_df_score = filtered_df['score']
        filtered_df_user = filtered_df_user.apply(lambda x: [y for y in x if y['subject'] == 'uas' and y['key'] == key])
        list_filtered_df_user = filtered_df_user.apply(lambda x: [y['score'] for y in x])
        # flatten the list

        filtered_df_user_score_flat = [item for sublist in list_filtered_df_user for item in sublist]

        uas_results.append({
            "key": key,
            "user_id": user_id,
            "cohen_kappa_score": cohen_kappa_score(filtered_df_score.tolist(), filtered_df_user_score_flat, weights="quadratic")
        })
        # print('=====================')
        # print(f'key: {key}')
        # print('user_id: ', user_id)
        # print(f'filtered_df_score: {filtered_df_score.tolist()}')
        # print(f'filtered_df_user_score: {filtered_df_user_score_flat}')
        # print(f'cohen kappa score: {cohen_kappa_score(filtered_df_score.tolist(), filtered_df_user_score_flat, weights="quadratic")}')
        # print('=====================')

# uas results filter where cohen_kappa_score is less than threshold
uas_results_filtered = list(filter(lambda x: x['cohen_kappa_score'] < THRESHOLD, uas_results))
# sort by cohen_kappa_score
uas_results_filtered = sorted(uas_results_filtered, key=lambda x: x['cohen_kappa_score'])
df_mock = pd.DataFrame(uas_results_filtered)

# Group by the 'key' column and count the occurrences of each unique key
grouped_df = df_mock.groupby('key').size().reset_index(name='count')

# Convert the grouped DataFrame to a list of dictionaries
grouped_list = grouped_df.to_dict(orient='records')
for result in grouped_list:
    print(result)