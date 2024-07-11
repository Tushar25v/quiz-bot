
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not current_question_id:
        return False, "Error: No current question id provided."

    if not answer:
        return False, "Error: Answer cannot be empty."
     
    session_key = f"answer_{current_question_id}"
    session[session_key] = answer
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        # Start from the first question if there is no current question id
        next_question_id = 0
    else:
        next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]
    else:
        # No more questions
        next_question = None
        next_question_id = None

    return next_question, next_question_id

     


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_count = 0
    user_answers = []

    for question_id in range(total_questions):
        session_key = f"answer_{question_id}"
        user_answer = session.get(session_key, "")
        correct_answer = PYTHON_QUESTION_LIST[question_id]["answer"]

        if user_answer == correct_answer:
            correct_count += 1
            result = "Correct"
        else:
            result = f"Incorrect (Correct answer: {correct_answer})"

        user_answers.append({
            "question": PYTHON_QUESTION_LIST[question_id]["question_text"],
            "your_answer": user_answer,
            "result": result
        })

    score = (correct_count / total_questions) * 100

    final_message = "Quiz Results:\n"
    for answer in user_answers:
        final_message += f"Q: {answer['question']}\n"
        final_message += f"Your Answer: {answer['your_answer']}\n"
        final_message += f"Result: {answer['result']}\n\n"

    final_message += f"Your total score is: {score}%"

    return final_message


    return "dummy result"
