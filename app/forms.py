from flask.ext.wtf import Form
from flask.ext.uploads import UploadSet, IMAGES
from wtforms import TextField, BooleanField, StringField, PasswordField, TextAreaField, SubmitField
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

images = UploadSet('images', IMAGES)

class EditProfile(Form):
	about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])

class EditAvatar(Form):
	avatar = FileField("file")
	submit = SubmitField("Send")




