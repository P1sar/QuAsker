from app import app, db, lm, facebook
from flask import render_template, request, flash, redirect, session, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm, EditProfile, EditAvatar, AskQuestion, WriteAnswer, VoteAnswer
from wtforms.validators import ValidationError
from models import User, Question, Answer
from datetime import datetime
from werkzeug import secure_filename
import hashlib
import os

@app.template_filter('format_date')
def format_date(s):
    return s.strftime('%d %B %Y; %H:%M')

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/index")
def index():

    question = Question.query.order_by(Question.post_time.desc()).all()


    by_user = User.query.all()



    ip = request.remote_addr

    return render_template("index.html",question = question,
                            user_ip = ip, user = by_user)



@app.route("/login", methods = ["GET", "POST"])
def login():

    if current_user is not None and current_user.is_authenticated():
        flash("You are logged in already", "notice")
        return redirect(url_for("index"))

    login_form = LoginForm()


    if login_form.validate_on_submit():

        get_password_hash = hashlib.sha224(login_form.password.data).hexdigest()  
        #looking for an a existing email in our database
        get_user = User.query.filter_by(email=login_form.email.data)

        if get_user:

            for item in get_user:
                user_id = item.id
                user_pass = item.password
                user = User.query.get(user_id)

                if user_pass == get_password_hash:
                    #compering password form login from with pass in database
                    user.is_authenticated = True
                    user.last_seen = datetime.now()
                    remember_me = login_form.remember_me.data
                    print remember_me
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember = remember_me)
                    flash("Welcome to QuAsker, %s!!!!"% str(user.nickname), "greetings")


                    return redirect ("/")

        flash("Incorrect Login or Password", 'error')

    return render_template("login.html",
                            title="Log in",
                            login_form=login_form)



@app.route("/register", methods = ["GET", "POST"])
def register():
    if current_user is not None and current_user.is_authenticated():
        flash("You are logged in already", "notice")
        return redirect(url_for("index"))

    register_form = RegisterForm()

    if register_form.validate_on_submit():
        email = register_form.email.data
        nickname = register_form.nickname.data
        password = register_form.password.data

        hash_type = hashlib.sha224()
        hash_type.update(password)
        hash_password = hash_type.hexdigest()


        #Verifaing email or nickname unique
        email_conflict = User.query.filter_by(email = email).first()
        nick_conflict = User.query.filter_by(nickname = nickname).first()

        if email_conflict:
            flash("This email is occupied already", "notice")
            return redirect (url_for('register'))
        elif nick_conflict:
            flash("This nick is occupied already", "notice")
            return redirect (url_for('register'))
        else:
            user = User(email=email, password = hash_password,
                        reg_date = datetime.now(),
                        nickname = nickname)
            db.session.add(user)
            db.session.commit()

        return redirect(url_for('index'))


        flash("Welcome " + str(register_form.nickname.data)\
                 + ", you registred successfully!!", "greetings")
        return redirect ("/login")
    return render_template("register.html",
                            title="Register",
                            register_form=register_form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Goodbuy! We will miss you...", "greetings")
    return redirect(url_for("index"))


@app.route("/user/<nickname>")
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    questions = Question.query.filter_by(user_id = user.id).all()
    answers = Answer.query.filter_by(user_id = user.id).all()

    if user == None:
        flash("User" + nickname + "not found", "error")
        return redirect(url_for("index"))

    return render_template('user.html',answers = answers,
                            user = user, questions = questions)


@app.route('/edit_profile', methods = ['GET','POST'])
@login_required
def edit():

    edit_form = EditProfile()
    edit_avatar = EditAvatar()

    if edit_avatar.avatar.data:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                current_user.nickname + ".png")
        edit_avatar.avatar.data.save(file_path)

    if edit_form.validate_on_submit():
        about_me = edit_form.about_me.data
        current_user.about_me = about_me
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('edit'))


    return render_template('edit_profile.html', edit_form = edit_form, 
                            edit_avatar = edit_avatar)


@app.route('/ask_question', methods = ["GET","POST"])
@login_required
def ask():
    new_question = AskQuestion()

    if new_question.validate_on_submit():
        question_title = new_question.question_title.data
        question_body = new_question.question_body.data
        question = Question(title = question_title, body = question_body, 
                            post_time =  datetime.now(),
                            user_id = current_user.id)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

    flash("Title or question can't be empty", "notice")

    return render_template("ask_question.html", new_question = new_question )


@app.route("/question/<id>", methods = ["GET","POST"])
def question(id):

    full_question = Question.query.filter_by(id = id).first()
    author = full_question.author.nickname
    new_answer = WriteAnswer()
    current_question_answers = Answer.query.filter_by(question_id = id).all()



    if new_answer.validate_on_submit():
        answer_body = new_answer.answer_body.data
        answer = Answer(body = answer_body, user_id = current_user.id, 
                        question_id = full_question.id , ans_time = datetime.now())
        db.session.add(answer)
        db.session.commit() 
        return redirect(url_for('question', id = full_question.id))


      

    return render_template("question.html", full_question = full_question,
                         author = author, new_answer = new_answer, 
                         current_question_answers = current_question_answers,
                         vote = vote, os = os)


@app.route("/vote/<id>", methods = ["GET","POST"])
def vote(id):
    answer_carma = Answer.query.filter_by(id = id).first()
    #Create a list from text colummn with users id
    voted_list = answer_carma.voted_users_id.split(",")

    #Cheking if user in the voted_users_list. If he is, flash notice, if not, approve voting
    if str(current_user.id) in voted_list:
        flash("U voted already", 'notice')
    else:
        answer_carma.votes+=1
        answer_carma.voted_users_id += "," + str(current_user.id)
        flash ("Voted", "notice")
        db.session.commit() 

    return redirect(request.referrer)




                        #<<<<FACEBOOK OAUTH LOGIN>>>>

@app.route('/login_facebook')
def login_facebook():
    return facebook.authorize(callback="http://localhost:5000/")


@app.route('/oauth-authorized')
@facebook.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash('You denied the request to sign in.', "error")
        return redirect(url_for('login'))

    session['facebook_token'] = (
        resp['access_token'], "")   
    session['facebook_user'] = resp['screen_name']

    user_data = facebook.get('/me').data
    user = User.query.filter(User.email == user_data['email']).first()
    print user_data['email']

    if user is None:
        new_user = User(id=user_data['id'], email=user_data['email'],
                        nickname=user_data['first_name'], reg_date = datetime.now)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
    else:
        login_user(user)

    flash('You were signed in as %s' % resp['screen_name'], "greetings")
    return redirect('login')


@facebook.tokengetter
def get_facebook_token(token = None):
    return session.get('facebook_token')


