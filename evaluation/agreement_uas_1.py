import pandas as pd
from sklearn.metrics import cohen_kappa_score

df = pd.read_excel('../assets/agreement/ratna_uas_1.xlsx')

# iterate over the rows
agreement = []
for index, row in df.iterrows():
    score = row['user_score']
    if row['Agreement'] == 'Agree':
        score = row['model_score']
    agreement.append({
        "no": row["no"],
        "score": score,
        "user_id": row["user_id"],
    })

# load uas 1 scores
df_uas_1 = pd.read_json('../assets/results/uas_llama_english_1.json')

print(df_uas_1['score'].tolist())
print([x['score'] for x in agreement])
print('cohen_kappa_score', cohen_kappa_score(df_uas_1['score'].tolist(), [x['score'] for x in agreement], weights="quadratic"),)


