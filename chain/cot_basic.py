from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

llm = Ollama(model="mistral")


# prompt_template = PromptTemplate.from_template("""
# Classify the question as 'open' or 'closed' based on the criteria and examples provided.
#
# A 'closed' question is one whose answer can be found specifically and explicitly in the existing knowledge base. These questions typically have clear right or wrong answers, or are limited to a set number of answer choices. Answers to closed questions are generally factual and do not require interpretation or personal opinion.
#
# Question: {question}
# desire answer format: open or closed
# """)

prompt_template = PromptTemplate.from_template("""
You are an assistant to give score and reasoning for the student answer.

rubric:
Score 1: The answer does not explain the actuator in IoT and does not provide an example.
Score 2: The answer explains the actuator in IoT but does not provide an example.
Score 3: The answer explains the actuator in IoT and provides only one example.
Score 4: The answer explains the actuator in IoT and provides two examples.
Score 5: The answer explains the actuator in IoT and provides three examples.

question:
Explain Actuators in the Internet of Things (IoT) and give examples!

context retrieved from document:
Actuators are devices that enable IoT applications to carry out real actions in the physical world. They are used to control the flow of liquids or gases, regulate temperature, and ventilate or cool air. Examples of actuators include water pumps, electric valves, heaters, and electric fans. These devices are crucial in home automation, industry, smart agriculture, healthcare, and many other areas where IoT is used to monitor environmental conditions and automatically take appropriate action.

student answer:
Actuator is one form of Physical component in the Internet of Things IoT. Actuator is a component or equipment to move or control a mechanism or system. Example of Actuator:  Actuators in cars that function to move the car system.  Actuator on a robot that functions to produce movement on the robot Actuator on a light search engine that functions to move the machine following the direction of the light source.

Lets thinking step by step and evaluate the student answer based on the rubric and context.

output desired format:
json object with following keys:
question: <string>,
score: <number>,
reasoning: <string>
""")

print(llm.invoke(prompt_template.format()))
