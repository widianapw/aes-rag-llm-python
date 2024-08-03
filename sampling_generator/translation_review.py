import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

MODEL_NAME = "llama3-70b-8192"

df_translation = pd.read_excel('../assets/sampling/translation.xlsx')

# iterate over rows with iterrows()
results = []
for index, row in df_translation.iterrows():
    print(row['answer'])
    print(row['translated_answer'])
    chat = ChatGroq(temperature=0, groq_api_key="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",
                    model_name=MODEL_NAME)
    system = "You are an translation review assistant indonesia to english to determine that the translation is correct or not."
    human = """
answer: {answer}    
translated_answer: {translated_answer}

Review the translation and determine if it is correct or not, minor problem its ok as long as it doesnt change the context of sentence.

Desired Output Format:
JSON object with keys "is_correct": 1 | 0 and "reason": string in one line."""
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    response = chain.invoke({"answer": row['answer'], "translated_answer": row['translated_answer']})

    is_success = True
    try:
        llm_output = response.content
        # if llm_output is contains } or not
        if "{" in llm_output:
            llm_output = llm_output[llm_output.index("{"):]
        else:
            if llm_output[0] != "{":
                llm_output = "{" + llm_output

        # check if llm_output is end with } or not
        if "}" in llm_output:
            llm_output = llm_output[:llm_output.index("}") + 1]
        else:
            if llm_output[-1] != "}":
                llm_output += "}"

        json_response = eval(llm_output)
    except Exception as e:
        is_success = False
        print(e)
        print(response.content)

    results.append({
        "no": row['no'],
        "key": row['key'],
        "subject": row['subject'],
        "answer": row['answer'],
        "translated_answer": row['translated_answer'],
        "is_correct": json_response['is_correct'] if is_success else 'manual',
        "reason": json_response['reason'] if is_success else 'manual'
    })

# save result to xlsx
df_results = pd.DataFrame(results)
df_results.to_excel('../assets/sampling/translation_review_result.xlsx', index=False)
