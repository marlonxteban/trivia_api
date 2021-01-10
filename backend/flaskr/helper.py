QUESTIONS_PER_PAGE = 10
def paginate_questions(request, selection):
  page = request.args.get("page", 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def is_valid_question(body):
  attrs = ["question", "answer", "difficulty", "category"]

  for attr in attrs:
    if not attr in body or body[attr] is None:
      return False

  return True