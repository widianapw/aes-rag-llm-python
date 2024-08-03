from method1 import Method1

method1 = Method1(
    temperature=0,
    groq_api_key="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",
    model_name="llama3-8b-8192"
)

# method_1_result = method1.evaluate(
#     rubric="""Score 1: Answer does not explain what Artificial Intelligence (AI) is and does not include examples.
# Score 2: Answer describes Artificial Intelligence (AI) and does not include any examples.
# Score 3: Answer explains Artificial Intelligence (AI) and only include one example of AI.
# Score 4: The answer explains Artificial Intelligence (AI) and includes two examples of AI.
# Score 5: The answer describes Artificial Intelligence (AI) and includes more than two examples of AI.""",
#     question="What is meant by AI (Artificial Intelligence) and name 3 (three) examples",
#     student_answer="Artificial Intelligence is an artificial intelligence system which is created as a simulation of human intelligence which is processed or executed by a machine, especially a computer system. Examples of AI: Autonomous Car, Chatbot, and Recommendation System",
#     context="""Artificial Intelligence (AI) refers to a branch of computer science that creates systems capable of performing tasks requiring human intelligence, such as language comprehension, learning, reasoning, and perception. Three examples of AI applications are: 1. Voice Recognition: Systems like Siri, Alexa, and Google Assistant that interpret and respond to voice commands. 2. Computer Vision: Technology allowing computers to "see" and interpret visual content, such as facial recognition or autonomous vehicle systems. 3. Natural Language Processing (NLP): Machines understanding and interacting with human language, used in chatbots, translators, and semantic search""",
# )

print("=============================================================")
# uas_2_result = method1.evaluate(
#     rubric="""Score 1: The answer does not include the difference between traditional data sources and big data sources.
# Score 2: Answer includes one difference between traditional data sources and big data sources.
# Score 3: Answer includes two differences between traditional data sources and big data sources.
# Score 4: Answer includes three differences between traditional data sources and big data sources.
# Score 5: Answer includes more than three differences between traditional data sources and big data sources.""",
#     question="Mention 5 (five) main differences between traditional data sources and big data sources!",
#     student_answer="A collection of structured data The size or volume of data is very small The existing data is centralized Easy to manipulate Traditional databases are sufficient for processing and storing data. Big Data: Is a collection of unstructured and semi-structured data The size or volume of data is large larger than traditional data Existing data is distributed Difficult to manipulate Requires special tools or tools to process and store data",
#     context="1. Value: Traditional data sources have clear value directly related to business operations, while big data sources require sophisticated analytical tools and data science techniques to uncover complex insights. 2. Complexity: Traditional data sources are relatively easier to manage due to their homogeneity and defined structure, whereas big data sources are complex due to high volume, variability, and velocity. 3. Technology Required: Traditional data can be managed with traditional IT systems, while big data requires new technologies like Hadoop, NoSQL databases, and real-time data processing platforms. 4. Data Volume: Traditional data is usually smaller in size and can be processed using conventional methods, whereas big data involves dealing with extremely large volumes of data. 5. Real-time Processing: Traditional data processing is often batch-oriented, while big data requires real-time or near real-time processing to gain value from the data."
# )

#
# print("=============================================================")
# uas_3_result = method1.evaluate(
#     rubric="""Score 1: The answer does not include the difference between traditional data sources and big data sources.
# Score 2: Answer includes one difference between traditional data sources and big data sources.
# Score 3: Answer includes two differences between traditional data sources and big data sources.
# Score 4: Answer includes three differences between traditional data sources and big data sources.
# Score 5: Answer includes more than three differences between traditional data sources and big data sources.""",
#     question="Mention 5 (five) main differences between traditional data sources and big data sources!",
#     context="1. Value: Traditional data sources have clear value directly related to business operations, while big data sources require sophisticated analytical tools and data science techniques to uncover complex insights. 2. Complexity: Traditional data sources are relatively easier to manage due to their homogeneity and defined structure, whereas big data sources are complex due to high volume, variability, and velocity. 3. Technology Required: Traditional data can be managed with traditional IT systems, while big data requires new technologies like Hadoop, NoSQL databases, and real-time data processing platforms. 4. Data Volume: Traditional data is usually smaller in size and can be processed using conventional methods, whereas big data involves dealing with extremely large volumes of data. 5. Real-time Processing: Traditional data processing is often batch-oriented, while big data requires real-time or near real-time processing to gain value from the data.",
#     student_answer="From its structure, traditional data is structured while big data has data that is unstructured or semi-structured. From its size, traditional data sources are very small, they can be large but rare, while big data has large data sources, traditional data sources are less diverse and varied, tending to 1 different source with big data which has diverse and varied data sources from various sources. Processing big data data sources requires someone who is an expert because new big data data sources are meaningful or have very high value if processed in the right way, different from traditional data which is the opposite. Because the data sources Big data is diverse, so its accuracy and validity are vulnerable, so it requires good analysis to produce the right decisions"
# )
#
# print("=============================================================")
# uas_4_result = method1.evaluate(
#     question="Mention 3 (three) main differences between structured and unstructured data forms!",
#     rubric="""Score 1: The answer does not include the difference between structured data and unstructured data.
# Score 2: The answer provides a distinction between structured and unstructured forms of data but is not relevant.
# Score 3: The answer provides one difference between structured and unstructured data forms correctly.
# Score 4: The answer provides two differences between structured and unstructured data forms correctly.
# Score 5: The answer provides three differences between structured and unstructured data forms correctly.""",
#     context="Structured data is organized in a predefined format that allows for easy searching, sorting, and analysis using traditional database management systems. It typically follows a specific schema or data model, such as relational databases or spreadsheets. Examples include numbers, dates, and text data with a clear structure. Unstructured data, on the other hand, does not have a predefined format or schema. It can be found in various forms like text documents, images, audio, video, and sensor data. Unstructured data is more complex to process as it requires advanced technologies and innovative approaches for analysis, such as natural language processing, machine learning algorithms, and data mining techniques. Three main differences between structured and unstructured data are: 1. Format: Structured data follows a predefined format that makes it easier to search, sort, and analyze using traditional database management systems. Unstructured data does not have a predefined format and requires advanced technologies for processing and analysis. 2. Processing: Structured data can be processed using traditional information technology and DBMS, while unstructured data requires new technologies like Hadoop, NoSQL databases, and real-time data processing platforms to manage and analyze it effectively. 3. Value extraction: The value extracted from structured data is often clear and directly related to business operations, whereas the value of unstructured data is not immediately obvious and may require sophisticated analytical tools and data science techniques to uncover complex insights.",
#     student_answer="Structured Data: - The types are numbers, characters and steps - The storage capacity required is smaller - The appearance can be visualized in rows, columns and appropriate databases Unstructured Data: - The type is image, sound or video data - The storage capacity required is larger - Its appearance cannot be visualized in the corresponding rows, columns and database."
# )
