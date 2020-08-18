def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the sixteenth note on building a python flask application *
~lb(0): hashing passwords via bcrypt
~lb(1): verifying hashed passwords
~lb(2): implementing hashed passwords to app
~lb(3): confirming data upload + password hashed successfully

'''
#____________from previous flask notes (+ modification)____________

from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# the next series of notes
# will be on how to use your application to add users to your database
# and also how to authenticate users so that they can log in/out
# and also soon be able to create posts, etc.

# previously, you created your database and saw how you could manually create some users and posts
# but let's apply the same logic to your application
# to create your users through the registration form.

# now, before you create your users
# you're going to need to find a way to hash your passwords.

# in the previous notes, you were using plaintext 'passwords' for your examples
# but you never want to do this to your actual website!

# because if anyone ever gets access to your database,
# they would have the logins for all of your users!

# there are several different hashing algorithms,
# but one good one is called bcrypt

# and the flask extension flask-bcrpyt makes this easy to use

# navigate to your virtual environment in your project directory and type in the following commands:

# 1: pipenv shell (to activate virtual environment)
# 2: pipenv install flask-bcrypt (or pip install flask-bcrypt outside the venv)

# 3: python (to see how bcrypt works)
# 4: from flask_bcrypt import Bcrypt (importing the Bcrypt class from flask-bcrypt module)
# 5: bcrypt = Bcrypt() (creating an instance of that class)

# 6: bcrypt.generate_password_hash('testing')
#(hashing a password='testing' using .generate_password_hash() method)
#returns: b'$2b$12$Vvbb6pwsIaw0C77q4kxizuAWTauyEV7BU5xKDK.ra7Dz1fNNA.vXK'

# you can see that the method created a password hash^.
# and the b' in the beginning means that this is in 'bytes'.

# n.b. in the extension's documentation page,
# they say that if you want a string then you can simply decode this into UTF-8:

# 7: bcrypt.generate_password_hash('testing').decode('utf-8')
#returns: '$2b$12$2NlR8lHL2x4xtxpkOAbnV.L9NL/eWKbCsg6c5YaggsKGyRUfLZeXe'

# you can see that the result is a hashed string (with no b' in the beginning)

# note: one thing to notice is that each time you run this
# you get a different hash (even when using the same password 'testing'):

# a) bcrypt.generate_password_hash('testing').decode('utf-8')
#returns: '$2b$12$jjm4DIIFH1HB/Mxd4dhVgeRcXfy835npn08.KQwkfi13LTJ0qq.gW'

# b) bcrypt.generate_password_hash('testing').decode('utf-8')
#returns: '$2b$12$vGa4s06KPHOFxkJt9Y/aWutzRTIx9W1pJ7bbuo1GAaR4YkN6kKUGa'

# c) bcrypt.generate_password_hash('testing').decode('utf-8')
#returns: '$2b$12$NYCdH3./POHB.g.aJrirC.QRgWUMe73VThEEBgNQsVywZpunrPZ9u'

# this means that if someone were to steal your database,
# they wouldn't even be able to use a hashtable to crack these passwords.

lb(1)
# then, if its a different hash every time
# how can you verify that the user enters the correct password?

# if you just hashed their entered password and compare it to what is stored in the database,
# those will likely be different.

# so you need to use another method called .check_password_hash()
# in order to check if the passwords are equal.

# you're going to save this hashed password as a variable [1],
# and check a few passwords against this hashed password [2][3]:

# 1: hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')
# 2: bcrypt.check_password_hash(hashed_pw, 'password') (i.e. comparing hashed_pw with 'password')
#returns: False

# the False is anticipated because your password prior-hash was 'testing', not 'password'.
# then:

# 3: bcrypt.check_password_hash(hashed_pw, 'testing')
#returns: True

# so this is how you are going to hash and verify passwords.

lb(2)
# let's add this to your application initialisation.
# navigate to __init__.py in flaskblog,

# 1: (below SQLAlchemy import) from flask_bcrypt import Bcrypt
# 2: (below db = SQLAlchemy(app)) bcrypt = Bcrypt(app)

# and now let's open up your routes.py and see what your registration logic is:

'''
form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
'''

# the above shows that if the form is valid on submit,
# it will flash an 'Account created for user X'
# but you aren't currently creating that account.

# so let's do that:
# if the form is valid on submit,
# let's hash the password that they entered
# so that it's ready for you to save it to the database.

# first, you need to import bcrypt and the db variables
# and remember that if you're importing from your package,
# it's going to import it from that __init__.py file
# but you can just write that as if you're simply importing from the package itself:

# 1: you're already importing from flaskblog (from flaskblog import app)
# 2: modify to 'from flaskblog import app, db, bcrypt'

# and now the following changes in the registration route:

'''
[a]    if form.valiudate_on_submit():
[b]        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
[c]        user = User(username=form.username.data, email=form.email.data, password=form.hashed_password)
[d]        db.session.add(user)
[e]        db.session.commit()
[f]        flash('Your account has been created! You are now able to log in', 'success')
[g]        return redirect(url_for('login'))
'''

#[a] inside the validate_on_submit() conditional,
#[b] write in basically what you had done back in the command line in lb(1),
# although in this time, passing in the password that you'd want to hash
#(which is going to be whatever they insert into the password field)
# lastly, remembering that you'd want to decode('utf-8') since you want a string (not a byte) returned:

#[c]: now that you have you have a hashed password,
# you can create a new instance of a user.
# n.b. the user instance can be created as below, but make sure to pass in hashed_password instead of form.password.data
# because that would be the plaintext password (and we want the hashed version of that!)

#[d]: one you have the user created, go to the next line
# and add this user to the changes that you want to make in your database.

#[e]: and now you also want to commit those changes
# note: it's only one change so db.session.commit() is writen only once.
# henceforth, the user is finally added to the database.

#[f]: now let's flash them a message telling them that their account has been created
# and that they can now log in
# keeping the second argument/category 'success' there because that is the Bootstrap class.

#[g]: and now instead of redirecting them to the home page, return the login route

lb(3)
# now let's see if that works.

# start up the website by typing in 'python flaskblog16.py' into terminal in project directory,

# and on the webserver 'localhost:5000/register',
# make a dummy account:

'''

username:
JYC
email:
JinYoungChoi@gmail.com
password:
password

'''

# with valid form information you can see that you were redirected to the login page
# with your flashed message telling you that you can now log in.

# now your login still isn't working
# but it looks like your user was added to the database.

# to confirm,
# load up terminal in the project directory once again:

# 1: python
# 2: from flaskblog import db
# 3: from flaskblog.models import User
# 4: user = User.query.first() (grabbing the first user from this table)

# 5: user (printing out your first user)
#returns: User('JYC', 'JinYoungChoi@gmail.com', 'default.jpg')

# now let's look at the password for this user:

# 6: user.password
#returns: '$2b$12$QZosP65KrAwVzIwQsNTDoO3dvux5SpGcoLFfjlcP22fs66h.WU/Hq'

# you see that you do get a hashed version of user's password which is exactly what you wanted.

# # # # # # # # # # # # # # # # continue onto flaskblog17.py # # # # # # # # # # # # # # # #
