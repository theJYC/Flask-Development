def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the eighteenth note on building a python flask application *
~lb(0): restructuring login logic
        (by querying database & matching entered login with existing account info.)
~lb(1): modifying UX upon login
~lb(2): redesigning nav bar upon login
'''
#____________from previous flask notes (+ modification)____________

from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# now let's modify your login route so you can see how this works
# see how [0]-[9] are transformed to [a]-[8]

# up till now, here is how the login route was structured:
'''

[0] @app.route("/login", methods=['GET', 'POST'])
[1] def login():
[2]     form = LoginForm()
[3]     if form.validate_on_submit():
[4]         if form.email.data == 'admin@blog.com' and form.password.data == 'password'
[5]            flash('You have been logged in!', 'success')
[6]             return redirect(url_for('home'))
[7]         else:
[8]             flash('Could not log in. Please check username and password')
[9]         return render_template('login.html', title='Login', form=form)

'''
#[n] lines numbered for coherence.

# so, before you were simply checking hardcoded username and password [4]
# whereas now, you're going to be checking your database if the username and password are valid.

# so delete what you have within your if form.validate_on_submit(): conditional (lines [4][5][6][7])
#[a]-[e]: and let's put in the logic for logging in a user:

'''
[0] @app.route("/login", methods=['GET', 'POST'])
[1] def login():
[2]     form = LoginForm()
[a]     if form.validate_on_submit():
[b]         user = User.query.filter_by(email=form.email.data)
[c]         if user and bcrypt.check_password_hash(user.password, form.password.data):
[d]             login_user(user, remember=True)
[e]             return redirect(url_for('home'))
[7]         else:
[8]             flash('Could not log in. Please check email and password')
[9]     return render_template('login.html', title='Login', form=form)
'''

# first of all, they'll be logging in with their email.
# so let's query your database so that you know that your user exists.

#[b]: you want to filter if there are any emails in the database
# with the same email that the user inputed into the login form.
# and if so, you just want to get the first user back with that email
# and if there isn't one, it'll just return None.

#[c]: now you're going to make a conditional that simultaneously checks that the user exists
# and that their password verifies with what they have in the database
# i.e. pass into bcrypt.check_password_hash() 1) user.password (which is what comes from the database)
# and the second value is the form.password.data (the password they entered into the form)

# if the user exists and the password that they entered is valid with what's in the database,
# then you want to log the user in.

# to log them in using the flask_login extension,
# you need to import the login_user function

#[d]: so you can now simply use the function to log the user in
# passing in the user (one that is to be logged in) and
# also remember that you have a 'Remember me' in the LoginForm
#(remember = BooleanField('Remember Me'))
# the login_user function takes a remember argument aswell.
# so you can write in remember=form.remember.data (which is just going to be a True/False value)

# and that will log in the user.

#[e]: after they're logged in, let's redirect them to the home page.

#[7]: and if they submitted the form and it *did not* meet the conditional (on line [c])
# of being a valid email or a password,
#[8]: then let's just keep the flashed message from before,
# after altering the 'Please check [username]' to 'Please check [email]'

#[9]: so if it wasn't a successful login,
# it would never reach 'return redirect(url_for('home'))' on [e]
# and they'd just be redirected to the login page.

lb(1)
# one thing that is strange here,
# is that once you log in, you still see the Login and Register routes
# in your navigation bar on the home page.

# and if you click on one of those routes,
# you can see that you can get back to the login page.
#(even though you're already logged in)

# but really, if the user is already logged in,
# and they try to go to the Login or Register pages,
# then you should really just redirect them to the homepage
# because they don't need to be on those pages if they're already logged into their account.

# in order to tell whether a user is currently logged in,
# you can use the 'current_user' variable from the flask-login extension

# first import current_user from flask-login (in routes.py)
# now, at the top of your login and register routes,

# write in:
'''
if current_user.is_authenticated:
    return redirect(url_for('home'))
'''

# see below for the example on register route:

'''
[0] @app.route('/register', methods=['GET', 'POST'])
[1] def register():
[a]     if current_user.is_authenticated:
[b]         return redirect(url_for('home'))
[2]     form = RegistrationForm()

'''

# n.b. [a]lphabet signs are where the change is introduced
# and [0] number signs indicate exisitng code

# make sure to apply the same to the login route!

# the result, if you pull up the webserver again,
# is that if you try to log in/register once you're already logged in,
# you'd now be redirected to the home page.

lb(2)
# now it's even stranger that you see those links when you're logged in;
# most websites will replace those with a logout link if you had logged in.

# let's create a logout route to logout your user,
# and then you'd display the logout route in your navigation bar when the user is logged in.

# just like you used the login_user function from flask-login to log the user in,
# you're going to use the logout_user function (after importing it) to log the user out.

#[a][b]: first, create the route using normal flask format

# within this route,
#[c]: you simply just need to log the user out
# in the form of the function logout_user().

# n.b. this function will not take in any argument
# because it already knows what user is already logged in.

#[d]: and once the user is logged out,
# let's redirect them to the homepage.

'''
[a] @app.route('/logout')
[b] def logout():
[c]     logout_user()
[d]     return redirect(url_for('home'))
'''

# and then, you also want to actually see this logout link in the navigation,
# if the user is logged in.

# in this case, you'd have to change the layout.html template where navigation is created.

# open up layout.html in your templates folder,
# and right where you put in the Login and Register buttons on the navigation bar
# which looks like below:

'''
[0] <!-- Navbar Right Side -->
[1]             <div class="navbar-nav">
[2]               <a class="nav-item nav-link" href="{{ url_for('login') }}">Login</a>
[3]               <a class="nav-item nav-link" href="{{ url_for('register') }}">Register</a>
[4]             </div>

'''

# you're going to put in a jinja 2 conditional
# and use that same 'if current_user.is_authenticated:' check that you used before.

#[a]: open up a code block {% if current_user.is_authenticated %}
# i.e. 'if the user is logged in':

#[b]: you want to add the logout route.
# copy and paste in one of the Login / Register links on [2][3],
# and modify it to house the logout route instead

#[c]: also making sure to put in the {% else %} block
# which would otherwise display the Login / Register routes to the currently not logged-in.

#[d]: and lastly remember to close out the if statement by {% endif %}
'''
[0] <!-- Navbar Right Side -->
[1]             <div class="navbar-nav">
[a]               {% if current_user.is_authenticated %}
[b]                 <a class="nav-item nav-link" href="{{ url_for('logout') }}">Logout</a>
[c]               {% else %}
[2]                 <a class="nav-item nav-link" href="{{ url_for('login') }}">Login</a>
[3]                 <a class="nav-item nav-link" href="{{ url_for('register') }}">Register</a>
[d]               {% endif %}
[4]             </div>

'''

# now save layout.html, routes.py and load up the server to check the changes.


# # # # # # # # # # # # # # # # continue onto flaskblog19.py # # # # # # # # # # # # # # # #
