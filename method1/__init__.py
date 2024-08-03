from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json


class Method1:
    def __init__(self, temperature=0, groq_api_key="", model_name="llama3-70b-8192"):
        self.chat = ChatGroq(temperature=temperature, groq_api_key=groq_api_key, model_name=model_name)
        self.system = "You are an academic assistant tasked with scoring and providing reasoning for student answers based on specific guidelines."
        self.rubric = """Score 1: The answer does not explain what Artificial Intelligence (AI) is and does not include examples.
Score 2: The answer describes Artificial Intelligence (AI) but does not include any examples.
Score 3: The answer explains Artificial Intelligence (AI) accurately and only include example of AI.
Score 4: The answer explains Artificial Intelligence (AI) accurately and includes two examples of AI.
Score 5: The answer accurately describes Artificial Intelligence (AI) and includes more than two examples of AI."""

        self.rubric_array = self.rubric.split("\n")
        self.rubrics = self._prepare_rubrics()

    def _prepare_rubrics(self):
        rubrics = []
        for rubric in self.rubric_array:
            score = rubric.split(":")[0].strip()
            score = int(score.split(" ")[1])
            description = rubric.split(":")[1].strip()
            rubrics.append({"score": score, "description": description})
        return rubrics

    def _make_output_json_array(self, output, isObject=False):
        llm_output = output

        # remove \n from llm_output
        llm_output = llm_output.replace("\n", "")
        if "[" in llm_output:
            llm_output = llm_output[llm_output.index("["):]
        else:
            if llm_output[0] != "[":
                llm_output = "[" + llm_output
        if "]" in llm_output:
            llm_output = llm_output[:llm_output.index("]") + 1]
        else:
            if llm_output[-1] != "]":
                llm_output += "]"

        if isObject:
            if llm_output[-2] != "}" and llm_output [-2] != ",":
                llm_output = llm_output[:-1] + "}"
                llm_output = llm_output + "]"

        print("llm_output: ", llm_output)

        return eval(llm_output)

    def _make_output_json(self, output):
        llm_output = output
        if "{" in llm_output:
            llm_output = llm_output[llm_output.index("{"):]
        else:
            if llm_output[0] != "{":
                llm_output = "{" + llm_output
        if "}" in llm_output:
            llm_output = llm_output[:llm_output.index("}") + 1]
        else:
            if llm_output[-1] != "}":
                llm_output += "}"
        return llm_output

    def extract(self, question):
        system = "You are an helpful assistant tasked to separate question into individual question."
        human = """
question: {question}

Let's thinking step by step and Separate the given question into individual question without loosing its context.

desired output format:
json array of string"""
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
        chain = prompt | self.chat
        response = chain.invoke({"question": question})
        print(question)
        print(response.content)
        return self._make_output_json_array(response.content)

    def evaluate_per_aspect(self, question, student_answer, context, extraction_result):
        extraction_result_string = "\n".join(
            [f"{no + 1}. {result}" for no, result in
             enumerate(extraction_result)]
        )

        # print("Extraction result per string")
        # print(extraction_result_string)

        #         human = """
        # Student answer:
        # {answer}
        #
        # Question aspects:
        # {aspects}
        #
        # Evaluate the student's answer based on the question aspects provided.
        #
        # desired output format:
        # json array with keys "aspect", "student_answer", "evaluation_level", and "evaluation" in one line"""

        human = """
Student answer:
{answer}

Supporting theories:
{context}

Questions:
{aspects}

Evaluate the student's answer based on the questions provided.
Use supporting theory as a reference in conducting the evaluation. Use the following rules:
1. The answer does not have to exactly match the supporting theory, but you can use the supporting theory as a consideration in assessing an answer.
2. In evaluating an answer, you do not have to compare it explicitly with the supporting theory. But it is the meaning of the supporting theory that you consider in assessing an answer.

desired output format:
json array with keys and datatype "question" : string, "student_answer": string, and "evaluation": string in one line"""
        prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", human)])
        chain = prompt | self.chat
        response = chain.invoke({"answer": student_answer, "aspects": extraction_result_string, "context": context})
        print("Evaluation per aspect result")
        print(student_answer)
        print(extraction_result_string)
        print(context)
        print(response.content)
        return self._make_output_json_array(response.content, True)

    def match_per_rubric(self, student_answer, evaluation_per_aspect_result):
        evaluation_per_aspect_result_string = "\n".join(
            [f"{no + 1}. {result['student_answer']}" for no, result in
             enumerate(evaluation_per_aspect_result)]
        )

        # print("Evaluation per aspect result per string\n", evaluation_per_aspect_result_string)

        system = "You are a helpful assistant."

        results = []
        for rubric in self.rubrics:
            rubric_string = f"{rubric['description']}"
            human = """
Score Guideline:
{rubric}

Student answer: 
{student_answer}

Student Answer Breakdown:
{evaluation_aspects}

Take the following steps:
1. Breakdown the scoring guideline and determine whether or not the student answer and scoring guideline are match.
2. Explain the match reason in detail.

output format:
json object with key is_match: number 0 or 1, match_rate: float, and reason: string in one line"""
            prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", human)])
            chain = prompt | self.chat
            response = chain.invoke({"rubric": rubric_string, "student_answer": student_answer,
                                     "evaluation_aspects": evaluation_per_aspect_result_string})
            print(evaluation_per_aspect_result_string)
            print(response.content)
            json_text = self._make_output_json(response.content)
            # add rubric_text and rubric_score to the json_text

            print(json_text)
            json_text = json.loads(json_text)
            json_text["rubric_text"] = rubric_string
            json_text["rubric_score"] = rubric["score"]
            # set back to string
            json_text = json.dumps(json_text)
            results.append(json_text)
            # results.append(self._make_output_json(response.content))
        return results

    def match_per_rubric_1(self, student_answer):
        system = "You are a helpful assistant."

        results = []
        for rubric in self.rubrics:
            rubric_string = f"{rubric['description']}"
            print(rubric_string)
            print(student_answer)
            print("====================================")
            human = """
Score Guideline:
{rubric}

Student answer: 
{student_answer}

Take the following steps:
Breakdown the scoring guideline and determine whether or not the student answer and scoring guideline are match.

desired output format:
json object with key:
is_match: boolean
match_rate: number"""
            prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", human)])
            chain = prompt | self.chat
            response = chain.invoke({"rubric": rubric_string, "student_answer": student_answer})
            print(response.content)
            # print(response.content)
            json_text = self._make_output_json(response.content)
            # add rubric_text and rubric_score to the json_text

            # json_text = json.loads(json_text)
            # json_text["rubric_text"] = rubric_string
            # json_text["rubric_score"] = rubric["score"]
            # # set back to string
            # json_text = json.dumps(json_text)
            results.append(json_text)
            # results.append(self._make_output_json(response.content))
        return results

    def matching_rubric(self, student_answer, evaluation_per_aspect_result):
        evaluation_per_aspect_result_string = "\n".join(
            [
                f"aspect: {result['aspect']}\nstudent_answer: {result['student_answer']}\nevaluation: {result['evaluation']}\n"
                for result in evaluation_per_aspect_result]
        )
        human = """
        Scoring Guidelines:
        {rubric}

        Student evaluation aspects:
        {evaluation_aspects}

        student answer:
        {student_answer}

        Give the evaluation per scoring guidelines provided.

        desired output format:
        json array with keys "scoring_guideline", "student_answer", "match_level", and "match" in one line
        """
        prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", human)])
        chain = prompt | self.chat
        response = chain.invoke({"rubric": self.rubric, "evaluation_aspects": evaluation_per_aspect_result_string,
                                 "student_answer": student_answer})

        return self._make_output_json_array(response.content)

    def rubric_based_evaluation(self, evaluation_per_aspect_result):
        evaluation_per_aspect_result_string = "\n".join(
            [
                f"aspect: {result['aspect']}\nstudent_answer: {result['student_answer']}\nevaluation: {result['evaluation']}\n"
                for result in evaluation_per_aspect_result]
        )
        human = """
        Scoring Guidelines:
        {rubric}

        Student evaluation aspects:
        {evaluation_aspects}

        Evaluate the student evaluation aspect based on Scoring guidelines provided,

        desired output format:
        json object with keys "question", "score", and "reasoning" in one line
        """
        prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", human)])
        chain = prompt | self.chat
        response = chain.invoke({"rubric": self.rubric, "evaluation_aspects": evaluation_per_aspect_result_string})
        return self._make_output_json(response.content)

    def decide_score(self, matching_per_rubric_result):
        # Parse JSON strings into dictionaries
        parsed_results = [json.loads(result) for result in matching_per_rubric_result]

        # Ensure all elements in parsed_results contain the expected keys
        filtered_results = [result for result in parsed_results if
                            isinstance(result, dict) and 'match_rate' in result]

        # check filtered results where is_match is True
        selection_1_results = [result for result in filtered_results if result['is_match']]
        print("Selection 1 Results Length: ", len(selection_1_results))
        if len(selection_1_results) > 0:
            return selection_1_results[-1]
            if len(selection_1_results) == 1:
                return selection_1_results[0]
            else:
                # Get max match rate
                max_match_rate = max(result['match_rate'] for result in selection_1_results)

                # Get all rubrics with max match rate
                max_rubrics = [result for result in selection_1_results if result['match_rate'] == max_match_rate]

                # Get the latest rubric with max match rate (last one in the list)
                latest_rubric = max_rubrics[-1]

                return latest_rubric

        if not filtered_results:
            raise ValueError("No valid results in matching_per_rubric_result")

        # Get max match rate
        max_match_rate = max(result['match_rate'] for result in filtered_results)

        # Get all rubrics with max match rate
        max_rubrics = [result for result in filtered_results if result['match_rate'] == max_match_rate]

        # Get the latest rubric with max match rate (last one in the list)
        latest_rubric = max_rubrics[-1]

        return latest_rubric

    def evaluate(self, rubric, question, student_answer, context):
        self.rubric = rubric
        self.rubric_array = self.rubric.split("\n")
        self.rubrics = self._prepare_rubrics()

        extraction_result = self.extract(question)
        evaluation_per_aspect_result = self.evaluate_per_aspect(question, student_answer, context, extraction_result)
        matching_per_rubric_result = self.match_per_rubric(student_answer, evaluation_per_aspect_result)
        # matching_per_rubric_result = self.match_per_rubric_1(student_answer)
        # matching_rubric_result = self.matching_rubric(student_answer, evaluation_per_aspect_result)

        # print("Extraction Result:")
        # for result in extraction_result:
        #     print(result)
        #
        # print("\nEvaluation Result:")
        # for result in evaluation_per_aspect_result:
        #     print(result)
        #
        # print("\nMatching per Rubric Result:")
        # for result in matching_per_rubric_result:
        #     print(result)
        #
        # print("\nDecide Score:")
        decide_score_result = self.decide_score(matching_per_rubric_result)
        print(decide_score_result)
        return decide_score_result

        # print("\nMatching Rubric Result:")
        # for result in matching_rubric_result:
        #     print(result)

# Example usage:
# evaluator = AcademicEvaluator(temperature=0, groq_api_key="your_api_key_here", model_name="llama3-8b-8192")
# evaluator.evaluate(question, student_answer, context)
