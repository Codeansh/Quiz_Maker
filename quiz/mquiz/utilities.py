import json

def Quiz_to_dict(quiz):
    quiz_json = quiz.to_json()
    return json.loads(quiz_json)
