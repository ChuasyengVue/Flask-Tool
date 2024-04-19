from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask (__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)


RESPONSE_KEY = 'responses'


@app.route('/')
def survey_page():
    return render_template('survey.html', survey=survey)


@app.route('/start', methods = ['POST'])
def question_zero():

    session[RESPONSE_KEY] = []

    return redirect('/questions/0')


@app.route('/answer', methods =['POST'])
def answers():
    
    choice = request.form['answer']

    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    
    else:
        
        return redirect(f'/questions/{len(responses)}')

# qid = question id
@app.route('/questions/<int:qid>')
def questions(qid):

    responses = session.get(RESPONSE_KEY)

    if (responses is None):
        return redirect(f'/')
    
    if (len(responses) == len(survey.questions)):
        return redirect ('/complete')
    
    if (len(responses) != qid):
        flash (f'Invalid question id: {qid}')
        return redirect (f'/questions/{len(responses)}')

    question = survey.questions[qid]
    return render_template("questions.html",question_number=qid, question=question)


@app.route('/complete')
def complete():
    return render_template('complete.html')



    