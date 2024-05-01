import pandas as pd
import re
import json

data = pd.read_excel("../assets/raw/uas.xlsx")
question_columns = [
    {
        "question": "Apa yang dimaksud dengan AI (Artificial Intelligence) dan sebutkan 3 (tiga) contohnya",
        "column": "Response 1",
        "key": "response-1",
        "rubric": """Skor 1: Jawaban tidak menjelaskan apa itu Kecerdasan Buatan (AI) dan tidak menyertakan contoh.
Skor 2: Jawaban menjelaskan Kecerdasan Buatan (AI) dan tidak menyertakan contoh apa pun.
Skor 3: Jawaban menjelaskan Kecerdasan Buatan (AI) dan menyertakan satu contoh yang relevan.
Skor 4: Jawaban menjelaskan Kecerdasan Buatan (AI) dan menyertakan dua contoh AI yang relevan.
Skor 5: Jawaban menjelaskan Kecerdasan Buatan (AI) dan menyertakan lebih dari dua contoh AI yang relevan."""
    },
    {
        "question": "Menurut Saudara, apakah pekerjaan Costumer Service dan pekerjaan yang sifat layanannya berulang, suatu saat akan dapat digantikan oleh mesin? Berikan alasan yang didasarkan pada konteks Transformasi Digital.",
        "column": "Response 2",
        "key": "response-2",
        "rubric": """Skor 1: Jawaban tidak membahas kemungkinan pekerjaan Customer Service digantikan oleh mesin dan tidak menyertakan alasan apa pun.
Skor 2: Jawaban menjawab kemungkinan pekerjaan Customer Service digantikan oleh mesin, tetapi tidak menyertakan alasan yang mendukung pendapat tersebut.
Skor 3: Jawaban menjawab kemungkinan pekerjaan Customer Service digantikan oleh mesin dan memberikan alasan yang umum, namun alasan yang diberikan tidak didasarkan pada konteks Transformasi Digital.
Skor 4: Jawaban menjawab kemungkinan pekerjaan Customer Service digantikan oleh mesin dan memberikan alasan yang sesuai dengan konteks tranformasi digital, tetapi tidak memberikan contoh atau aplikasi nyata.
Skor 5: Jawaban menjawab kemungkinan pekerjaan Customer Service digantikan oleh mesin dan memberikan alasan yang sesuai dengan konteks Transformasi Digital dan memberikan contoh atau aplikasi nyata."""
    },
    {
        "question": "Sebutkan 5 (lima) perbedaan utama dari sumber data tradisional dan sumber big data!",
        "column": "Response 3",
        "key": "response-3",
        "rubric": """Skor 1: Jawaban tidak menyertakan perbedaan antara sumber data tradisional dan sumber big data.
Skor 2: Jawaban menyertakan satu perbedaan antara sumber data tradisional dan sumber big data.
Skor 3: Jawaban menyertakan dua perbedaan antara sumber data tradisional dan sumber big data.
Skor 4: Jawaban menyertakan tiga perbedaan antara sumber data tradisional dan sumber big data.
Skor 5: Jawaban menyertakan lebih dari tiga perbedaan antara sumber data tradisional dan sumber big data."""
    },
    {
        "question": "Sebutkan 3 (tiga) perbedaan utama bentuk data yang terstruktur dan tidak terstruktur!",
        "column": "Response 4",
        "key": "response-4",
        "rubric": """Skor 1: Jawaban tidak menyertakan perbedaan antara data terstruktur dan data tidak terstruktur.
Skor 2: Jawaban memberikan perbedaan antara bentuk data yang terstruktur dan tidak terstruktur namun tidak relevan.
Skor 3: Jawaban memberikan satu perbedaan antara bentuk data yang terstruktur dan tidak terstruktur dengan benar.
Skor 4: Jawaban memberikan dua perbedaan antara bentuk data yang terstruktur dan tidak terstruktur dengan benar.
Skor 5: Jawaban memberikan tiga perbedaan antara bentuk data yang terstruktur dan tidak terstruktur dengan benar."""
    },
    {
        "question": "Jelaskan mengenai Sensor dalam Internet of Things (IoT) dan sebutkan 3 (tiga) contohnya!",
        "column": "Response 5",
        "key": "response-5",
        "rubric": """Skor 1: Jawaban tidak menjelaskan sensor dalam Internet of Things (IoT) dan tidak menyebutkan contohnya.
Skor 2: Jawaban menjelaskan sensor dalam Internet of Things (IoT) namun tidak menyebutkan contohnya.
Skor 3: Jawaban menjelaskan sensor dalam Internet of Things (IoT) dan menyebutkan satu contohnya.
Skor 4: Jawaban menjelaskan sensor dalam Internet of Things (IoT) dan menyebutkan dua contohnya.
Skor 5: Jawaban menjelaskan sensor dalam Internet of Things (IoT) dan menyebutkan tiga contohnya."""
    },
    {
        "question": "Jelaskan mengenai Actuator dalam Internet of Things (IoT) dan sebutkan 3 (tiga) contohnya!",
        "column": "Response 6",
        "key": "response-6",
        "rubric": """Skor 1: Jawaban tidak menjelaskan actuator dalam IoT dan tidak menyebutkan contohnya.
Skor 2: Jawaban menjelaskan actuator dalam IoT namun tidak menyebutkan contohnya.
Skor 3: Jawaban menjelaskan actuator dalam IoT dan menyebutkan satu contohnya.
Skor 4: Jawaban menjelaskan actuator dalam IoT dan menyebutkan dua contohnya.
Skor 5: Jawaban menjelaskan actuator dalam IoT dan menyebutkan tiga contohnya."""
    },
    {
        "question": "Jelaskan apa yang Saudara ketahui mengenai prediksi bahwa pekerjaan-pekerjaan yang ada pada saat ini akan berkurang di masa depan dan akan muncul jenis pekerjaan baru!. Sikap dan strategi kita menghadapi hal tersebut sebaiknya seperti apa?",
        "column": "Response 7",
        "key": "response-7",
        "rubric": """Skor 1: Jawaban tidak memberikan penjelasan mengenai prediksi pekerjaan yang akan berkurang dimasa depan dan tidak memberikan opini tentang strategi menghadapinya.
Skor 3: Jawaban memberikan penjelasan sangat singkat mengenai prediksi pekerjaan yang akan berkurang di masa depan namun tidak memberikan opini tentang strategi menghadapinya.
Skor 5: Jawaban memberikan penjelasan sangat singkat mengenai prediksi pekerjaan yang akan berkurang di masa depan namun dan memberikan opini tentang strategi menghadapinya."""
    },
    {
        "question": "Berikan contoh implementasi IoT pada Bidang Lingkungan dan Bidang Pertanian atau Perikanan atau Peternakan, berikan juga penjelasan yang memadai dari masing-masing contoh di atas.",
        "column": "Response 8",
        "key": "response-8",
        "rubric": """Skor 1: Jawaban tidak memberikan contoh implementasi IoT pada bidang lingkungan, pertanian, perikanan, atau peternakan.
Skor 2: Jawaban memberikan satu contoh implementasi IoT namun tanpa penjelasan cara kerja dan manfaat implementasi tersebut.
Skor 3: Jawaban memberikan satu contoh implementasi IoT pada salah satu bidang dengan penjelasan yang mencakup cara kerja implementasi tersebut namun tidak menjelaskan manfaat implementasi tersebut.
Skor 4: Jawaban memberikan satu contoh implementasi IoT pada salah satu bidang dengan penjelasan yang mencakup cara kerja dan manfaat implementasi tersebut.
Skor 5: Jawaban memberikan lebih dari satu contoh implementasi IoT pada lebih dari satu bidang (lingkungan, pertanian, perikanan, atau peternakan) dengan penjelasan yang mencakup cara kerja dan manfaat implementasi tersebut."""
    },
    {
        "question": "Sebutkan 5 (lima) kriteria suatu data disebut big data? dan jelaskan secara singkat dan memadai.",
        "column": "Response 9",
        "key": "response-9",
        "rubric": """Skor 1: Jawaban tidak ada menyebut salah satu dari lima kriteria big data.
Skor 2: Jawaban hanya menyebutkan satu kriteria dari big data secara singkat.
Skor 3: Jawaban menyebutkan dua kriteria dari big data secara singkat.
Skor 4: Jawaban menyebutkan tiga kriteria dari big data secara singkat.
Skor 5: Jawaban menyebutkan lebih dari tiga kriteria dari big data secara singkat."""
    }

]
df = pd.DataFrame(data, columns=["Email address", "id","Surname","Response 1", "Response 2", "Response 3", "Response 4", "Response 5",
                                 "Response 6", "Response 7", "Response 8", "Response 9"])


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
            print("Error on index ", index, " with response ", response)
            clean = ""
        # if response and response != "nan":
        #     print(response)
        #     clean = cleanResponse(response)
        # else:
        #     clean = ""

        items.append({
            "no": index + 1,
            "email": df["Email address"][index],
            "name": df["Surname"][index],
            "question": question["question"],
            "response": clean,
            "rubric": question["rubric"],
            "column": question["column"],
            "subject": "uas",
            "key": question["key"]
        })

# save to json file
json_object = json.dumps(items, indent=4)
with open("../assets/uas.json", "w") as outfile:
    outfile.write(json_object)
