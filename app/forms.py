from flask.ext.wtf import Form
from wtforms  import TextField, BooleanField, StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import Required, Email, Length, equal_to
from flask_wtf.file import  FileField, FileAllowed, FileRequired
class LoginForm(Form):

	email = StringField("Email",  validators = [Required(),
												Email(message="Enter a valid email address")])
	password = PasswordField("Password", validators = [Required(),
														Length(min=5, max=15)])
	remember_me = BooleanField('remember_me', default = False)

class RegisterForm(Form):

	email = StringField("Email",default="example@mail.com", validators = [Required(),
												Email(message="Enter a valid email address")])
	password = PasswordField("Password", validators = [Required(),
														Length(min=5, max=15)])

	repeat_password = PasswordField("RepeatPassword", validators = [Required(),
																	equal_to("password",
																	message="Passwords must be equal")]) 																
	nickname = StringField("nick", validators = [Required(),
												Length(min=3, max=10)])



class EditProfile(Form):
	about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])

class EditAvatar(Form):
	avatar = FileField("file")
	submit = SubmitField("Send")


class AskQuestion(Form):
	question_title = StringField("Title",validators = [Required(), Length(min = 0, max = 50)])
	question_body = TextAreaField("Question", validators = [Required(), Length(min = 0, max = 9999)])
	question_submit = SubmitField("Ask")


class WriteAnswer(Form):
	answer_body = TextAreaField("Answer", validators = [Required()])
	answer_submit = SubmitField("Answer")

class SearchForm(Form):
    search = TextField('search', validators = [Required()])



