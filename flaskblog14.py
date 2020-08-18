def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the fourteenth note on building a python flask application *
~lb(0): turning flaskblog__.py into a package
~lb(1): ### RENAMED TO run.py ###

'''

if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# now flaskblog13.py was the run-through of the problem itself,
# but the solution to this is a lot easier than the above deep-dive analysis of the problem.
#(the deep-dive was just to justify why you're restructuring this project into packages, which is going to fix this)

# a good explanation of these import issues can be found in miguel grinberg's 'flask at scale' talk
# from pycon 2016. url: https://youtu.be/tdIIJuPh3SI

# ok, so the solution here is to set up your code whereby you're not running flaskblog13 directly.
# that way, it won't get that name of __main__.

# and the way you're going to do this is to turn your application into a package.

# using a package will make all of these imports more simple
# and allow you separate things out better than you've done up till now.

# in order to tell python that your directory is a package,
# you just need to create a __init__ file.
# go ahead and create a package with the name of your application:

# 1: create a folder within the project directory with the name of your application (flaskblog).
# 2: within this folder, create a __init__ file (__init__.py)

# now you have a new package with the name of your application;
# let's move some of your current project into this new package, except for the module(s) named flaskblog00/01//02.py etc.
#(meaning forms.py, models.py, static, templates)

# n.b. don't worry about the pycache, it's something that just gets created.
# you can delete that for now.

# now, within your project directory,
# you have the application code modules (flaskblog__.py) and the flaskblog package.

# you now want to go ahead and open up your __init__.py file;
# which will be where you initialise your application, and bring together different components.

# you can go ahead and open up flaskblog13.py module and separate out certain parts:

# 1: go ahead and cut from the imports all the way down to where you're creating the instance of db:

# this part #
'''

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key hidden for github'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

'''

# and now, paste those into the __init__.py file

# then, in the application module (flaskblog14.py),
# you're left with a lot of your route information
# which are beckoning to be separated out into their own modules too!
#(so that everything has its own place)

# go ahead and create a new file within the package folder (flaskblog)

# and name it 'routes.py',
# after which cut all the part (starting from the 'import models' to the dummy post data and) routes:
'''
from models import User, Post

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

'''
# as you can see, you want to copy basically everything apart from the conditional 'if __name__ == '__main__'


lb(1)
# now, all you're left with in the application file (flaskblog14.py)
# is what you're using the run the application.

# let's leave this here, and when you want to test what you've got,
# you'll still be running this file,
# whose only job is to grab the app and run it.

# first of all,
# since running the application is the only purpose of this file now,
# let's rename this file (flaskblog14.py) to run.py
# that way you don't confuse the name of that module with your new package that is now named flaskblog.


# # # # # # # # # # # # # # # # continue onto flaskblog15.py (or run.py) # # # # # # # # # # # # # # # #
