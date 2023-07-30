import secrets, os
from flask import render_template, url_for, flash, redirect, request
from quizzhub import app, db, bcrypt
from quizzhub.forms import RegistrationForm, LoginForm, UpdateAccountForm, CreateQuizForm, AttemptQuiz, SearchForm
from quizzhub.models import User, Quiz
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
@login_required
def home():
    quizes=Quiz.query.all()
    return render_template('home.html', quizes=quizes)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesful, Please check username and password','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex= secrets.token_hex(8)
    f_name,f_ext= os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated",'success')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file=url_for('static',filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file, form=form)

@app.route("/account/<int:user_id>", methods=['GET', 'POST'])
def user_account(user_id):
    user=User.query.get(user_id)
    quizes=Quiz.query.filter_by(user_id=user_id).all()
    image_file=url_for('static',filename='profile_pics/'+ user.image_file)
    return render_template('user_account.html', title=user.username, user=user, quizes=quizes, image_file=image_file)

@app.route("/quiz/new", methods=['GET', 'POST'])
@login_required
def new_quiz():
    form = CreateQuizForm()
    if form.validate_on_submit():
        quiz=Quiz(title=form.quiz_name.data,
                  question =form.question.data,
                  option1 =form.option1.data,
                  option2 =form.option2.data,
                  option3 =form.option3.data,
                  option4 =form.option4.data,
                  correct_option=form.correct_option.data,
                  author= current_user)
        db.session.add(quiz)
        db.session.commit()
        flash('Your quiz has been created','success')
        return redirect(url_for('home'))
    return render_template('create_quiz.html',title='New Quiz',form=form)

@app.route("/quiz/<int:quiz_id>", methods=['GET', 'POST'])
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form=AttemptQuiz()
    if form.validate_on_submit():
        if form.answer.data == quiz.correct_option:
            flash('Given answer is correct!','success')
            return redirect(url_for('home'))
        else:
            flash('Given answer is wrong. Try again','danger')
            return redirect(url_for('home'))
    return render_template('quiz.html', title=quiz.title, quiz=quiz, form=form)

@app.route("/search", methods=['GET', 'POST'])
def search():
    form=SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('result',searched_username=form.user.data))
    return render_template('search.html',form=form)

@app.route("/result/<searched_username>")
def result(searched_username):
    users=User.query.filter_by(username=searched_username).all()
    return render_template('result.html',users=users)