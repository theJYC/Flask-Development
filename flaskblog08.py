def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the eighth note on building a python flask application *
~lb(0): allowing methods within @app.route('/')
~lb(1): flash() message: Account created for X
~lb(2): redirecting user back to homepage ('/home').

'''
#____________from previous flask notes (+ modification)____________

# refer to line C, line F
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret key hidden for github'

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


@app.route('/register', methods=['GET', 'POST'])  # refer to line A
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # refer to line B
        # refer to line D, Line E
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# so the localhost:5000/register page seems to have been implemented correctly in flaskblog7.py,
# with the StringFields for Username/Email/Password/Confirm password, etc.

# however, when you do go ahead and fill out username/email/password/confirmpassword and click Submit,
# you can see that it returns: Method Not Allowed /n The method is not allowed for the requested URL.

# the reason that you get that is because you're submitting a post request
# back to the same register route with your form data, but you currently don't accept post requests on that route.

# to accept a post request, you need to add a list of allowed methods in your route.
# go up to the application code and to the @app.route('/register'),
# Line A: pass in a second argument methods=['GET', 'POST'] so that it accepts get and post requests.

lb(1)
# with the methods added into the /register,
# you can see that submitting a registration form will no longer return a Method Not Allowed error
# and instead it posts the data and directs you right back to the register page.

# so you have no idea whether the form validated properly or not.
# so before you render your register template in your route,
# let's put in a check in place that checks whether you have post data,
# and also that this data is valid for your form.

# to do this, go back to your application code again
# and after form = RegistrationForm() and before return render_template,

# Line B: write in the validate_on_submit() method on form: if form.validate_on_submit()
# note: as you can probably tell by the name, this will tell you if your form validated when it was submitted.

# now you're going to use something called a flash message,
# which is an easy way for you to send a one-time alert.

# Line C: make sure you import this functionality, from flask import flash!

# Line D: create a message you want to display when you created your user successfully, within flash():
# using an f string (since you're going to pass in a variable) f'Account created for {form.username.data}!'

# so now you have a flashed message here,
# but you want to be able to tell the difference between different kinds of alerts.

# bootstrap has different alert styles for successes, warnings, and errors,
# and the flash() function accepts a second argument that is called a 'category'.
# so you're going to pass in the name of the bootstrap class that you want this alert to have,
# and that is 'success'.

# Line E: pass in the string 'success' as a second argument to flash().

lb(2)
# now that you got your flash message,
# let's redirect the user to a different page, because you don't want to fill out a form
# and just get redirected back to the same form after you submit it.
#(that would be a little confusing for the user).

# instead, you'll redirect the user to the homepage.
# Line F: to do this, first import the redirect function from flask (from flask import redirect)

# and then come back into the if conditional (from line B), i.e. when the form validates properly,
# Line G: you'll say return redirect(url_for('home'))
# again, 'home' is the name of the function of that route (and NOT the route (/home) itself).

# now this should all work except for one thing:
# you haven't updated your template to show the flashed messages yet.

# so you're going to put this within your layout.html template so that flashed messages pop up on any page.
# open up your layout.html and, let's just assume that you want to display any of your flashed messages

# up at the top of the content block {% block content %} (at line 44),
# open up a code block {% %}, and use a with statement and get_flashed_messages() function (i.e. with block),
# and you also want to pass in an argument within the function, 'with_categories=true'.:
'''{% with messages = get_flashed_messages(with_categories=true) %} '''
# note: the get_flashed_messages() function will get the flashed messages that you send to this template
# note2: the 'with_categories_true' argument will allow you to grab the 'success' category that you passed into the flashed message,
# which is the Bootstrap class that you're going to use.

# and now, within this {% with %} block, you want to print out any messages
# if there were messages returned from this get_flashed_messages() function.

# i.e open up another code block {% if messages %} {% endif %},
# which will mean that if messages were not empty, you have some flashed messages to display

# now you can loop over the flashed messages
# by opening up another code block {% for category, message in messages %}
#(since you said with_categories=true you're going to get two values (category, message) from these messages)

# nested within the for loop {% for %}, finally print out this message
# by creating a <div class='alert alert-{{ category }}'>
# so, e.g. since you passed in 'success', this class is going to be assigned alert-success.
# and you'll see this in action in just a second!

# so now within this div, you want to actually print out this message
# pass in a {{ message }}

# and now end the for loop with {% endfor %},
# and also close off the {% with %} block with {% endwith %}

# so now that you have all of that in place,
# let's make sure that it all works if your form validates properly,
# by running the server on Terminal and reviewing the changes on the browser.

# and it does!
# when valid data was typed into the RegistrationForm on Register page,
# the green flash message (of 'Account created for {form.username.data }}!')

# # # # # # # # # # # # # # # # continue onto flaskblog9.py # # # # # # # # # # # # # # # #
