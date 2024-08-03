from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


class Method1:
    def __init__(self, temperature=0, groq_api_key="", model_name="llama3-8b-8192"):
        self.chat = ChatGroq(temperature=temperature, groq_api_key=groq_api_key, model_name=model_name)
        self.system = "You are an academic assistant tasked with scoring and providing reasoning for student answers based on specific guidelines."
        self.rubric = """Score 1: The answer does not explain what Artificial Intelligence (AI) is and does not include examples.
Score 2: The answer describes Artificial Intelligence (AI) but does not include any examples.
Score 3: The answer explains Artificial Intelligence (AI) accurately and includes one correct example of AI.
Score 4: The answer explains Artificial Intelligence (AI) accurately and includes two correct examples of AI.
Score 5: The answer accurately describes Artificial Intelligence (AI) and includes more than two correct examples of AI."""

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

    def _make_output_json_array(self, output):
        llm_output = output
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
        human = """
        question: {question}

        Read the following questions, then extract the following questions and determine the aspects that students must answer.

        desired output format:
        json array of string
        """
        prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", human)])
        chain = prompt | self.chat
        response = chain.invoke({"question": question})
        return self._make_output_json_array(response.content)

    def evaluate_per_aspect(self, question, student_answer, context, extraction_result):
        extraction_result_string = "\n".join(extraction_result)
        human = """
        Student answer:
        {answer}

        Question aspects:
        {aspects}

        Supporting Theory:
        {context}

        Use your knowledge to evaluate the student's answer based on the question aspects provided.
        Evaluate the student's answer based on the question aspects provided.

        desired output format:
        json array with keys "aspect", "student_answer", "evaluation_level", and "evaluation" in one line
        """
        prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", human)])
        chain = prompt | self.chat
        response = chain.invoke({"answer": student_answer, "aspects": extraction_result_string, "context": context})
        return self._make_output_json_array(response.content)

    def match_per_rubric(self, student_answer, evaluation_per_aspect_result):
        evaluation_per_aspect_result_string = "\n".join(
            [f"aspect: {result['aspect']}\nevaluation_aspect: {result['evaluation']}\n" for result in
             evaluation_per_aspect_result]
        )
        results = []
        for rubric in self.rubrics:
            rubcric_string = f"rubric: {rubric['description']}\nrubric_score: {rubric['score']}"
            human = """
            Score Guideline:
            {rubric}

            Evaluation aspects:
            {evaluation_aspects}

            Student answer: 
            {student_answer}

            Calculate the match rate between the rubric and student answer.

            desired output format:
            json object with keys "rubric", "rubric_score", "match_rate", and "reason" in one line
            """
            prompt = ChatPromptTemplate.from_messages([("system", self.system), ("human", human)])
            chain = prompt | self.chat
            response = chain.invoke({"rubric": rubcric_string, "student_answer": student_answer,
                                     "evaluation_aspects": evaluation_per_aspect_result_string})
            results.append(self._make_output_json(response.content))
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

    def evaluate(self, rubric, question, student_answer, context):
        self.rubric = rubric
        self.rubric_array = self.rubric.split("\n")
        self.rubrics = self._prepare_rubrics()

        print("Rubric:")
        print(rubric)

        print("\nQuestion:")
        print(question)

        extraction_result = self.extract(question)
        evaluation_per_aspect_result = self.evaluate_per_aspect(question, student_answer, context, extraction_result)
        matching_per_rubric_result = self.match_per_rubric(student_answer, evaluation_per_aspect_result)
        matching_rubric_result = self.matching_rubric(student_answer, evaluation_per_aspect_result)

        print("Extraction Result:")
        for result in extraction_result:
            print(result)

        print("\nEvaluation Result:")
        for result in evaluation_per_aspect_result:
            print(result)

        print("\nMatching per Rubric Result:")
        for result in matching_per_rubric_result:
            print(result)

        print("\nMatching Rubric Result:")
        for result in matching_rubric_result:
            print(result)

# Example usage:
# evaluator = AcademicEvaluator(temperature=0, groq_api_key="your_api_key_here", model_name="llama3-8b-8192")
# evaluator.evaluate(question, student_answer, context)
