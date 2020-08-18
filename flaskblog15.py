def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the fifteenth note on building a python flask application *
*this is also referred to as the run.py that logically connects to flaskblog14.py*
~lb(0): turning flaskblog__.py into a package
~lb(1): splitting the import modules among package files
~lb(2): cleaning up redundant imports from split files
~lb(3): high-level overview of flaskblog package (!= directory)

'''

from flaskblog import app  # refer to line A

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

lb(2)
# ok, so you're still running app.run() within this file,
# Line A: so go ahead and import the app to run from your package.

''' from flaskblog import app '''

# n.b. when you're working with packages,
# that is going to import from the __init__.py file from within your package
# so that app variable has to exist within __init__.py

# and lastly, you need to go through your other files and clean up your imports.
# now, some of the imports within the __init__.py file were only used in your routes,
# in particular, the first line of import:
''' from flask import Flask, render_template,url_for, flash, redirect '''

# i.e. copy and paste this line of code into routes.py
# n.b. you don't need the Flask import from this code so remove this when code is moved to routes.py
# correspondingly, return to __init__.py and remove all but Flask (render_template, url_for, flash, redirect)

# now, the next line of import 'from flask_alchemy import SQLAlchemy' will still be needed in __init__.py
# since right below the imports you are calling SQLAlchemy with 'db = SQLAlchemy(app)'.
# so keep this line of code.

# but, the next line of import:

'''from forms import RegistrationForm, LoginForm'''

# is not really needed in __init__.py
# and instead they were only really used within your routes.

# so let's grab those and move them to routes.py.

# and also, now, when you do these imports,
# instead of importing from models and forms like you did before,
# now that you're in your package,
# you're going to use the package name and the module name.
# i.e.:
'''
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

instead of (previously):

from forms import RegistrationForm, LoginForm
from models import User, Post
'''

# also, if you scroll down within routes.py,
# you'll note that the decorators (app.route('xyz')) are using the 'app' to create the decorators.
# which means that you need to import this 'app' variable into routes.py also.

# Line B: so import it within the flaskblog package

# now if you look back at the app __init__.py file,
# you'll see that you need to import your routes here also
# so that when you run your application it can find those.

# now, even though you solved the problem with the messy imports,
# you still need to watch out for circular imports.

# remember that your routes are importing the app variable from __init__.py
# you can't import the routes at the top of this file
# or else you'll get into a circular import again.

# so, instead, let's do the import of the routes
# after you've made the app initialisation (app = Flask(__name__)

# i.e. write 'from flaskblog import routes' at the bottom of this __init__.py

# you're almost done here;
# let's also check your forms.py and models.py modules aswell.

# first, looking at forms.py:
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
'''

# in forms.py, you're not using any other modules from your package,
# you're just using packages that you pip install'ed.
# i.e. nothing needs to be changed there.

# lastly, looking at models.py:
'''
from __main__ import db  # refer to line A, line
from datetime import datetime  # refer to line B
'''

# here is where you had your messy work-around from before.
# now, instead of importing from __main__, you can simply import from flaskblog
# because now you know that's not actually going to be called __main__ anymore.

# so modify 'from __main__ import db' to 'from flaskblog import db'.
# and now that's going to come into the __init__.py file,
# and import the db = SQLAlchemy(app) here.

lb(3)

# ok, so that should do it.
# now, before you run this, here is the tree structure of what you've done in this video:
'''
|--<flaskblog>          [1]
|   |
|   |--__init__.py
|   |--forms.py
|   |--models.py
|   |--routes.py
|   |--<static>
|   |   |
|   |   |--main.css
|   |
|   |--<templates>
|       |
|       |--about.html
|       |--home.html
|       |--layout.html
|       |--login.html
|       |--register.html
|
|--run.py               [2]

[1]: <> are directories
[2]: run.py is now the default file for running the application

# so you can see that in your project directory, you now have a <flaskblog> package
# and a module called run.py that will run your application.

# within <flaskblog> package, you have __init__.py file which tells python that this is a package,
# and it also initialises and ties together everything that you need for your app.

# you also have the routes.py file that contains all of the logic for your routes,
# and forms.py and models.py should be familiar from previous notes but you just cleaned up the imports.
#(you also have the static and templates modules but you didn't change anything within those two directories)

# now to run your directory, instead of python 'flaskblogXX.py', it'd be python 'run.py'.
# upon running the app, it looks like everything still works as they should, without throwing any errors like before.

# now, not only does your application now work in your browser,
# but you can also create your database again, which failed when you tried this before:

# in the command line:
# 1: python
# 2: from flaskblog import db
# 3: from flaskblog.models import User, Post
# 4: db.create_all()
#(since you had deleted site.db in flaskblog12.py notes)

# 5:User.query_all() should return an empty list (since you don't have anything in the database yet)
# returns: []

# it's understood that in this restructuring note
# you didn't get much further in your application that added new features,
# but now you'll have a much better idea on why it's better to structure your applications in this way
# and how it can save you a lot of headaches down the road.


# # # # # # # # # # # # # # # # continue onto flaskblog16.py # # # # # # # # # # # # # # # #
