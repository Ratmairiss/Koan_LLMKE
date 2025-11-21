
def print_answers_check(llm_answers, answers, questions):
    rightAnsw = 0
    wrongAnsw = 0

    for llm_answer in llm_answers:
        if answers[int(llm_answer['id']) - 1].lower() == llm_answer['answer'].lower():
            rightAnsw += 1
        else:
            wrongAnsw += 1
            print("Wrong answer: ",   llm_answer['answer'],
                  "\nCorrect answer: ", answers[int(llm_answer['id']) - 1],
                  "\nQuestion: ",       questions[int(llm_answer['id']) - 1],'\n')

    print("Correct = ", rightAnsw)
    print("Incorrest = ", wrongAnsw)
