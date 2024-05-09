import re


def extract_questions(contents):
    print("extract_questions is being called with contents:", contents)
    extracted_questions = []

    for content in contents:
        questions = re.split(r'\n(?=FEEDBACK:)', content)

        for question in questions:
            parts = question.split('\n')

            q_text = parts[0]
            answer = parts[-2].split(': ')[1]
            feedback_text = parts[-1].split(': ')[1]
            choices = [choice.split('. ')[1] for choice in parts[1:-2]]

            extracted_questions.append({
                'text': q_text,
                'choices': choices,
                'answer': answer,
                'feedback': feedback_text,
            })

    return extracted_questions
