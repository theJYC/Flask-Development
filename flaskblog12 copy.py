def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the twelveth note on building a python flask application *
~lb(0): creating the database with the database models in place
~lb(1): querying the database
~lb(2): capturing the query into a variable
~lb(3): db.relationship in action
~lb(4): removing the content of the database & starting anew

'''
#____________from previous flask notes (+ modification)____________

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key hidden for github'

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
                            lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def __repr__(self):
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
# now that you have these database models (that represent the structure of your database),
# you can now use those to create a database.

# so, navigate to terminal in your project directory and type in the following commands:

# from flaskblog import db
# db.create_all()

# and you'll notice that you now have a site.db file in the directory.

# so now you have the database, but it's currently empty.
# it's easy to add data to your database using the commandline.

# now, you'll be using your application to be adding this data later,
# but let's go ahead and add your User and your Post, just so you can see how this works.

# return to Terminal, and type:
# 1: from flaskblog12 import User, Post

# 2: user_1 = User(username='JinYoung', email='jyc@gmail.com', password='password')
# creating an instance of a User by passing in all the attributes that it needs.

# n.b. you're setting a plaintext password in this example,
# but you're going to be hashing these passwords when you do this through your application.

# n.b.2. also notice that you didn't specify an id or an image_file for this user_1 instance.
# since id is your primary key, it'll assign a unique id to the user automatically.
# and you also have a default value for the image_file, so if you don't provide one,
# it'll just get that value from default.jpg that you specified in your model.

# 3: db.session.add(user_1)
# this code tells your database that you're going to want to add user_1 to your database (site.db)

# now #3 hasn't actually added the user to your database;
# rather, you told it that you have a change that you want to make to your database.

# i.e. you could have several changes at a time and add them like this
# and then when you commit those changes, it'll make the changes to the database all at once.

# e.g. if you add user_2:

# 4: user_2 = User(username='Fredrick', email='ft@gmail.com', password='password')
#(first create the user)

# 5: db.session.add(user_2)
#(then add the user)

# 6:db.session.commit()
#(and finally commit the adds to the database)

lb(1)
# now that they are committed, they should now actually be in the database
# and SQLAlchemy makes querying the database extremely easy.

# let's look at a couple of common queries:

# a) if you want to just get all of your users:

# User.query.all()
#returns: [User('JinYoung', 'jyc@gmail.com', 'default.jpg'), User('Fredrick', 'ft@gmail.com', 'default.jpg')]

# b) if you want to just get the first user:

# User.query.first()
#returns: User('JinYoung', 'jyc@gmail.com', 'default.jpg')

# c) you can also filter the results (e.g. by username='JinYoung'):

# User.query.filter_by(username='JinYoung').all() *
#returns: [User('JinYoung', 'jyc@gmail.com', 'default.jpg')]
# you can see that you get a list of one user with that matching username 'JinYoung'

# n.b. now if there are multiple people with that same username it should return all of them,
# though that should never happen in your application because each username is unique.

# *instead of the .all() method, you can also do .first() method.
#i.e. User.query.filter_by(username='JinYoung').first()

lb(2)
# let's look at this user that is getting returned.

# use the command that you used above, capture it inside a variable:

'''user = User.query.filter_by(username='JinYoung').first()'''

# your 'user' is that user_1 that was returned from that query,
# but now you should have access to some additional attributes:

# you could say

'''user.id'''
#returns: 1

# now you can actually perform queries using the id aswell:
# you already saw User.query.all() and User.query.first()

# but if you were to say:

''' user = User.query.get(1) '''
''' user '''
#returns: User('JinYoung', 'jyc@gmail.com', 'default.jpg')
# this would fetch a user with a specific id of 1


# now, to look at this user's posts:

'''user.posts'''
#returns: []
# this returns an empty list because this user does not have any posts at the moment.

# remember when you wrote your models;
# the posts attribute is not actually a column itself.
# that is actually running an additional query on the posts table
# that grabs any post from that user

# let's create some posts written by this user to see what this looks like:

# 1: post_1 = Post(title='Blog 1', content='First Post Content!', user_id=user.id)

# note: notice that you didn't specify a date when you created this post
# if you remember from models.py, you have a default date of utc_now
# so it should populate the date with the current utc time if you didn't provide anything.

# now let's add one more post that is similar to post_1:

# 2: post_2 = Post(title='Blog 2', content='Second Post Content!', user_id=user.id)

# 3: db.session.add(post_1)
# 4: db.session.add(post_2)
# 5: db.session.commit()

# now that these posts are committed to the database, let's take a look at the user's posts again

# 6: user.posts
#returns: [Post('Blog 1', '2020-08-18 05:37:48.785459'), Post('Blog 2', '2020-08-18 05:37:48.786713')]
# you can see that this user has two blog posts (Blog 1, Blog 2).
# this result is just a list, meaning that you can loop through this like any other lists.

# 7: for post in user.posts:
#       print(post.title)

# returns:
'''
Blog 1
Blog 2
'''

lb(3)
# now let's get the first of these posts by actually querying the post table directly:

# 1: post = Post.query.first()
# 2: post

#returns: Post('Blog 1', '2020-08-18 05:37:48.785459')

# now you can get the id of the user who created this post just by accessing this column:

# post.user_id
#returns: 1

# you got the right id for the user who created this post,
# but in the post table, that's the only information about the user that you have.

# you might want more information about the author.

# if you remember back at models.py,
# the posts db.relationship() from the User db.Model not only let's you access a user's post
# but also adds this backref='author' to each post.

# and that's not an actual column down in the Post db.Model,
# but it allows you to use that to access the user who created the post.

# returning to the command line:

#: post.author
#returns: User('JinYoung', 'jyc@gmail.com', 'default.jpg')

# you can see that you get the entire user object that you can work with.

# that's an extremely nice feature with SQLAlchemy.

lb(4)
# now that you've added some sample data to make sure that everything was working properly,
# let's delete all that data so that in the next note you are starting with a nice clean database:

# 1: db.drop_all()
# 2: db.create_all()

# 1- drops all of your database's tables and rows.
# 2- recreates that database structure


# # # # # # # # # # # # # # # # continue onto flaskblog13.py # # # # # # # # # # # # # # # #
