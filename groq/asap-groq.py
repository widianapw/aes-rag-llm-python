from time import sleep

import pandas as pd
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import json
import os

def append_to_json(file_path, result):
    data = []
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding JSON from file")
                return

    data.append(result)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


rubric = """Score Point 1: An undeveloped response that may take a position but offers no more than very minimal support. Typical elements:
- Contains few or vague details.
- Is awkward and fragmented.
- May be difficult to read and understand.
- May show no awareness of audience.

Score Point 2: An under-developed response that may or may not take a position. Typical elements:
- Contains only general reasons with unelaborated and/or list-like details.
- Shows little or no evidence of organization.
- May be awkward and confused or simplistic.
- May show little awareness of audience.

Score Point 3: A minimally-developed response that may take a position, but with inadequate support and details. Typical elements:
- Has reasons with minimal elaboration and more general than specific details.
- Shows some organization.
- May be awkward in parts with few transitions.
- Shows some awareness of audience.

Score Point 4: A somewhat-developed response that takes a position and provides adequate support. Typical elements:
- Has adequately elaborated reasons with a mix of general and specific details.
- Shows satisfactory organization.
- May be somewhat fluent with some transitional language.
- Shows adequate awareness of audience.

Score Point 5: A developed response that takes a clear position and provides reasonably persuasive support. Typical elements:
- Has moderately well elaborated reasons with mostly specific details.
- Exhibits generally strong organization.
- May be moderately fluent with transitional language throughout.
- May show a consistent awareness of audience.

Score Point 6: A well-developed response that takes a clear and thoughtful position and provides persuasive support. Typical elements:
- Has fully elaborated reasons with specific details.
- Exhibits strong organization.
- Is fluent and uses sophisticated transitional language.
- May show a heightened awareness of audience.
"""

df = pd.read_excel('../assets/asap/essay_set_1.xlsx')

# drop nan values in rater1_domain1 and rater2_domain1
df = df.dropna(subset=['rater1_domain1', 'rater2_domain1'])

# read last_id.txt
with open('../assets/asap/last_id.txt', 'r') as f:
    last_id = int(f.read())

# filter df where essay_id is greater than last_id
df = df[df['essay_id'] > last_id]

chat = ChatGroq(temperature=0.1, groq_api_key="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",
                model_name="mixtral-8x7b-32768")


dataset_prompt= """More and more people use computers, but not everyone agrees that this benefits society. Those who support advances in technology believe that computers have a positive effect on people. They teach hand-eye coordination, give people the ability to learn about faraway places and people, and even allow people to talk online with other people. Others have different ideas. Some experts are concerned that people are spending too much time on their computers and less time exercising, enjoying nature, and interacting with family and friends. 
Write a letter to your local newspaper in which you state your opinion on the effects computers have on people. Persuade the readers to agree with you.
"""

system = """As a virtual evaluator with expertise in English composition, your role is to critically analyze and grade student essays according to a predetermined set of rubrics. You are to act as an impartial judge and evaluate the essays based on the quality of the writing and adherence to the essay prompt."""

human ="""Here are the specific guidelines for each score:
{rubrics}

Sample Essay Prompt:
{prompt}

Student’s Essay to Evaluate:
{essay}

Task Breakdown:
1. Carefully read the provided essay prompt, scoring guidelines, and the
student’s essay.
2. In the Explanations part, identify specific elements in the essay referring
to the rubrics. In the language dimension, list all the spelling and grammar
errors, and count the number of them to determine the Language Score. The
Explanations for each dimension should be as detailed as possible.
3. Determine the appropriate scores according to the analysis above.

Please present your evaluation in the following manner:
json object with keys "score" (number) and "reasoning" (string) in one line."""

prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat

for index, row in df.iterrows():
    response = chain.invoke({
        "rubrics": rubric,
        "prompt": dataset_prompt,
        "essay": row['essay']
    })
    llm_output = response.content
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

    print(row['essay'])
    print(llm_output)
    output_obj = eval(llm_output)
#     save to csv
    with open('../assets/asap/last_id.txt', 'w') as f:
        f.write(str(row['essay_id']))

    json_object = {
        "essay_id": row['essay_id'],
        "essay": row['essay'],
        "rater1_domain1": row['rater1_domain1'],
        "rater2_domain1": row['rater2_domain1'],
        "score": output_obj['score'],
        "reasoning": output_obj['reasoning']
    }
    append_to_json('../assets/asap/asap_groq_output.json', json_object)
    sleep(30)





