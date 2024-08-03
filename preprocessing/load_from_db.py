import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tesis_scorer_laravel"
)

user_ids = [2, 3, 4, 5, 6]
users = [
    {
        "id": 2,
        "email": "ratna@tesis.com"
    },
    {
        "id": 3,
        "email": "juli@tesis.com",

    },
    {
        "id": 4,
        "email": "jena@tesis.com"
    },
    {
        "id": 5,
        "email": "cokin@tesis.com"
    },
    {
        "id": 6,
        "email": "friska@tesis.com"
    }
]

cursor = mydb.cursor()
scores_per_user = []

for user_id in user_ids:
    cursor.execute("""SELECT answer_scores.id, user_id,answer_id, score, answers.no, answers.question_id, questions.key, questions.subject_id
    FROM answer_scores 
    JOIN answers ON answer_scores.answer_id = answers.id
    JOIN questions ON answers.question_id = questions.id
    WHERE user_id = %s order by answer_id asc""",
                   (user_id,))
    user_scores = cursor.fetchall()

    temp_scores = []
    temp_answer_ids = []

    score_objs = []
    for user_score in user_scores:
        score = user_score[3]
        answer_id = user_score[2]
        temp_scores.append(score)
        temp_answer_ids.append(answer_id)
        score_objs.append({
            "question_id": user_score[5],
            "key": user_score[6],
            "no": user_score[4],
            "subject": "kuis" if user_score[7] == 1 else "uas",
            "score": score
        })

    scores_per_user.append({
        "user_id": user_id,
        "email": users[user_id - 2]["email"],  # user_id starts from 2
        "scores": temp_scores,
        "answer_ids": temp_answer_ids,
        "score_objs": score_objs
    })

print(scores_per_user)
# save to json file
with open('../assets/taken_data/scores_per_user.json', 'w') as f:
    # add indent=4 for pretty print
    json.dump(scores_per_user, f, indent=4)

# Path: preprocessing/load_from_db.py
