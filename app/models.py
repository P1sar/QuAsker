from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password = db.Column(db.String(120))
	last_seen = db.Column(db.DateTime)
	reg_date = db.Column(db.DateTime)
	question = db.relationship("Question", backref = "author", lazy = "dynamic" )
	answer = db.relationship("Answer", backref = "author", lazy = "dynamic")

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

	def __repr__(self):
		return "<Post %r>" % (self.body)

class Answer(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
	ans_time = db.Column(db.DateTime)
