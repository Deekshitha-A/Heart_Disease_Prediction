from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import numpy as np
import pickle
import forms
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_manager, UserMixin, logout_user, login_required
model=pickle.load(open('model.pkl', 'rb'))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///display.db'
app.config['SECRET_KEY'] = '389b960c82f8f46cc6f51cdf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return userlogin.query.get(int(user_id))


class userlogin(db.Model, UserMixin):
    id = Column(Integer(), primary_key=True)
    username = Column(String(length=30), nullable=True, unique=True)
    email = Column(String(length=40), nullable=True, unique=True)
    pwd = Column(String(length=40), nullable=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, pt):
        self.pwd = bcrypt.generate_password_hash(pt).decode('utf-8')

    def checkpassword(self, entered):
        return bcrypt.check_password_hash(self.pwd, entered)


class User(db.Model):
    id = Column(Integer(), primary_key=True)
    name = Column(String(length=30), nullable=False, unique=True)
    age = Column(Integer(), nullable=False)

    def __repr__(self):
        return f'User {self.name}'


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/predict', methods=['GET',  'POST'])
@login_required
def predict():
    #users = userlogin.query.all()
    form = forms.Predict()
    sample = 1
    if request.method == "POST":
    #if form.validate_on_submit():
        li = [int(form.Age.data), int(form.Gender.data), int(form.ChestPainType.data), int(form.RestingBP.data), int(form.Cholesterol.data),
              int(form.FastingBS.data), int(form.RestingECG.data), int(form.MaxHR.data), int(form.ExerciseAngina.data), int(form.Oldpeak.data),
              int(form.ST_Slope.data)]
        final = [np.array(li)]
        prediction = model.predict(final)
        output = round(prediction[0])
        output = str(output)
        if output == '1':
            flash("Likely to have Heart disease", category="danger")
        else:
            flash("Not likely to have Heart disease", category="success")
        return redirect(url_for('predict',  info=output, sample=sample))
    #else:
        #flash("hello", category="success")'''
    return render_template('predict.html', form=form)


@app.route('/')
@app.route('/login', methods=['GET',  'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        new = userlogin.query.filter_by(username=form.username.data).first()
        if new and new.checkpassword(entered=form.pwd.data):
            login_user(new)
            flash(f'Successfully logged in as :{new.username}', category='success')
            return redirect(url_for('predict'))
        else:
            flash('Username and password not matched! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.Register()
    if form.validate_on_submit():
        create = userlogin(username=form.username.data,
                           email=form.email.data,
                           password=form.pwd1.data)
        db.session.add(create)
        db.session.commit()
        login_user(create)
        flash(f'Account created successfully! You are now logged in as :{create.username}', category='success')
        return redirect(url_for('predict'))

    if form.errors != {}:
        for i in form.errors.values():
            flash(i)
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!',category='info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)