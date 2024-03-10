import pandas as pd
import re
import json

data = pd.read_excel("../assets/raw/kuis.xlsx")
question_columns = [
    {
        "question": "Pada modul telah dijelaskan mengenai 3 ciri Big Data yaitu Variety, Velocity, dan Volume. Sebutkan dan jelaskan 2V selain yang telah dijelaskan pada modul.",
        "column": "Response 1",
        "key": "response-1",
        "rubric": """Skor 1: Jawaban tidak menyebutkan 'Veracity' maupun 'Value' atau jawaban yang diberikan tidak memiliki kaitan dengan konsep Big Data.
Skor 2: Jawaban menyebutkan salah satu dari 'Veracity' atau 'Value' tanpa penjelasan yang relevan.
Skor 3: Jawaban menyebutkan kedua istilah 'Veracity' dan 'Value', namun tanpa memberikan penjelasan yang relevan terhadap kedua istilah tersebut.
Skor 4: Jawaban menyebutkan kedua istilah 'Veracity' dan 'Value'. Penjelasan diberikan untuk salah satu istilah tersebut dengan relevan, namun istilah kedua tidak dijelaskan.
Skor 5: Jawaban menyebutkan dan memberikan penjelasan yang relevan untuk kedua konsep 'Veracity' dan 'Value'."""
    },
    {
        "question": "Berikan contoh implementasi Big Data di bidang masing-masing selain yang disebutkan di modul.",
        "column": "Response 2",
        "key": "response-2",
        "rubric": """Skor 1: Jawaban tidak ada menyertakan contoh implementasi Big Data yang relevan.
Skor 2: Jawaban menyertakan hanya satu contoh implementasi Big Data yang relevan.
Skor 3: Jawaban menyertakan dua contoh implementasi Big Data yang relevan.
Skor 4: Jawaban menyertakan tiga contoh implementasi Big Data yang relevan.
Skor 5: Jawaban menyertakan lebih dari tiga contoh implementasi Big Data yang relevan."""
    },
    {
        "question": "Sebutkan dan jelaskan secara singkat ciri-ciri kumpulan data disebut Big Data",
        "column": "Response 3",
        "key": "response-3",
        "rubric": """Skor 1: Jawaban tidak menyebutkan ciri-ciri Big Data.
Skor 2: Jawaban menyebutkan dan menjelaskan satu ciri Big Data secara singkat. 
Skor 3: Jawaban menyebutkan dan menjelaskan dua ciri Big Data secara singkat.
Skor 4: Jawaban menyebutkan dan menjelaskan tiga ciri Big Data secara singkat.
Skor 5: Jawaban menyebutkan dan menjelaskan lebih dari tiga ciri Big Data secara singkat."""
    },
    {
        "question": "Apa yang dimaksud dengan ciri velocity?",
        "column": "Response 4",
        "key": "response-4",
        "rubric": """Skor 1: Jawaban tidak menyebutkan velocity.
Skor 3: Jawaban menyebutkan velocity namun penjelasan tidak relevan.
Skor 5: Jawaban menyebutkan dan menjelaskan velocity dengan relevan."""
    },
    {
        "question": "Apa perbedaan database relational dan data warehouse?",
        "column": "Response 5",
        "key": "response-5",
        "rubric": """Skor 1: Jawaban tidak menyebutkan perbedaan antara database relasional dan data warehouse.
Skor 3: Jawaban menyebutkan satu perbedaan antara database relasional dan data warehouse dengan penjelasan yang relevan.
Skor 5: Jawaban menyebutkan dua atau lebih perbedaan antara database relasional dan data warehouse dengan penjelasan yang benar dan singkat."""
    },
    {
        "question": "Apa tantangan-tantangan yang ada ketika mengimplementasikan Big Data?",
        "column": "Response 6",
        "key": "response-6",
        "rubric": """Skor 1: Jawaban tidak menyebutkan tantangan dalam mengimplementasikan Big Data.
Skor 3: Jawaban menyebutkan satu tantangan dalam mengimplementasikan big data.
Skor 5: Jawaban menyebutkan lebih dari satu tantangan dalam mengimplementasikan big data."""
    }
]
df = pd.DataFrame(data, columns=["Surname", "Email address", "Response 1", "Response 2", "Response 3", "Response 4",
                                 "Response 5", "Response 6"])


def cleanResponse(text):
    text = text.replace("\n", " ").strip()
    # remove extra spaces or tabs
    text = re.sub(r'\s+', ' ', text)
    # remove specialcase except , . / :
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\:\-]', '', text)
    # remove multiple dot (.), set to single dot
    text = re.sub(r'\.{2,}', '.', text)
    # remove multiple comma (,), set to single comma
    # trim leading and trailing whitespace
    text = text.strip()
    return text


items = []
for question in question_columns:
    print(question["question"])
    for index, response in enumerate(df[question["column"]]):
        clean = response
        try:
            clean = cleanResponse(response)
        except:
            clean = ""
        items.append({
            "no": index + 1,
            "email": df["Email address"][index],
            "name": df["Surname"][index],
            "question": question["question"],
            "response": clean,
            "rubric": question["rubric"],
            "column": question["column"],
            "subject": "kuis",
            "key": question["key"]
        })

# save to json file
json_object = json.dumps(items, indent=4)
with open("../assets/kuis.json", "w") as outfile:
    outfile.write(json_object)
