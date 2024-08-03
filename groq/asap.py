import pandas as pd
from sklearn.metrics import cohen_kappa_score

df = pd.read_excel('../assets/asap/essay_set.xlsx')

# drop nan values in rater1_domain1 and rater2_domain1
df = df.dropna(subset=['rater1_domain1', 'rater2_domain1'])

rater1_scores = df['rater1_domain1']
rater2_scores = df['rater2_domain1']


print(cohen_kappa_score(rater1_scores, rater2_scores))
