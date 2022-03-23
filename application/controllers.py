from flask import Flask, request
from flask import render_template, url_for, redirect
from flask import current_app as app
from application.models import userinfo, tracker, trackinfo
from sqlalchemy import or_,and_
from datetime import datetime,date,timedelta
import matplotlib.pyplot as plt
from .database import db

@app.route("/", methods=["GET", "POST"])
def options():
    return render_template("options.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
    	return render_template("login.html")
    
    elif request.method == "POST":
    	usr = request.form["usr"]
    	pwd = request.form["pwd"]
    	user = db.session.query(userinfo).filter_by(username=usr,password=pwd).first()
    	
    	if user:
    		return redirect(url_for('track',username=usr))
    	else:
    		return render_template("w3.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
    	return render_template("signup.html")
    
    elif request.method == "POST":
    	usr = request.form["usr"]
    	age = request.form["age"]
    	pwd = request.form["pwd"]
    	
    	new_user = db.session.query(userinfo).filter_by(username=usr).first()
    	
    	if new_user:
    		return render_template("w1.html")
    		
    	else:
    		if len(pwd) < 6:
    			return render_template("w2.html")
    			
    		new_usr = userinfo(username=usr,age=age,password=pwd)
    		db.session.add(new_usr)
    		db.session.commit()
    		
    	return redirect(url_for('options'))

@app.route("/<username>/tracker", methods=["GET", "POST"])
def track(username):
	events = db.session.query(tracker.tname).filter_by(user=username).all()
	lst = []
	
	if events:
		for e in events:
			ltrck = db.session.query(tracker,trackinfo).\
				outerjoin(trackinfo,and_(tracker.user==trackinfo.user,tracker.tname==trackinfo.tname)).\
				filter(tracker.user==username,tracker.tname==e[0]).order_by(trackinfo.on.desc()).first()

			print(ltrck)
			if ltrck:
				lst.append(ltrck)
		return render_template("tracker.html",username=username,trackers=lst)
	return render_template("tracker2.html",username=username)
 	
@app.route("/<username>/create", methods=["GET", "POST"])
def create(username):
	if request.method == "GET":
		return render_template("create.html",username=username)
		
	elif request.method == "POST":
    		name = request.form["name"]
    		desc = request.form["desc"]
    		dtype = request.form["type"]
    		settng = request.form["setting"]
    		
    		new_trck = db.session.query(tracker).filter_by(user=username,tname=name).first()
    		
    		if not new_trck:
    			new = tracker(user=username,tname=name,desc=desc,dtype=dtype,setting=settng)
    			db.session.add(new)
    			db.session.commit()
    		return redirect(url_for('track',username=username))

@app.route("/<username>/<tracker>", methods=["GET", "POST"])
def graph(username, tracker):
	if request.method == "GET":
		return render_template("period.html",username=username,tname=tracker)
		
	elif request.method == "POST":
    		pd = request.form["period"]	
    		today = (date.today()).strftime("%Y-%m-%d")
    		
    		if pd=="today":
    			value = []; on = []
    			search = "{}%".format(today)
    			l = db.session.query(trackinfo).filter(trackinfo.user==username,trackinfo.tname==tracker,trackinfo.on.like(search)).all()

    			for row in db.session.query(trackinfo).filter(trackinfo.user==username,trackinfo.tname==tracker,trackinfo.on.like(search)).all():
    				value.append(row.value)
    				on.append(row.on)
    			
    			plt.title('Today\'s graph')
    			plt.xlabel('timestamp')
	    		plt.ylabel('value')	
	    		plt.plot(on, value)
	    		plt.savefig('static/graph.png')
	    		value = []; on = []
    				
    		elif pd=="week":
    			value = []; on = []
    			today = date.today()
    			a = (today - timedelta(days=today.weekday()))
    			b = (a + timedelta(days=1))
    			c = (a + timedelta(days=2))
    			d = (a + timedelta(days=3))
    			e = (a + timedelta(days=4))
    			f = (a + timedelta(days=5))
    			g = (a + timedelta(days=6))
    			a1 = "{}%".format(a.strftime("%Y-%m-%d"))
    			b1 = "{}%".format(b.strftime("%Y-%m-%d"))
    			c1 = "{}%".format(c.strftime("%Y-%m-%d"))
    			d1 = "{}%".format(d.strftime("%Y-%m-%d"))
    			e1 = "{}%".format(e.strftime("%Y-%m-%d"))
    			f1 = "{}%".format(f.strftime("%Y-%m-%d"))
    			g1 = "{}%".format(g.strftime("%Y-%m-%d"))
    			l = db.session.query(trackinfo).filter(trackinfo.user==username,trackinfo.tname==tracker,or_(trackinfo.on.like(a1),trackinfo.on.like(b1),trackinfo.on.like(c1),trackinfo.on.like(d1),trackinfo.on.like(e1),trackinfo.on.like(f1),trackinfo.on.like(g1))).all()
    			for row in db.session.query(trackinfo).filter(trackinfo.user==username,trackinfo.tname==tracker,or_(trackinfo.on.like(a1),trackinfo.on.like(b1),trackinfo.on.like(c1),trackinfo.on.like(d1),trackinfo.on.like(e1),trackinfo.on.like(f1),trackinfo.on.like(g1))).all():
    				value.append(row.value)
    				on.append(row.on)
    			plt.title('This week\'s graph')
    			plt.xlabel('timestamp')
	    		plt.ylabel('value')	
	    		plt.plot(on, value)
	    		plt.savefig('static/graph.png')
	    		value = []; on = []
    			
    		else:
    			value = []; on = []
    			month = (date.today()).strftime("%Y-%m")
    			search = "{}%".format(month)
    			l = db.session.query(trackinfo).filter(trackinfo.user==username,trackinfo.tname==tracker,trackinfo.on.like(search)).all()
 
    			for row in db.session.query(trackinfo).filter(trackinfo.user==username,trackinfo.tname==tracker,trackinfo.on.like(search)).all():
    				value.append(row.value)
    				on.append(row.on)
    			plt.title('This month\'s graph')
    		
	    		plt.xlabel('timestamp')
	    		plt.ylabel('value')	
	    		plt.plot(on, value)
	    		plt.savefig('static/graph.png')
	    		value = []; on = []

    		return render_template("period3.html",username=username,tname=tracker,trackers=l)
    				
@app.route("/<username>/<tracker>/add", methods=["GET", "POST"])
def add(username, tracker):
	if request.method == "GET":
		return render_template("add.html",username=username,tracker=tracker)
		
	elif request.method == "POST":
    		when = datetime.strptime(request.form["on"], "%Y-%m-%d %H:%M:%S")
    		value = request.form["value"]
    		notes = request.form["notes"]
    		
    		new_log = db.session.query(trackinfo).filter_by(user=username,tname=tracker,on=when).first()
    		
    		if not new_log:
    			new = trackinfo(user=username,tname=tracker,on=when,value=value,notes=notes)
    			db.session.add(new)
    			db.session.commit()
    		return redirect(url_for('track',username=username))

@app.route("/<username>/<track>/edit", methods=["GET", "POST"])
def edit(username, track):
	if request.method == "GET":
		t=db.session.query(tracker).filter_by(user=username,tname=track).first()
		return render_template("editt.html", t=t)
		
	elif request.method == "POST":
		desc = request.form["desc"]
		setting = request.form["setting"]
		
		db.session.query(tracker).filter_by(user=username,tname=track).\
			update({"desc":desc,"setting":setting},synchronize_session = False)
		db.session.commit()
			
		return redirect(url_for('track',username=username))
			
@app.route("/<username>/<track>/delete", methods=["GET", "POST"])
def delete(username, track):
	r = db.session.query(tracker).filter_by(user=username,tname=track).first()
	db.session.delete(r)
	db.session.commit()

	db.session.query(trackinfo).filter_by(user=username,tname=track).delete(synchronize_session=False)
	db.session.commit()

	return redirect(url_for('track',username=username))

@app.route("/<username>/<tracker>/<on>/edit", methods=["GET", "POST"])
def editon(username, tracker, on):
	on = datetime.fromisoformat(on)
	search = "{}%".format(on)
	if request.method == "GET":
		log = db.session.query(trackinfo).filter(trackinfo.user==username,trackinfo.tname==tracker,trackinfo.on.like(search)).first()
		print(log)
		return render_template("editlog.html", t=log)
		
	elif request.method == "POST":
		when = request.form["on"]
		when = datetime. strptime(when,'%Y-%m-%d %H:%M:%S')
		value = request.form["value"]
		notes = request.form["notes"]
		
		db.session.query(trackinfo).filter_by(user=username,tname=tracker,on=search).\
			update({"on":when,"value":value,"notes":notes},synchronize_session = False)
		db.session.commit()
			
		return redirect(url_for('graph',username=username,tracker=tracker))
			
@app.route("/<username>/<tracker>/<on>/delete", methods=["GET", "POST"])
def deleteon(username, tracker, on):
	on = datetime.fromisoformat(on)
	search = "{}%".format(on)
	log = db.session.query(trackinfo).filter(trackinfo.user==username,trackinfo.tname==tracker,trackinfo.on.like(search)).first()
	
	if log:
		db.session.delete(log)
		db.session.commit()
	return redirect(url_for('graph',username=username,tracker=tracker))

