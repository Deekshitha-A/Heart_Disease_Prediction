from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
import main


class Register(FlaskForm):
    def validate_username(self, checkname):
        user = main.userlogin.query.filter_by(username=checkname.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, checkemail):
        mail = main.userlogin.query.filter_by(email=checkemail.data).first( )
        if mail:
            raise ValidationError('E-mail already exists')
    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    pwd1 = PasswordField(label='Password:', validators=[Length(min=3), DataRequired()])
    pwd2 = PasswordField(label='Confirm Password:', validators=[EqualTo('pwd1'), DataRequired()])
    submit = SubmitField(label='Create')


class LoginForm(FlaskForm):
    username = StringField(label='Username:',validators=[DataRequired()])
    pwd = PasswordField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class Predict(FlaskForm):
    Age= IntegerField(label='Age', validators=[DataRequired()])
    Gender= IntegerField(label='Gender', validators=[DataRequired()])
    ChestPainType = IntegerField(label='ChestPainType', validators=[DataRequired()])
    RestingBP = IntegerField(label='RestingBP', validators=[DataRequired()])
    Cholesterol = IntegerField(label='Cholesterol', validators=[DataRequired()])
    FastingBS = IntegerField(label='FastingBS', validators=[DataRequired()])
    RestingECG = IntegerField(label='RestingECG', validators=[DataRequired()])
    MaxHR = IntegerField(label='MaxHR', validators=[DataRequired()])
    ExerciseAngina = IntegerField(label='ExerciseAngina', validators=[DataRequired()])
    Oldpeak = FloatField(label='Oldpeak', validators=[DataRequired()])
    ST_Slope = IntegerField(label='ST_Slope', validators=[DataRequired()])
    submit = SubmitField(label='Predict')
