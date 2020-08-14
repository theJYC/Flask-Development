def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the eleventh note on building a python flask application *
~lb(0): class models and database structure (2: creating a Post class)
~lb(1): one-to-many relationship (db.relationship('many', backref='x', lazy=True))
~lb(2): db.Column(db.ForeignKey('one.attribute'))

'''
#____________from previous flask notes (+ modification)____________


from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # refer to line C

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key removed for github'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,
                         nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author',
                            lazy=True)  # refer to line F

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):  # refer to line A
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)  # refer to line B
    content = db.Column(db.Text, nullable=False)  # refer to line D
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)  # refer to line G

    def __repr__(self):  # refer to line E
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author': 'Jin Young Choi',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 3, 2020'
    },
    {
        'author': 'Fredrick Thompson',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 4, 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:

            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)


#_________________________end of app code_________________________

lb(0)
# now let's create your class Post(db.Model), which will hold your posts.

# Line A: this will be quite similar to the class User (db.Model), also being equipped the id db.Column.

# and this time you'll want a title db.Column, with a db.String length of (100), nullable=False

# Line B: and now, a date_posted db.Column to hold the date that your post was made,
# whereby the type (first argument) of this column will be db.DateTime.
# also make sure that each of the column will need to have a date_posted, so nullable=False,

# and you'll also want a default for this aswell;
# so if you don't actually specify a date for when your post was created, you can just say that it was created at the current time.

# Line C: to get the current time, you're going to have to import the datetime class from datetime module

# with the datetime module imported,
# return to the date_posted db.Column, and pass in the default=datetime.utcnow .

# n.b. take caution not to pass in datetime.utcnow() (with the added parentheses)
# because doing so will call the datetime.utcnow method now (as you build the app (cmd + b)) instead of when the user posts.
# i.e. you don't want the parentheses there because you want to pass in the function as the argument, and not the current time.

# n.b.2: and you also want to use utc times when saving dates and times to a database, so that they are consistent

# Line D: and now, the last db.Column in the class Post() will be content.
# and the type of this db.Column will be db.Text (instead of db.String)
# again, set nullable=False since content will be required for every post, and save this column.

# and now, to finish off the class Post(db.Model):, put in the dunder repr method here aswell,
# Line E: whereby you want to print out the title and the date_posted so you can see those values of each instance.
# note: you don't want to print out the content since, logically speaking, this can get very long,
# and if you're looping through posts and printing those all out, you'd just want a short description that has ample info. (i.e. title & date)

lb(1)
# one thing that you may have noted is that you haven't yet added the author to your Post model yet.

# the Post model and the User model are going to have a relationship,
# since User's will author Post's.

# specifically, this is going to be called a 'One-to-Many' relationship,
# because one user can have multiple posts, but a post can only have one author.

# so this is how it's done in SQLAlchemy:

# up in your class User(db.Model):,

# Line F: create a posts attribute, whereby it will be set to (not a db.Column, but) a db.relationship
# and now pass in the string of 'Post' (to say that this posts attribute has a relationship with your Post db.model),
# and now specify a backref='author', and also pass in the lazy=True argument.

# ok, so this is saying that the posts attribute has a relationship to the Post model,
# now the backref is similar to adding another db.Column to the Post model.

# what the backref allows you do is, when you have a post,
# you can simply use this author attribute to get the user who created the post.
#(and if that doesn't make sense yet, you'll see this in action in just a bit!)

# now, the lazy argument just defines when SQLAlchemy loads the data from the database.
# hence, lazy=True means SQLAlchemy will load the data as necessary in one go
# this is convenient because, with this relationship,
# you'll be able to simply use this posts attribute to get all of the posts created by an individual user.

# note: this is, once again, a db.relationship, not a db.Column.
# which means that, if you were to actually look at your database structure in some kind of SQL client,
# you wouldn't see this posts column here.

# i.e. this is actually just running an additional query in the background that will get all of the posts this user has created.

lb(2)
# now, to specify the user in the Post model,
# you can add the user_id for the author.

# within class Post(db.Model):,
# Line G: set user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# db.ForeignKey meaning that this user_id has a relationship with the User model.
# within the db.ForeignKey argument, you specify what the relationship is with exactly 'user.id'*

# now, it would be required that each post has an author, so you're also going to pass in a nullable=False.


# * 'user.id' is going to be the id of the user who authored the post.
# note: it might be a little bit confusing because you're a using an uppercase 'P' for Post
# in the User model when you're defining the relationship with the Post class (refer to line F)
# but in the case of Line G, you're using a lowercase 'u' for the user.id in the Post model.

# that is because, in the User model (line F), you're referencing the actual Post class,
# whereas in the ForeignKey, you're actually referencing the table name and the column name, so it's a lowercase.

# ** so the User model automatically has this tablename set to lowercase 'user', **
# ** and the Post model will have a tablename automatically set to lowercase 'post' **

# n.b. if you want to set your own tablenames, then you can set a specific tablename attribute,
# but since your models are pretty simple, you'll just leave those as the default lowercase values.


# # # # # # # # # # # # # # # # continue onto flaskblog12.py # # # # # # # # # # # # # # # #
