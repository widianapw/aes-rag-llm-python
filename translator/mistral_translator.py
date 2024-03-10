from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from langchain.prompts import PromptTemplate
from deep_translator import GoogleTranslator


def translate_to_english(content: str) -> str:
    try:
        llm = Ollama(model="mistral", temperature=0.1)
        prompt_template = PromptTemplate.from_template(
            "You are the translator to translate the given text from Indonesian to English. Translate the context directly and concisely. "
            "text: {text}"
        )
        text = prompt_template.format(text=content)
        translated_content = llm.invoke(text)
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
        return translated_content
    except:
        translator = GoogleTranslator(target="id")
        return translator.translate(content)