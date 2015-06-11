from app import db
from flask.ext.login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password = db.Column(db.String(120))
	last_seen = db.Column(db.DateTime)
	about_me = db.Column(db.String(140))
	reg_date = db.Column(db.DateTime)
	question = db.relationship("Question", backref = "author", lazy = "dynamic" )
	answer = db.relationship("Answer", backref = "author", lazy = "dynamic")
	root = db.Column(db.Boolean, default = False)



	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False


	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Question(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title  = db.Column(db.String(140))
	body = db.Column(db.Text)
	post_time = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	answer = db.relationship("Answer", backref ="answer", lazy = "dynamic" )
	#category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

	def __repr__(self):
		return self.title

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	#question_id = db.relationship("Question", backref = "question", lazy = "dynamic")

class Answer(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
	ans_time = db.Column(db.DateTime)
	votes = db.Column(db.Integer, default = 0)
	voted_users_id = db.Column(db.String, default = "")
