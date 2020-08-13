def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the tenth note on building a python flask application *
~lb(0): intro. to SQLalchemy and ORM
~lb(1): sqlite relative path (sqlite:///)
~lb(2): creating database instance within application code
~lb(3): class models and database structure (1: creating User class)

'''
#____________from previous flask notes (+ modification)____________


from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy  # refer to line A

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key removed for github'
# refer to line B, line C
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy()  # refer to line D


class User(db.Model):  # refer to line E
    id = db.Column(db.Integer, primary_key=True)  # refer to line F
    username = db.Column(db.String(20), unique=True,
                         nullable=False)  # refer to line G
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')  # refer to line H, line I
    password = db.Column(db.String(60), nullable=False)  # refer to line J

    def __repr__(self):  # refer to line K
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


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
# in this series you'll be creating a database for your application
# so that you can create real users and posts instead of relying on dummy data.

# and to work with these databases in python, you're going to be using SQLalchemy,
# which is a very popular ORM people use for different databases.

# ORM stands for Object Relational Mapper,
# which allows you to access your database in an easy-to-use, object-oriented way,
# and the best part with SQLalchemy is that you can use different databases without changing your python code.

# e.g. if you want to use an SQLlite database for testing and Postgre database for production,
# then all you need to do is just pass in a different database URL for SQLalchemy to connect to
# but all of the code to create the database will be the same.

# and that's what you'll be doing in this series:
# you'll use SQLlite database for development and then when you're ready to deploy this application
# you'll switch over to Postgre database for production.

lb(1)
# first of all, you need to pip install the flask-sqlalchemy package.
# note: there is also a regular sqlalchemy package,
# but flask-sqlalchemy package is a flask-specific extension that provides some useful defaults and helpers for your flask application.

# once that is installed,
# Line A: import it to the application above

# after SQLAlchemy is imported, you need to specify the URI for the database;
# URI is where the database is located.

# now you currently don't have a database so let's just choose this location to where you want it to be:
# for now, let's use an SQLlite database because it is the easiest to get up and running.

# SQLlite database will simply be a file in your file system.
# to set this location, you'll have to set it as a configuration (i.e. app.config! )
# Line B: app.config[SQLALCHEMY_DATABASE_URI] = ''
# noting a) the all UPPERCASE location^, and b) the = '' (i.e. empty string)

# with SQLlite, you can specify a relative path with three forward slashes in the URI.

# Line C: so, in this empty string, type in 'sqlite:///site.db'

# these '///' three slashes are a relative path from the current file
# which means that the site.db file should get created within the project directory
# alongside the python module that you're currently in.

lb(2)
# now that you have that location set,
# you need to create a database instance.

# to do that, you can come up to right below the config you just created,

# Line D: db = SQLAlchemy(app)
# now you have an SQLAlchemy database instance and are ready to work with your databases.

# now, the great thing about SQLAlchemy is that you can represent your database structure as classes.
# you'll be hearing those classes referred to as 'model's

# and doing the database structure this way is actually very intuitive once you get the hang of it.

# now, you could put these classes into a separate file (like you did with forms.py),
# and you will do that later along in the notes but
# for now, you're going to put these within your main application code above^,
# since the imports can get a little weird with these dependencies if you were to separate them right now
#(in Part 5, you'll learn how to split these files up properly).

lb(3)
# let's go ahead and create those class models that will be your database structure.
# each class is going to be its own table in the database;
# first, let's create the user class to hold your users.

# Line E: create a class called User and inherit from db.Model.

# now, within the User class,
# add the columns for this table.

# Line F: first, add a variable called 'id' (which is going to be a unique id) and assign it to db.Column()

# now, within the db.Column() method, specify what type this is.
# pass in db.Integer (since this is going to be an integer),
# and also pass in primary_key=True, which just means that it's going to be your unique ID for your user:

'''id = db.Column(db.Integer, primary_key=True)'''

# now you can move on to your next column (username): username = db.Column()

# Line G: this username is going to be a string (db.String(20))
# noting that in the validation check of Part 3, the username was set to max 20 characters long,
# so pass in 20 into db.String(20).

# now, you want your username to be unique also, so pass in a unique=True as second argument,
# and also, a user *has* to have a username (i.e. it can't be 'null'), so pass in nullable=False as third argument.

# and now, the next column (email) will be very similar to username (except that it will need a longer max length)

# and the next column (image_file) will be for the user's profile picture

# Line H: just copy the db.Column format for username column, maintaining the max db.String(20) length to (20),
# and later in the notes you'll see why
#(you're going to hash these image files that are 20 characters long so that they are all unique)

# now, there's going to be a profile picture that every user starts out with that is the same,
# so users are not going to have unique=True if they keep the default picture (so remove this argument!)
# though keep the nullable=False because they have to have at least the default image,

# and now let's set a default value here.
# this is if you do not create the user with a specific profile image, then what is going to be the default.
# Line I: just set it to default='default.jpg' and this is something that you will add later in the series.

# let's keep adding some more columns.

# Line J: create a password column: password = db.Column(db.String())
# whereby these are going to be hashed, and the hashing algorithm that you'll use let's 60 characters.
# and you won't need the unique=True since people can have the same passwords, though you'll set nullable=True
#(since any user will need to have a password to create the account).

# and now you're going to specify a dunder repr method __repr__(self).
# this method is how your object is printed whenever you print it out.
# fyi: this method is covered in the Object Oriented Programming repository.

# you're going to return what you want the user object to look like when printed out.
# Line K: e.g. print out username, email, and image_file.


# # # # # # # # # # # # # # # # continue onto flaskblog11.py # # # # # # # # # # # # # # # #
