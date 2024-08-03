import pandas as pd
from sklearn.metrics import cohen_kappa_score

df = pd.read_json('../assets/results/uas_llama_english.json')
df.drop(['raw', 'ground_truth', 'rubric','reasoning','question'], axis=1, inplace=True)
df_user = pd.read_json('../assets/taken_data/scores_per_user.json')
user_ids = df_user['user_id'].unique()
keys = df['key'].unique()

for user_id in user_ids:
    print('=====================')
    print('user_id: ', user_id)
    print('=====================')
    df_user_id = df_user[df_user['user_id'] == user_id]['score_objs']
    df_user_id = df_user_id.apply(lambda x: [y for y in x if y['subject'] == 'uas'])
    for key in keys:
        print("KEY",key)
        filtered_df_user = df_user_id.apply(lambda x: [y for y in x if y['key'] == key])
    #     sort the list of dictionaries by no
        filtered_df_user = filtered_df_user.apply(lambda x: sorted(x, key=lambda y: y['no']))
        list_filtered_df_user = filtered_df_user.apply(lambda x: [y['score'] for y in x])
        list_filtered_df_user = [item for sublist in list_filtered_df_user for item in sublist]
        print("USER ANSWER",list_filtered_df_user)
        df_score = df[df['key'] == key]['score']
        print("MODEL ANSWER",df_score.tolist())
        print(cohen_kappa_score(df_score.tolist(), list_filtered_df_user, weights="quadratic"),)
        print('=====================')