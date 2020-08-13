def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the sixth note on building a python flask application *
~lb(0): brief intro. to forms in flask development
~lb(1): working with wtforms
~lb(2): creating a field (username) within form
~lb(3): validators: acknowledging limitations within a given field
~lb(4): creating a new field (email)
~lb(5): creating more fields (password, password confirmation)
~lb(6): ...and more fields (submit)
~lb(7): creating login form

'''

lb(0)
# today you'll go over how to create forms and to validate user input
# so the app you create will have the ability for the user to:

# create account
# log-in
# make posts
# log-out, etc.

# and the first part of that process is to create a registration page
# where users can create an account on the website, log-in, and log-out.

# now, if you were to create forms from scratch, that can get very complicated very fast.
# you'd have to put in different validation checks to:
# ensure that the user was inserting information correctly,
# make sure that their password matches,
# write some regular expressions,
# make sure they entered a valid email, etc

# but luckily, this process is so common that you don't have to reinvent the wheel.
# there are extensions out there that have already put in all the hard work so that you don't have to.

# and the most popular extension when it comes to working with forms in flask is called wtforms (wtf).
# and that's what you're going to be using today.

lb(1)
# first, you need to install this, load up terminal and write in a simple 'pip install install flask-wtf'
# once installed, create a file 'forms.py' within the project directory where you can put these forms

# n.b. now, this could go into the application module that you have been writing,
# but it's best to split things like this out into their own files so that everything has its own place.
#(that way, if you need to update a form in the future, you'd know exactly where to look)

# so it's better to have this stuff split up into smaller, more manageable sections of code,
# rather than one larger application file where everything is in one place and hard to find.

# now within forms.py, let's create your forms.
# first, import this into your application by 'from flask_wtf import FlaskForm'

# now, if you have done web development for some time, you may be used to writing forms in HTML,
# and this is going to be a little different using this flask extension:
# you'll actually be writing python classes that would be representative of your forms,
# and they will automatically be converted into HTML forms within your template.

# let's say if you wanted to create a registration form,
# you can create a registration form class that will inherit from FlaskForm:

'''
class RegistrationForm(FlaskForm):
    pass
'''

lb(2)
# now, within your form, you're going to have different form fields.
# and these form fields are all going to be imported classes aswell.

# e.g. let's say that the first field that you want in your form is a username.
# and the username is going to be a string field.

# and this won't be imported from the flask-wtf package,
# but instead, the wtforms package (which was also installed with the pip install)

# so, in forms.py, write in 'from wtforms import StringField'
# and now within the RegistrationForm class, you can create a new attribute:
'''
    username = StringField('Username')
'''
# note: Username will also be used as your label in your HTML.

lb(3)
# but now, when it comes to usernames, there might be a few limitations you want to put into place:

# first of all, you want to make sure that the user puts in ~something~ for their username,
# instead of leaving it blank

# second, you wouldn't want the user to create a username that is 50 characters long,
# because that wouldn't look great on your website.

# so let's say that you want to allow usernames between 2-20 characters.
# to put these checks and validations in place, you can use something called validators.
# and they will be another argument that you pass into your field.

# so let's add a list of what you want validated, by passing in another argument to StringField()
# called 'validators=[]'
'''
    username = StringField('Username', validators=[])
'''

# and just like with the fields, these validators are also going to be classes that you import.
# to make sure that a field isn't empty, you can use the DataRequired validator.
# to use this validator, write in 'from wtforms.validators import DataRequired' into forms.py

# once DataRequired is imported, be sure to add in DataRequired() into the validators=[] list.
# n.b. since DataRequired is a class (like StringField), be sure to also add the parentheses after DataRequired

# so now, if you want to make sure that the username is between 2 and 20 characters,
# you can use the length validator; so let's include that to to classes to import from wtforms.validators
# and also add Length() to the list of validators= [] aswell.

# but this time, within Length(), be sure to add args of Length(min=2 and max=20)!
# now, you have a list of validators whereby the first is DataRequired(), meaning it can't be empty,
# and the second is Length(), which gives a min and max for what a username can be.
# that's why using these extensions can be so convenient, because you don't have to write these from scratch.

lb(4)
# moving on, let's write another field now:
# the next field you're going to want is an email,
# which is also going to be a StringField with the label 'Email':
'''
    email= StringField('Email', )
'''
# and let's also pass in some validators:

# 1) DataRequired() so that you don't want the user to leave that empty and
# 2) Email() which will ensure that the email is a valid email address.
#(make sure to add Email() to a list of classes to import from wtforms.validators):
'''
    email= StringField('Email', validators=[DataRequired(), Email()]
'''

lb(5)
# and lastly, for the registration form,
# you're going to want fields for password, and password confirmation.

# to do this, you need to add a PasswordField from wtforms (like you did StringField)
# and now, you can add these into a password field.
# whereby the label could just be 'Password',
# and the validators you'd need= DataRequired() and Length(min=8, max=20)
'''
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
'''
# and now you also want a password confirmation field,
# which will basically be the same as the above password field, but slightly different.
# the different being that you'd want to add another validator-
#-to ensure that the input value for password and confirm_password are equal.

# you'd need to import the EqualTo() validator from wtforms.validators,
# and add it to the list of validators=[] for confirm_password.
# n.b. the argument for EqualTo() is the field you want this to be equal to, 'password':
'''
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=8, max=20),
                                                 EqualTo('password')])
'''

lb(6)
# once you finish this form with the above fields,
# you now need a submit button to send that information to you.
# as expected, you can do so using a SubmitField.

# similarly to StringField and PasswordField, import SubmitField from wtforms,
# and add a new field 'submit' to RegistrationForm class,
# and have the label called 'Sign Up' (since this is a registration form after all):
'''
    submit = SubmitField('Sign Up')
'''
# and with the submit field added, the RegistrationForm class is now complete.

lb(7)
# now that you have registration out the way, you need to create a LoginForm class.
# copy the RegistrationForm class and paste it underneath,
# and change a few things around to make it applicable to Login:

# first of all, you can choose to require either username or email for Login,
# and typically email is the preferred one for login since it's easy to forget a username and less so for email
#(i.e. delete the username field from LoginForm)

# and second of all, you can also get rid of the confirm_password field
# since the user should only have to do that in Registration.

# and now, for some change in Login Form,
# you're going to add a remember field
# which will allow the user to be logged in for sometime after their browser closes, using a secure cookie.

# when creating the remember field, this is going to be a BooleanField.
#(again, make sure to import BooleanField alongside StringField, PasswordField, SubmitField up top)
# BooleanField is basically a True or False:
'''
remember = BooleanField('Remember Me')
'''

# and lastly, modify the submit field to submit = SubmitField('Login')

# # # # # # # # # # # # # # # # continue onto flaskblog7.py # # # # # # # # # # # # # # # #

