import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Load data
df = pd.read_json('../assets/results/uas_llama_8b_english_transformed.json')
df.drop(['raw', 'ground_truth', 'rubric', 'question'], axis=1, inplace=True)
df_user = pd.read_json('../assets/taken_data/scores_per_user.json')

# Define user IDs and keys to process
user_ids = [3]
keys = ['response-1', 'response-2', 'response-3', 'response-4', 'response-5', 'response-6', 'response-7', 'response-8',
        'response-9']

data_to_excel = []

# Process each user and key
for user_id in user_ids:
    print(f'=====================\nuser_id: {user_id}\n=====================')
    df_user_id = df_user[df_user['user_id'] == user_id]['score_objs']
    df_user_id = df_user_id.apply(lambda x: [y for y in x if y['subject'] == 'uas'])
    for key in keys:
        print("KEY", key)
        filtered_df_user = df_user_id.apply(lambda x: [y for y in x if y['key'] == key])
        filtered_df_user = filtered_df_user.apply(lambda x: sorted(x, key=lambda y: y['no']))
        list_filtered_df_user = filtered_df_user.apply(lambda x: [y['score'] for y in x])
        list_filtered_df_user = [item for sublist in list_filtered_df_user for item in sublist]

        print("USER ANSWER", list_filtered_df_user)

        df_key = df[df['key'] == key]
        df_score = df_key['score'].tolist()

        print("MODEL ANSWER", df_score)
        if len(df_score) != len(list_filtered_df_user):
            print(f"Warning: Mismatch in lengths for user {user_id} and key {key}.")
            continue

        qwk_score = cohen_kappa_score(df_score, list_filtered_df_user, weights="quadratic")
        print("QWK", qwk_score)
        print('=====================')

        # Add data for each item in the current key
        for i in range(len(df_score)):
            data_to_excel.append({
                'user_id': user_id,
                'key': key,
                'no': i + 1,
                'answer': df_key['answer'].tolist()[i],
                'user_score': list_filtered_df_user[i],
                'model_score': df_score[i],
                "reasoning": df_key['reasoning'].tolist()[i],
                "agreement": "Agree" if list_filtered_df_user[i] == df_score[i] else "Open"
            })

# Save the results to an Excel file
df_to_excel = pd.DataFrame(data_to_excel)
df_to_excel.to_excel('../assets/agreement/ratna_uas_llama_8b_agreement.xlsx', index=False)
