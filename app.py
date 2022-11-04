from flask import Flask, request, render_template, redirect, flash, jsonify


from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)

#  This will be the survey title borrowed from the clas survey function
title = satisfaction_survey.title
#After the title  is set , let set the current question  counter to  initial index Zero
current_question = [0]

# Our Survey question,answer will be put in a list holder called "res"
res = []


def reset_survey_values():
    """ after current question is set to index zero """
    """ let resets survey current question to value of Zero """
    current_question[0] = 0

    # once we reset, we should have the propensity to remove all element the res list
    # clear() shoud do  that for us
    res.clear()

# app.route links us to welcome page
@app.route("/")
def welcome_page():
    """
        the welcome page  has up to 3 funtions supported by render_template:
        1:  return title  of survey 
        2:  return  instructions
        3: it will also show the click start page
    """
      # instructions variable  need to be called  here 
    instructions = satisfaction_survey.instructions
           # title is passed to the survey title 
           # instruction is passed to survey instructions
    return render_template("welcomes.html", title_holder=title,
                           survey_instructions=instructions)


# @app.route link us to question form.html page
@app.route("/questions")
def questions_page():
    """ 
        In the question  page, the current question will be passed

        This page will display current question as well as answer choice
        button radios. 

        skipping next page on button radio will send a bad request to server

    """

       # "title" variable was borrowed from line 21  in class Sruvey
       # "questions" varibles was borrowed from  line 22 in class Survey
    title = satisfaction_survey.title
    # from class Question (), line 10 handles all kinds of question
    # hence let grab  a current  question  from line 10 
    # let pass the current question  to  line 23 from class Survey ()
    #  and point to a specific satisfaction survey question ()
    # from  line  26 in survey.py
    quest_holder = satisfaction_survey.questions[current_question[0]].question
      # handles list of answers from all the choice we make from every page
    answers_list = []
    x = 0
    #let get our answer by  making a choice from the class Question at chocies ()
    # in line 8 and the we can append  to the answers list
    for answer in satisfaction_survey.questions[current_question[0]].choices:
        answers_list.append((
            answer, f"{x},{answer.replace(' ', '-')}"))
        x += 1
     # in the form template we are passing the  title to title holder
     # we will pass the current  question to a question  number
     # we will pass all the  questions to  total quest
     # we will pass  question  to  a question holder
     # we will pass the  answers list  to  answer holder
    return render_template("form.html", title_holder=title,
                           quest_num= current_question[0],
                           total_quest=(
                               len(satisfaction_survey.questions)),
                           quest_holder=quest_holder,
                           answer_holder=answers_list)


@app.route("/answer", methods=["POST"])
def answer_page():
    """ This function will handle answer to our survey questions. 

    """

     # we are requesting from <form action> and passing  current question answer 
    #  the current question are tagged along to the radio boxe name q-choices
    answer = request.form[f'q-{current_question[0]}-choices']
    #  answer will be appended to "res" as  res is the sole holder of  all the  q/a
    res.append(answer)

    # next question counter
    current_question [0] += 1

    # If   question is  no more we will redirect  to question  else say thanks!! 
    if (current_question  [0] < len(satisfaction_survey.questions)):
        return redirect("/questions")

    else:
        return redirect("/thankyou")


@app.route("/thankyou")
def thank_you_page():
    """ thank you () handles thank you page. """

    # if the survey is complete we can display all  response for quest_ans
    # and put in quest_ans_holder
    if ((current_question[0] == len(satisfaction_survey.questions)) and (len(res) == len(satisfaction_survey.questions))):
        quest_ans = "Your Survey Respond:<br>"
        x = 0
        for quest in satisfaction_survey.questions:
            quest_ans = f"{quest_ans}{x + 1}. {quest.question}  <b>{res[x]}</b><br><br>"
            x += 1

        return render_template("thanks.html", title_holder=title,
                               quest_ans_holder=quest_ans)
    else:
        # restart 
        #  reset 
        reset_survey_values()
        flash("There is break in transmission . Survey was reset.", "warning")
        return redirect("/")


@app.route("/reset")
def survey_reset():
    """ survey () reset completley reset survey and survey variables """

    reset_survey_values()

    return redirect("/")
