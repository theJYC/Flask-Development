def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the thirteenth note on building a python flask application *
~lb(0): restructuring an application into a package
~lb(1): circular import
~lb(2): importing modules: behind the scenes
~lb(3): if flaskblog.py != __main__.py

'''

#____________from previous flask notes (+ modification)____________

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key hidden for github'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)  # refer to line A, line D

from models import User, Post #refer to line C, line F

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
# today, you'll be restructuring your application to be a package
# rather than running it as a module.

# now, you typically start off all your flask applications as packages
# because you dodge a lot of headaches by creating it as a package from the beginning.

# but you'll see a lot of people using modules like you've done so far
# so in flaskblog13 you'll be shown the process of converting these into using a package
# and also the reasons why you'd want to do that.

# in flaskblog11, it was discussed that the db.Models are to be put into the application;
# rather than splitting them into different files like you did with forms.py
# and that's because the imports can get a little weird.

# let's go ahead and split these models into different files
# so that you can see what happens and what the problem is.

# create a file called 'models.py' within the Flask_Blog project directory,
# that will hold your db.Models.

# with models.py created, move over the db.Models (User, Post) from the application to the models.py file.
# and since the classes inherit the db.Model class from the db instnance,

# Line A: grab the db instance from this application file flaskblog13 and import it to models.py

# Line B: since your db.Models also use the datetime library (in the date_posed db.Column),
# let's go ahead and move that import to models.py aswell.

# and now within the flaskblog13.py module, you're going to be using the db.models within your views

# Line C: so go ahead and import the db.Models(User, Post) into flaskblog13 aswell.^

lb(1)
# now let's run your application and see if everything worked.

# since it was already mentioned up top in lb(0) that there were problems with this,
# so you can probably take an educated guess that this isn't going to work
# but let's go ahead and try it anyways:
# returns:
'''
ImportError: cannot import name 'User' from partially initialized module 'models'
(most likely due to a circular import)
(/Users/jinyoungchoi/Desktop/self_development/Programming/Python/Corey Schafer Python Beginner Tutorials/Flask_Blog/models.py)
'''

# actually, what's going on here is kind of a big mess.
# the solution that you're going to put in place
# is a lot more simple than what the walkthrough of this error is going to be.

# now, this is called a circular import
# but even this circular import is extra confusing.

# it was anticipated that this would throw an error,
# but as to why this was failing on the User import, and not somewhere else, is tricky to comprehend.
# let's walk through this step by step and explain why it failed on the User import.

lb(2)
# when you were running flaskblog13 script,
# it imports User and Post from your models.py module.

# and anytime python imports something from a module,
# it still runs that entire module.

# n.b. now some people are not actually aware of that,
# thinking that it only runs the sections that are being imported.

# then when it runs the entire models.py module,
# it comes into the models.py script and tries to run *its* imports.

# now, it is at *this point* that you would expect things to fail.
# because you've already seen the flaskblog13.py module,
# and you figured that it would just say:

''' 'hey, i've already seen this flaskblog13.py module,
     and i haven't seen this db variable that you're asking for' '''

# and if you switch over to flaskblog13.py,
# the reason that it hasn't seen the db variable yet,

# Line D: is because db is created 'db = SQLAlchemy(app)'
#*after* the import statement 'from models import User, Post'.

# so, then, it would throw an error saying that it can't import this db variable.
# but it doesn't do that;
# it fails on the user import

# why does it do that?!

# what's actually going on here when you ran flaskblog13 within the command line,
# is that you're running it directly with python

# and when you run a script directly,
# python calls the name of that script: __main__
# and you've seen that before with your conditional down at the bottom of the flaskblog13 script:
'''
if __name__ == '__main__':
    app.run(debug=True)
'''

# so here's the exact sequence:

# 0: you're running this python script, which python calls '__main__'
# 1: and then you say 'from models import User, Post'
# 2: and then it comes in and runs your models.py script

# 3: and when it gets to the line 'from flaskblog13 import db',
# pyton hasn't actually seen flaskblog13 yet, since python named flaskblog13 --> '__main__'

# 4: so it'll actually run your flaskblog13 module for the second time from the beginning,
# and it redoes all of the imports (including the 'from models import User, Post') again,

# 5 and when it gets to that models import, it says:

''' 'ok, i've already seen this models module,
     but i don't know what this User class is' '''

# and the reason it doesn't know what the User class is,
# it is because it is below your imports in the models.py module.
# so that is why it fails on the user import and not on the db import.

# so if you were to come into the models.py module,

# Line E: and if you were to change the 'from flaskblog13' import db to 'from __main__ import db',
# then this should still give you an error,
# but that would be the error you initially expected
#(i.e. saying that it can't find the db variable instead of failing on the user)

# in fact, if you return to the commandline and run flaskblog13.py via python again,
# this time it'll say 'ImportError: cannot import name 'db'

# just to walk through this again,
# the reason that it fails on this import now is because
# when flaskblog13.py is run, it gets down to the models import,
# and within models, now it's running 'from __main__ import db'
# and it's already seen the __main__ module but it hasn't created the db variable yet
# so that's why it fails on that import.

lb(3)
# now you could fix this by
# Line F: moving the 'from models import User, Post' *below* db = SQLAlchemy(app)

# and this now let's you run flaskblog13.py from the command line successfully.

# *but*, even though you solved this problem and the application is running now,
# the way you solved this problem is still really ugly
# and if you were to run the application where flaskblog13 *weren't* set to __main__,
# then all of this would fail.

# so, e.g. when you created your database by doing db.create_all() in the command line,
# that would no longer work.

# to illustrate,
# if you were to delete the database you created (site.db) in flaskblog12 from the project directory,
# and return to the command line and type in 'from flaskblog13 import db',
# you can see that at this point this fails:
# returns: ImportError: cannot import name 'db' from '__main__' (unknown location)

# and that's because it's looking for db in one of your imports in __main__,
# and, at that point, __main__ is no longer your flaskblog13 module.


# # # # # # # # # # # # # # # # continue onto flaskblog14.py # # # # # # # # # # # # # # # #
