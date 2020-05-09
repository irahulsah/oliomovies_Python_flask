from flask import Flask,render_template,request,redirect ,session

from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from send_mail import send_mail

with open('config.json', 'r') as c:
    info = json.load(c)["info"]

app = Flask(__name__)
app.secret_key = 'super-secret key'
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9865103845H@localhost/rahul'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] =''
    

db = SQLAlchemy(app)


class Contacts(db.Model):
    __tablename__ = 'contacts'
    sno = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    # Phone = db.Column(db.String(13), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    Date = db.Column(db.String(40), nullable=True)

    def __init__(self, movie_name, email,  message, Date):
        self.movie_name = movie_name
        self.email = email
        # self.Phone = Phone  
        self.message = message 
        self.Date = Date

class Posts(db.Model):
    __tablename__ = 'posts'
    sno = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(10), nullable=False)
    front_image = db.Column(db.String(40), nullable = False)
    back_image = db.Column(db.String(40), nullable = False)
    back_title =db.Column(db.String(50), nullable=False)
    back_text  = db.Column(db.String(1000), nullable = False)
    back_link  = db.Column(db.String(2000), nullable = False)
    Date = db.Column(db.String(30), nullable =True)

    def __init__(self , id, front_image,  back_image, back_title, back_text, back_link,  Date):
        self.id = id
        self.front_image = front_image
        
        self.back_image = back_image
        self.back_title = back_title
        self.back_text = back_text
        self.back_link = back_link
        self.Date = Date

@app.route('/')
def home():
    posts = Posts.query.filter_by().all()[0:4]


    
    return render_template('index.html', info = info, posts=posts)
@app.route('/about')
def about():


    
    return render_template('about.html', info = info)
@app.route('/movies')
def movies():
    posts = Posts.query.filter_by().all()


    
    return render_template('movies.html', info = info, posts =posts)






  


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/contacts' , methods = ['GET','POST'])
def contacts():

    if (request.method == 'POST'):
        movie_name = request.form.get('name')
        email = request.form.get('email')
        # phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(movie_name = movie_name , email = email ,  message = message , Date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        send_mail(movie_name, email, message)
        

    return render_template('contacts.html', info = info )



@app.route('/login' ,methods = ['GET', 'POST'])
def login():
    if ('user' in session and session['user'] == info['user_name']):
        posts = Posts.query.all()
        return render_template('dashboard.html', info = info,  posts = posts)




    if (request.method == 'POST'):
        username = request.form.get('uname')
        password = request.form.get('Pass')
        if (username == info['user_name'] and password == info['password']):
            
            session['user'] = username
            posts = Posts.query.all()


            return render_template('dashboard.html', info = info, posts = posts)
    return render_template("login.html"  ,info = info)


@app.route("/edit/<string:sno>", methods = ['GET' , 'POST'])
def edit(sno):
    if ('user' in session and session['user'] == info['user_name']):



        if (request.method == 'POST'):
        # front_image, back_image, back_text, Date
            id = request.form.get('id')
            front_image = request.form.get('front_image')
            
            back_image = request.form.get('back_image')
            back_title = request.form.get('back_title')
            back_text = request.form.get('back_text')
            back_link = request.form.get('back_link')
            Date = datetime.now()

            
            
            if sno == '0' :
                post = Posts(id = id,front_image = front_image  ,back_image = back_image , back_title = back_title,  back_text = back_text , back_link= back_link, Date = Date )
                db.session.add(post)
                db.session.commit()

            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.id = id
                post.front_image = front_image
                post.back_image = back_image
                post.back_title = back_title
                post.back_text = back_text
                post.back_link = back_link
                post.Date = Date
                db.session.commit()
                return redirect('/edit/'+ sno)
    

        post = Posts.query.filter_by(sno=sno).first()

        return render_template("edit.html",info = info, post =post, sno=sno)



@app.route("/delete/<string:sno>", methods = ['GET' , 'POST'])
def delete(sno):


    # if ('user' in session and session['user'] == info['user_name']):
    post = Posts.query.filter_by(sno=sno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/login')
    
    return render_template('dashboard.html', info = info)


if __name__ == "__main__":

 



    app.run()