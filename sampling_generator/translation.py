import pandas as pd
from deep_translator import GoogleTranslator

df_kuis_answers = pd.read_json('../assets/sampling/kuis_answers.json')
df_uas_answers = pd.read_json('../assets/sampling/uas_answers.json')
english_translator = GoogleTranslator(target="en")

def translate_to_english(text):
    return english_translator.translate(text)

kuis_answers = []
for _, row in df_kuis_answers.iterrows():
    kuis_answers.append({
        "no": row["no"],
        'subject': 'kuis',
        "key": row["key"],
        "answer": row["response"],
        "translated_answer": translate_to_english(row["response"])
    })

uas_answers = []
for _, row in df_uas_answers.iterrows():
    uas_answers.append({
        "no": row["no"],
        'subject': 'uas',
        "key": row["key"],
        "answer": row["response"],
        "translated_answer": translate_to_english(row["response"])
    })

merged_answers = kuis_answers + uas_answers
# save to excel
df_merged_answers = pd.DataFrame(merged_answers)
df_merged_answers.to_excel('../assets/sampling/translation.xlsx', index=False)