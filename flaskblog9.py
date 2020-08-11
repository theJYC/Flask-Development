def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the nineth note on building a python flask application *
~lb(0): validation feedback mechanism; incorrect data entry
~lb(1): applying the lessons to login page
~lb(2): simulating a successful login (with 'admin@blog.com' 'password')
~lb(3): errorproofing with url_for('route') vs. direct links (/route)

'''
#____________from previous flask notes (+ modification)____________


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])  # refer to line B
def login():
    form = LoginForm()
    if form.validate_on_submit():  # refer to line C
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':  # refer to line D
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))  # refer to line E
        else:  # refer to line F
            # refer to line G
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# towards the end of flaskblog8.py,
# you saw that your form was validating correctly and produced a feedback (get_flashed_messages()).

# n.b. now, these flashed messages are nice, but they are only a one time alert.
# so if you reload the homepage, the flashed message goes away.

# with this said, let's give some validation feedback to the end user
# so that if they input incorrect info., they know exactly what it is that they did wrong and hence need to fix.

# this is particularly pertinent because, say, if you currently fill out the form with incorrect info.
# e.g. 'jyc@gma' instead of a correct form of email address 'jyc@gmail.com',
# it'll not show any feedback at all
#(since the green flashed message 'Account created for (user)!' will not show since form was not valid).

# go back to the register.html template to fix this.
# so, for each field that you have here (form.username/email/password/confirm_password),
# each of those fields will have a list of errors if that field was invalid.

# so you can open up a conditional and print those errors.
# the way this is done in Bootstrap is you add a class=is-invalid to your field,
# and then you put a <div></div> underneath that with the class=invalidfeedback
# and then put in the error there.

# e.g. go under the {{ form.username.label(class='form-control-label') }} on line 9
# and open up a codeblock for the if statement {% if form.username.errors %} {% endif %},
#(which will only hit this conditional if you have any errors)

# and within the if codeblock,
# copy & paste in the {{ form.username(class='form-control form-control-lg')}}
# and make sure to add the is-invalid to the two classes^ that pertain to the field.

# now, underneath this field, create a <div class='invalid-feedback'></div> block
# and within this <div>, print out all of the errors that you have, using a for loop,
# i.e. {% for error in form.username.errors %} {% endfor %}.

# and within the for loop, print out a <span>{{ error }}</span> of all of these errors:

'''
{{ form.username.label(class='form-control-label') }} on line 9

{% if form.username.errors %}
    {{ form.username(class='form-control form-control-lg is-invalid')}}
    <div class='invalid-feedback'>
        {% for error in form.username.errors %}
            <span> {{ error }} </span>
        {% endfor %}
    </div>

{% else %}
    {{ form.username(class='form-control form-control-lg') }} #refer to line A
{% endif %}
'''

# to explain the above:
# if you form had errors,
# it would print out the above form field and its errors.

# if it had no errors,

# Line A: you want to complement the {% if form.username.errors %} with an {% else %},
# whereby you just want to print out what you had before: {{form.username(class='form-control form-control-lg') }}
#(i.e. the line that came after {{ form.username.label(class='form-control-label')}})
#(hence cut & paste this line into the else block!)

# now, its true that it can look like a lot to do all of this in lb(0) just to print out the validation errors
# and honestly, forms and validations is really where the flask Bootstrap extension has some advantages.

# but it's still much preferred to do these manually
# if you want the ability to easily make design decisions; i.e. you want to change to look of something.
# making these manually simply gives you more control!

# now you want to make sure to put in these validation errors for all of the field sections in your form,
# i.e. ensure that for form.email / form.password / and form.confirm_password this validation error check is included!

# once done, save and run the webserver to note the changes!
# you're getting some good feedback to let the user know exactly what they need to fix to create their account successfully.

lb(1)
# you're almost finished up,
# but one thing that remains is the login page.

# now this is going to be a lot faster because you've already done most of this work for the register page.

# let's copy your register.html template into your currently-blank login.html template,
# and now there are some things that you need to change in order to customise the login page.

# 1. modify Join Today on <legend class='border-bottom mb-4'>Join today</legend> line 7
# to 'Sign In' or 'Log In'

# 2. delete the username and confirm_password field sections
#(because you decided earlier that the most user-friendly login input method is email and password!)

# 3. add in the 'Remember me' binary field that you wanted to add to the Login page
# this is going to be a little different from the other fields.

# this is going to be a <div></div> with the Bootstrap class='form-check' (since it's going to be a checkbox)
# and you don't need any complicated validations here because it's going to be either a check / not checked
#(i.e. there is not really anything you, as a user, can do wrong here; no need to anticipate errors)
'''
<div class='form-check'>      -------------line 34
</div>
'''

# now, within the div, let's put in these field values.
# first, put in the checkbox: {{ form.remember(class='form-check-input') }}
# also you want to put in the label for this field: {{form.remember.label(class='form-check-label')}}

# 4. also, if you look at most websites, if you had forgotten your password, you can do a password reset.
# let's add one of those in right after the submit button (line 40)
# by creating a <small></small> tag with the classes 'text-muted ml-2'
# text-muted to make it subtle and ml-2 to have it spaced a little from the submit button.

# and then with the <small class='text-muted ml-2'> </small>,
# add in an anchor tag <a> with the href=''
# n.b. you haven't yet made a URL for the Forgot Password link,
# so if you ever just want to put in a dummy link, put in a '#' as the href.
# and, as for the txt within the <a> tags,
# write in Forgot Password?:
'''
<small class='text-muted ml-2'>      -------------line 42
    <a href='#'>Forgot Password?</a>
</small>
'''

# 5. finally, change up the Already Have An Account? of register.html (line 49)
# from 'Already Have An Account' to 'Don't Have an Account?',
# and from url_for('login') to url_for('register')
# and finally, from 'Sign in' to 'Sign up now'

# now, save login.html and flaskblog9.py and run localhost:5000/login.
# looking pretty good!

lb(2)
# you currently don't have any user data stored on the browser,
# but 'let's go ahead and simulate a successful login!
# return to the application code above,

# Line B: first, make sure you allow GET and POST requests for the app.route('/login')
# by adding the second argument of app.route('/login', methods=['GET', 'POST'])

# Line C: and copy and paste in the if.form.validate_on_submit(): under form =LoginForm()
#(similar to how form = RegistrationForm() is set up)

# now within the if conditional, let's put in some fake data to simulate a successful login.

# Line D: write in if.email.data (i.e. the data that was submitted on the email form)

""" if form.email.data == 'admin@blog.com' and form.password.data == 'password' """
# i.e. if the user submits a login form with email (admin@blog.com) and password (password)
# then you want to simulate a successful login

""" flash('You have been logged in!', 'success') """
#(note that the second argument 'success' is the category that gives this flash message a green tone)

# Line E: make sure that, if user puts in the fake admin profile as above, they are redirected to homepage.

# Line F: now, you'll just say that any other submissions (i.e. else:) are invalid.

# Line G: and this will display a flash message of:
'''flash('Login unsuccessful. Please check username and password', 'danger')'''
# whereby the 'danger' second argument is responsible for giving the flash message a red (instead of green) tone.

# at this point, for the else: condition, you don't want to return anything (as opposed to the if: condition)
# because it'll just fall down to the 'return render_template' whereby it just renders the login page again.

# with everything done, you should now be able to do a fake login with the email & password you specified
# i.e. email 'admin@blog.com' and password 'password'

lb(3)
# now, one very quick thing:
# when you pasted in the snippet of your navigation bar into your layout.html template,

# the navitation bar currently is using the direct links to your different routes
# and this should work fine some of the times, but if you ever change the route for any reason
# you want your website to pick that up automatically instead of having to manually make changes in multiple locations.

# as you've seen several times now, you can do that using the url_for() function.
# you definitely want to utilise that function a lot
# because it makes linking to different pages pretty effortless.

# the only way this was not considered in the previous notes
# is that the login and register routes did not exist back then.
# and using url_for for a non-existing route would have thrown an error.

# let's see what this looks like to convert existing links to the url_for() function.

# go back and open up the layout.html template
# if you go back to your navigation links (at line 33):

"""
        <div class="collapse navbar-collapse" id="navbarToggle">
            <div class="navbar-nav mr-auto">
              <a class="nav-item nav-link" href="/">Home</a>
              <a class="nav-item nav-link" href="/about">About</a>
            </div>
            <!-- Navbar Right Side -->
            <div class="navbar-nav">
              <a class="nav-item nav-link" href="/login">Login</a>
              <a class="nav-item nav-link" href="/register">Register</a>
            </div>
        </div>
"""

# you can see that the href='s all show the direct links (e.g. "/home", "/about", "/login", "/register")
# instead of the names of the routes themselves (e.g. 'home', 'about', 'login', 'register')

# i.e. change each direct link:
# href="/home" to href="{{ url_for('home') }}"
# href="/about" to href="{{ url_for('about') }}"
# href="/login" to href="{{ url_for('login') }}"
# href="/register" to href="{{ url_for('register') }}"

# and now confirm that the changes present no error,
# by returning to the webbrowser and clicking around on the navigation bar.

# # # # # # # # # # # # # # # # continue onto flaskblog10.py # # # # # # # # # # # # # # # #
