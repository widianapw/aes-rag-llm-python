from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain.prompts.prompt import PromptTemplate

from langchain_community.llms import Ollama

llm = Ollama(model="mistral", temperature=0)
prompt_template = PromptTemplate.from_template("""
determine if the question is open, where answers may vary and are not strictly found in a provided key answer, or closed, where answers are expected to be specific and included in the key answer.
input: {question}
""")

prompt = prompt_template.format(question="Explain sensors in the Internet of Things (IoT)")
print(prompt)
print(llm.invoke(prompt))
