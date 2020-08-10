######## MAKE SURE TO REMOVE THE SECRET KEY BEFORE PUBLISHING ON GITHUB #########

def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the seventh note on building a python flask application *
~lb(0): setting up secret key for user protection
~lb(1): adding routes for register & login pages in flask app
~lb(2): creating the register/login.html
~lb(3): accounting for 'submit' button within RegisterForm
~lb(4): 'Already have an account? _Sign in_'
~lb(5):

'''
#____________from previous flask notes (+ modification)____________

from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm  # refer to line B

app = Flask(__name__)

# refer to line A
app.config['SECRET_KEY'] = '8dd5ed349de316172a6d96f08034249b'

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


@app.route('/register')  # refer to line C
def register():
    form = RegistrationForm()  # refer to line D
    # refer to line E
    return render_template('register.html', title='Register', form=form)


@app.route('/login')  # refer to line F
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# now when you use the two forms (Registration and Login) created in flaskblog6.py,
# you need to set a secret key for your application.

# a secret key is used to protect against modifying cookies, crosssite requests, forgery attacks, etc.
# it's simple to do; you just need to go to the top of the application file above,

# Line A: set a secret key by writing app.config[] (which is how you set config values on your application),
# and write in 'SECRET_KEY',
# and have it equal to an empty string ''.

# ideally, you want the secret key for your application to be some random characters.
# a good way to get some random characters in python is to:
# 1: load up the python interpreter in terminal (by typing in python in the command line)
# 2: import secrets module
# 3: use the .token_hex method of the secrets module, passing in 16 for 16 bytes

'''
>>> import secrets
>>> secrets.token_hex(16)
'8dd5ed349de316172a6d96f08034249b'
'''

# now the output '8dd5ed349de316172a6d96f08034249b' will be used as the secret key for Jin Young's Blog
# n.b. you'll likely want to make this an environment variable at some point
#(this will be covered in later notes)

lb(1)
# now let's use the RegistrationForm and LoginForm that you created here in the application^:
# Line B: first you need to import those forms (which are stored in forms.py, within the same directory)

# now let's create some routes for your Registration and Login
# so that you can see how these get converted to HTML.

# first, create the registration route,
# navigate to your if __name__ = '__main__' and right below it,

# Line C: create another app.route('/register') with function register():

# Line D: and now you need to create an instance of your form that you are going to send to your application.

# and now you can pass this form to a template.
# you haven't created your register or login templates yet, but you will in just a second.
# in the meantime, you'll go ahead and pretend that they're there for now.

# Line E: you will create template called 'register.html',
# add in some additional info. e.g. title='Register' and you also want to pass in your form: form=form
# that way, within your template, you have access to the form instance you created in Line D.

# Line F: now do the same thing for your Login route.
# since this is going to be similar to the register route, copy the latter
# and modify the route & function name:
'''
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
'''

lb(2)
# with both of the routes created,
# you now just need to create the templates that use these form variables that you just passed in.
# create 'register.html' and 'login.html' templates in the templates directory.

# and now let's navigate to the about.html template and copy and paste the entirety onto e.g. register.html
# you can see that you are already extending the layout.html template,
# and now you just want to put the form in the content block of this page.

# open up a <div></div> and give it a class='content-section'
#(which is a style that pertains to main.css file used to make the site look a little nicer).

# and now open up a <form></form> tag, with its method="POST" and action='' (i.e. empty string*)
#(*meaning that when you post this form, it'll just post that info to the same route you're currently on)
'''
{% block content %}
    <div class='content-section'>
        <form method='POST' action=''>

        </form>
    </div>
{% endblock content %}
'''

# now you're ready to start putting in some form fields.
# the first field that you need is going to be {{ form.hidden_tag() }} *
# (* remember that you need the double curly braces wrap when you're accessing a variable in your template)
# (*this just means you're accessing the form instance you passed into this template,
#  and you're using the .hidden_tag() method.)

# note: now the hidden_tag is something that you need to add in, but don't worry too much about what it does.
# it's adding something called a CSRF (or CrossSiteRequestForgery) token,
# which is part of that secret key protection:
'''
    <form method='POST' action=''>
         {{ form.hidden_tag() }}
    </form>
'''

# ok, now let's add in some other form fields <fieldset> here
# and you're also going to add a couple of HTML and CSS classes here aswell.

# first, add a <fieldset (and set a) class= here equal to 'form-group'></fieldset>
# which is all Bootstrap stuff to make it look a little nicer.

# then you'll pass in a <legend (and set a) class= 'border-bottom mb-4'> </legend>,
# which will be the legend for the register form. set it to e.g. 'Join Today'.
# mb-4 stands for margin bottom with the value of 4.

# and let's create a form group,
# which is going to be a <div (of) class='form-group'></div>
# and within this div, this is where you're going to actually use the fields from the form that you passed in.
# write in {{ form.username.label }} (which will print out the label from your username field)
# and you're going to want to give this a class aswell,
# by putting in parentheses within and passing in a class argument:
# {{ form.username.label(class='form-control-label') }}
# note: again, the form-control-label is just some Bootstrap stuff to make it look nicer.

# so that would actually print out the form label, though we also want the field itself, so a another line below:
# as {{ form.username(class='form-control form-control-lg') }} (lg standing for 'large')
'''
<fieldset class='form-group'>
    <legend class='border-bottom mb-4'>Join Today</legend>
    <div class='form-group'>
        {{ form.username.label(class='form-control-label') }}
        {{ form.username(class='form-control form-control-lg') }}
    </div>
</fieldset>
'''

# now that you have these two form lines that make up the div,
# you can copy and paste these for email [1], password [2] & confirm_password [3] fields:
'''
<fieldset class='form-group'>
    <legend class='border-bottom mb-4'>Join Today</legend>
    <div class='form-group'>
        {{ form.username.label(class='form-control-label') }}
        {{ form.username(class='form-control form-control-lg') }}
    </div>
    <div class='form-group'>
        {{ form.email.label(class='form-control-label') }}                [1]
        {{ form.email(class='form-control form-control-lg') }}                [1]
    </div>
    <div class='form-group'>
        {{ form.password.label(class='form-control-label') }}                [2]
        {{ form.password(class='form-control form-control-lg') }}                [2]
    </div>
    <div class='form-group'>
        {{ form.confirm_password.label(class='form-control-label') }}                [3]
        {{ form.confirm_password(class='form-control form-control-lg') }}                [3]
    </div>
</fieldset>

#n.b. if you're wondering where you're getting these email/password/confirm_password fieldnames from,
#these are the variable names that you specified within the RegistrationForm(FlaskForm) class in forms.py .
#you want these variables to match the variables within the class:
"""
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=20)])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(min=8, max=20), EqualTo('password')])

    submit = SubmitField('Sign Up')
"""'''

lb(3)
# the confirm_password field is the last field you want in your <fieldset></fieldset>.

# now, after the </fieldset> tag, you still have to add in the submit variable within RegisterForm class,
# so you're going to create another form-group,
# and within this form-group enclose in the {{ form.submit(class='btn btn-outline-info') }}.
#(whereby the 'btn' stands for button, and 'btn-outline-info' for a Bootstrap button outline).
'''
    <div class='form-group'>
        {{ form.submit(class='btn btn-outline-info') }}
    </div>
'''

lb(4)
# since you're on the register page, you'll see on a lot of websites that the register page will have a:
#'Do you already have an account? Sign in'.
# so let's put in something like that aswell.

# below the <div></div> that all the RegisterForm variables were wrapped in (line 29),
# add in another <div (with the) class='border-top pt-3'></div>
# and within, include a <small class='text-muted'> (small text with class 'text-muted' to fade in the text)
# within which add in Already have an acount? and a link (in the form of <a></a> anchor tag)
# within the anchor tag, <a class='ml-2' ('ml-2'= margin left of 2, to give it some spacing from that text),
# and an href="{{ url_for('login') }}"Sign In</a> (which will be the link to your login page),
# making sure to close out the <a></a>.
'''
    <div class='border-top pt-3'>
        <small class='text-muted'>
            Already have an account? <a class='ml-2' href="{{ url_for('login') }}">Sign In</a>
        </small>
    </div>
'''
# n.b. remember that if you're going to link somewhere, it's always good to use the url_for() function.
# n.b.2. also remember that the value you're putting into url_for() is NOT the name of the route,
# but the name of the route function.
# in other words, you're passing in the 'login' instead of the '/login'.

# now, save both flaskblog7.py and register.html to see what the progress looks like on the browser.

######## DID YOU REMEMBER TO REMOVE THE SECRET KEY ON BOTH THE app.config AND from lb(0)? ########

# # # # # # # # # # # # # # # # continue onto flaskblog8.py # # # # # # # # # # # # # # # #
