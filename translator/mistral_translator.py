from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain.prompts import PromptTemplate
from deep_translator import GoogleTranslator
import re

def clean_result(answer):
    # remove double new line, set to single new line
    response = re.sub(r'\n{2,}', '\n', answer)
    # remove extra spaces or tabs
    response = re.sub(r'\s+', ' ', response)
    # remove multiple dot (.), set to single dot
    response = re.sub(r'\.{2,}', '.', response)
    # trim leading and trailing whitespace
    response = response.strip()
    return response

def translate_to_english(content: str) -> str:
    try:
        llm = Ollama(model="mistral", temperature=0.1)
        prompt_template = PromptTemplate.from_template(
            "You are the translator to translate the given text from Indonesian to English. Translate the context directly and concisely. "
            "text: {text}"
        )
        text = prompt_template.format(text=content)
        translated_content = llm.invoke(text)
        translated_content = clean_result(translated_content)
        #if translated_content starts with "translation : " then remove it
        if translated_content.startswith("Translation: "):
            translated_content = translated_content[len("Translation: "):]

        return translated_content
    except:
        translator = GoogleTranslator(target="id")
        return translator.translate(content)


def translate_to_indonesia(content: str) -> str:
    try:
        llm = Ollama(model="mistral", temperature=0.1)
        prompt_template = PromptTemplate.from_template(
            "You are the translator to translate the given text from English to Indonesian. Translate the context directly and concisely. "
            "text: {text}"
        )
        text = prompt_template.format(text=content)
        translated_content = llm.invoke(text)
        translated_content = clean_result(translated_content)
        #if translated_content starts with "translation : " then remove it
        if translated_content.startswith("Translation: "):
            translated_content = translated_content[len("Translation: "):]

        return translated_content
    except:
        translator = GoogleTranslator(target="id")
        return translator.translate(content)