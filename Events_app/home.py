from flask import Flask,render_template,redirect,url_for,request,send_file,flash
from forms import Add_event
from werkzeug.utils import secure_filename
import os,urllib.request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'b7779335d0d83b657348daee94fd2468'
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)




# ---------- DB ---------

class Event(db.Model):
	id 		= db.Column(db.Integer,primary_key=True)
	name 	= db.Column(db.String(20),unique=False,nullable=False)
	content =  db.Column(db.String(500),unique=False,nullable=False)
	address =  db.Column(db.String(100),unique=False,nullable=False)
	start_date =  db.Column(db.Date,unique=False,nullable=False,default=datetime.utcnow)
	end_date =  db.Column(db.Date,unique=False,nullable=False,default=datetime.utcnow)
	category =  db.Column(db.String(50),unique=False,nullable=False)
	image_file =  db.Column(db.String(100),unique=False,nullable=False,default="default.jpg")
	album_file =  db.Column(db.String(1000),unique=False,nullable=False,default="default.jpg")

	def __repr__(self):
		return f"name:{self.name}, content:{self.content},category:{self.category},img:{self.image_file},album:{self.album_file}"

# ----------------------





@app.route('/')
def home():

	event = Event()
	events = Event.query.all()
	return render_template('home.html',title='Home',events=events)

@app.route('/add_event')
def add_event():
	form = Add_event()
	return render_template('add_event.html',form=form,title='Add new event',legend="Create Event")




@app.route('/', methods=['POST'])
def upload_image():
	form = Add_event()
	if form.validate_on_submit():
	    file = request.files['photo']
	    photo_album = request.files.getlist('photo')[1:]
	    album = ""
	    for i in range(len(photo_album)):
	    	if(i == 0):
	    		album+=photo_album[i].filename
	    	else:
	    		album+= "," + photo_album[i].filename



	    print(album.split(','))

	    event = Event(name=form.name.data,address=form.address.data,content=form.content.data,
	    	category=form.category.data,image_file=file.filename,
	    	start_date=form.startDate.data,end_date=form.endDate.data,album_file=album)

	    db.session.add(event)
	    db.session.commit()
	    if file :
	        filename = secure_filename(file.filename)
	        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	        for photo in photo_album:
	        	if photo:
	        		photoname = secure_filename(photo.filename)
	        		photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photoname))

	        #print('upload_image filename: ' + filename)
	        flash(f'Event created successfully','success')


	        return redirect(url_for('home'))
	    else:
	        return redirect(request.url)

@app.route('/<int:event_id>/update',methods=["GET","POST"])
def update_event(event_id):
	event = Event.query.get_or_404(event_id)	
	
	form = Add_event()

	if form.validate_on_submit():
		file = request.files['photo']

		event.name = form.name.data
		event.contnet = form.content.data
		event.address = form.address.data
		event.category = form.category.data
		event.image_file = file.filename
		event.start_date = form.startDate.data
		event.end_date = form.endDate.data

		db.session.commit()
		flash('Your Event has been updated !','success')
		return redirect(url_for('home'))

	elif request.method == 'GET':
		form.name.data = event.name
		form.content.data = event.content
		form.address.data = event.address
		form.category.data = event.category
		form.photo.data = event.image_file
		form.startDate.data = event.start_date
		form.endDate.data = event.end_date

	return render_template('update_event.html',form=form,title='update event',legend='Update Event')


@app.route('/<int:event_id>/delete',methods=["POST"])
def delete_event(event_id):
	event = Event.query.get_or_404(event_id)	
	db.session.delete(event)
	db.session.commit()

	flash('Your Event has been deleted !','success')
	return redirect(url_for('home'))



@app.route('/<int:event_id>/show_event')
def show_event(event_id):
	event = Event.query.get_or_404(event_id)
	
	return render_template('event_album.html',title='album',event=event)


if __name__ == '__main__':
	app.run(debug=True)