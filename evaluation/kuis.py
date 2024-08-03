import pandas as pd
from sklearn.metrics import cohen_kappa_score

df = pd.read_json('../assets/results/kuis_llama_english_transformed.json')
df.drop(['raw', 'ground_truth', 'rubric','reasoning','question'], axis=1, inplace=True)

df_user = pd.read_json('../assets/taken_data/scores_per_user_transformed.json')

user_ids = df_user['user_id'].unique()

for user_id in user_ids:
    print('=====================')
    print('user_id: ', user_id)
    print('=====================')
    filtered_df_user = df_user[df_user['user_id'] == user_id]['score_objs']
    filtered_df_user = filtered_df_user.apply(lambda x: [y for y in x if y['subject'] == 'kuis'])
    list_filtered_df_user = filtered_df_user.apply(lambda x: [y['score'] for y in x])
    # flatten the list
    list_filtered_df_user = [item for sublist in list_filtered_df_user for item in sublist]
    print('=====================')
    # print(f'filtered_df_score: {df["score"].tolist()}')
    print(cohen_kappa_score(df['score'].tolist(), list_filtered_df_user))

