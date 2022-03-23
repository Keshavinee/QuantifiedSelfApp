from .database import db

class userinfo(db.Model):
	__tablename__ = 'userinfo'
	username = db.Column(db.String, nullable=False, primary_key=True,)
	age = db.Column(db.Integer, nullable=False)
	password = db.Column(db.String, nullable=False)

class tracker(db.Model):
	__tablename__ = 'tracker'
	user = db.Column(db.String, db.ForeignKey("userinfo.username"), primary_key=True)
	tname = db.Column(db.String, primary_key=True)
	desc = db.Column(db.String)
	dtype = db.Column(db.String, nullable=False)
	setting = db.Column(db.String)
		
class trackinfo(db.Model):
	__tablename__ = 'trackinfo'
	user = db.Column(db.String, db.ForeignKey("userinfo.username"), primary_key=True)
	tname = db.Column(db.String, db.ForeignKey("tracker.tname"), primary_key=True)
	on = db.Column(db.DateTime, primary_key=True)
	value = db.Column(db.String , nullable=False)
	notes = db.Column(db.String)
