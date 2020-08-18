def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the seventeenth note on building a python flask application *
~lb(0): note on flask debug tool
~lb(1): custom validator for already taken username & email
~lb(2): installing & initialising flask_login and LoginManager
~lb(3): working with flask-login / LoginManager / UserMixin

'''
#____________from previous flask notes (+ modification)____________

from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# now, if you go back to your application,
# there is actually something wrong with how you have this right now
# that might not be obvious right off the bat.

# currently, your RegistrationForm() will validate against fields such as bad emails and empty fields
# but there is nothing stopping a user from trying to sign up with a username or email
# that already exists in your database.

# now you have a restriction set on your database model that say that those have to be unique
# but that won't be caught or throw an error until you try to add that new user to the database.

# let's see what it would look like
# if you try to add another user or email that currently already exists

# upon signing up again with the exact same credentials:
'''
sqlalchemy.exc.IntegrityError
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: user.email

(Background on this error at: http://sqlalche.me/e/13/gkpj)
'''

# n.b you get this ugly error screen when flask throws an error and you're in debug mode
# this information can be extremely useful when debugging problems in your application,

# but this is also why you want to be absolutely sure
# that you're never running on debug mode when deploy your website publicly
# because this is just too much information that you'd expose to other people.

# you can actually come to the bottom of the stack trace
# and run python code to dig further into the problem.

# and you need the debugger pin from your console to do this,
# but it's still risky having that possibility.

# i.e. never run your code in debug mode when deploying the website to the public.

lb(1)
# now, you might think that it be best to go into the register route in routes.py
# and add in some database checks after the form was validated
# to see if username/email already exists in your database.

# that would be one way to do it.

# but the best way to do it is to add your own custom validation for RegisterForm().
# that way, it get's checked when you actually validate the form
# and will return the visual feedback like the error messages like you've seen before.

# so, how do you do this?

#(information from the wtforms documentation)

# open up your forms.py file
# and within RegistrationForm class:

'''
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=20)])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(min=8, max=20), EqualTo('password')])

    submit = SubmitField('Sign Up')
'''

# and, below submit, you can create a custom validation simply by creating the function:

'''
[1] def validate_field(self, field):
[2]     if True:
[3]         raise ValidationError('Validation Message')
'''

# what you created here is bascially a template for your validation methods.
#[1]: in this format, you're going to validate_fieldname*(self, fieldname*)
# fieldname* being whatever field you want to validate,

#[2]: this just says if True for now, but you'll add in some kind of conditional.
#[3]: if it meets that condition, then it can raise a validation error with a validation message.

# this will be more clear once you customise it to your needs.
# let's do that now:

# you want to validate the username field:

''' [1] def validate_username(self, username): '''

# and the condition that you want to check
# is whether or not the user already exists in the database

# 0: from flaskblog.models import User

# and now you can query whether the username submitted to the form
# is already in your database by:

'''
[2] user = User.query.filter_by(username=username.data).first()

'''

# whereby username.data is coming from the username field of the form
# and .first() is to just return the first value that you get from the database
# so if there *is* a value, you'll get the first one.
# if there isn't a user, you'll be returned None.

# now you can change your conditional to something that you'd want to throw a ValidationError

'''

[3] if user:
[4]     raise ValidationError('Validation Message')

'''

# i.e. if this user exists,
# then you'd want to throw the ValidationError

# basically if user is None, it won't hit this conditional and raise the error,
# but if the user is anything other than None, it would throw the error.

# now the validation message is what gets sent to the form
# and you want to be specific so that the user already knows what is going wrong:

'''
[4] raise Validation Error('Username already exists')
'''

# so, here is the validation_field all stiched up:

'''
from wtforms.validators import ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
'''
'''
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')
'''

# now that should give an error when a username is already taken
# let's do the same validation check for if email is already stored in the database too:
'''
def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')
'''

# simply by adding in these custom validators will solve your problem
# and catch that before throwing an ugly error that you saw before in flaskblog16.

# let's go back and reload your webserver
# and check to see the validation checks in action!

lb(2)
# so you now have a pretty good registration system.

# now you need to create your login system so that
# your users who have created accounts can log in and log out.

# to do this, you're going to be using another flask extension
# called flask-login.
# flask-login extension makes it really easy to manage user sessions.

# first install it via pip/pipenv/etc.
# then, add it to the __init__.py file like you've done with other extensions:
''' from flask_login import LoginManager '''

# and now, create an instance of the LoginManager class (login_manager = LoginManager(app))
# with all that, you are now able to use this login_manager in your application.

lb(3)
# the way that this works is that you add some functionality to the database models
# and then it would handle all of the sessions in the background for you.

# so open up models.py and import the login_manager instance
#(which comes from the same place as the db instance; i.e. add login_manager to this line of import)

# and now you need to add a function with a decorator @userloader
# and this is for reloading the user from the user_id store in the session
# it's just one thing you need to put in place for the extension to work.
#(because the extension has to know how to find one of your users via id)

# let's create this function load_user
# which takes user_id as an argument
# and then you can return the user for that user_id*
# casting that user_id into an integer just to be sure.

# and penultimately, decorate the function so that
# the extension knows that this is the function to get a user by an id
# heeding the '@login_manager.user_loader' naming convention.

'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

'''

# and there is one more thing that you have to do:
# the extension will expect your User db.Model to have certain attributes and methods.

# it's going to expect four to be exact:
# one is called 'is_authenticated'
# which will return True if user provided valid credentials
# another is called 'is_active'
# another is called 'is_anonymous'
# and last one is a method called get_id()

# now, you could add all of these yourself,
# but this is so common that the extension provides a simple class that you can inherit from
# that would add all of these attributes and method for you.

# you can simply import this class from flask_login (in models.py),
# and this class is called UserMixin.

# and then in the User db.Model, you can just pass in UserMixin as the second argument (i.e inherit from it):

''' class User(db.Model, UserMixin): '''

#so that should be all you need to do with your flask_login extension
#in order for it to manage your session for you.


# # # # # # # # # # # # # # # # continue onto flaskblog18.py # # # # # # # # # # # # # # # #
