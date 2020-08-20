def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the nineteenth note on building a python flask application *
~lb(0): @app.route('/account')
~lb(1): 'Please login to access this page'
~lb(2): tailoring 'Please login to access this page' alert
~lb(3): the 'next' query parameter
'''
#____________from previous flask notes (+ modification)____________

from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# the last thing that is to be covered
# is how to put restrictions on certain routes so that
# you can only go to those sites if you're logged in.

# e.g. if you go on Glassdoor, if you were to browse around the different reviews
# you'll soon be hit with a 'You need to log in before accessing site content' page
# which basically restricts you from continuing with the rest of the page until you log in/sign up.

# let's to something like that on your site.

# i.e. let's create an a route for the user's account
# that they can access after they've logged in.

# [0][1] first, create that route by opening up routes.py.

#[2] you need to create a designated account.html template
# for now, let's return the template for the route that you're about to create

'''
[0] @app.route('/account')
[1] def account():
[2]     return render_template('account.html', title='Account')

'''

# within your templates directory ('/Flask_Blog/flaskblog/templates')
# create a new file 'account.html'.

# as a starting point for account.html,
# copy and paste the content of the about.html template,
# and modify the content block to just display the current user's username {{ current_user.username }}:

'''
[0] {% extends 'layout.html' %}
[1] {% block content %}
[a]     <h1>{{ current_user.username }}</h1>
[2] (% endblock content%)
'''

# making sure to add a link to this route within your navigation bar if the user is logged in:
#(navigation bar is located within layout.html)
# this is going to be visible if the user is logged in,
# so right above your Logout link [*]:

'''
[0] {% if current_user.is_authenticated %}
[a]     <a class="nav-item nav-link" href="{{ url_for('account') }}">Account</a>
[*]     <a class="nav-item nav-link" href="{{ url_for('logout') }}">Logout</a>
[1] {% else %}
'''

# restart the server in terminal,
# and go back to your homepage to find that you now see another link 'Account' in the navigationbar
# to the left of the 'Logout' link.
# and if you click on the 'Account' link
# it displays the current logged in user's username.

# but if you now try to 'Logout'
# and manually try to direct yourself to 'localhost:5000/account',
# you can see that that you don't get anything on this screen anymore
# because you're not a currently logged in user anymore
# and hence it doesn't know what username to display.

lb(1)
# so you want to put a check in place
# that makes a user log in before accessing the 'Account' page.

# it's very easy to do that;
# you can use the login_required decorator from the flask_login extension!

# 0: return to routes.py
# 1: add login_required to the list of modules to be imported from flask_login
# 2: simply add the @login_required decorator below the @app.route('/account') decorator in the account route:

'''
[0] @app.route('/account')
[a] @login_required
[1] def account():
[2]     return render_template('account.html', title='Account')
'''

# now your extension knows that you need to have logged in in order to access the /account route.
# but you also need to tell the extension where the login route is located!

# to do this you need to go back to the __init__.py file,
# where you first initialised this application,
#[0] and right under where you created the instance of the LoginManager(app),
#[a] you can set the login route:

'''
[0] login_manager = LoginManager(app)
[a] login_manager.login_view = 'login'
'''

# note: the view that you pass in here ('login') is the function name of the url route
# which is the same as what you put into the url_for() method.

# now, when you try this again in your browser:
# having logged out, direct yourself to 'localhost:5000/account',
# and you'll now be prompted with a 'Please log in to access this page' message
# and redirected to the login route.

lb(2)
# now there are just two more things
# that need to be done to clean up the app a little bit.

# the flashed message telling you to log in is noticeably ugly,
# and untill now you have been using the flashed categories to add a class to those flashed alerts

# now to do this within the 'Please log in to access this page' message,
# you can go back to the __init__.py file
# and just add another line 'login_manager.login_message_category',
# and set that equal to the category that you want it to be,
# which in this case, is what you're using for the Bootstrap classes
# so set it equal to 'info' for the info class
# which in Bootstrap is a nicely coloured blue information alert:

'''
[0] login_manager = LoginManager(app)
[1] login_manager.login_view = 'login'
[a] login_manager.login_message_category = 'info'
'''

lb(3)
# and the last thing that you want to do to improve this
# is when you try to access the 'Account' page when you're logged out,
# it directed you to the login, which is good.

# but after you logged in,
# it first redirected you to the home page
# and you had to access the Account page from there
#(by clicking the 'Account' link in the navigation bar)

# so it would be nice if, when logged in,
# it just redirected you back to the 'Account' page
# (which, after all, is the page you were trying to access-
# -before it told you that you have to log in).

# and this is easy to do aswell.
# now, if you haven't noticed it yet,
# when you tried to access the Account page and it directed you to Login first,
# it added a query parameter to the URL of the page that you were trying to access:

''' http://localhost:5000/login?next=%2Faccount '''

# the query parameter 'next' is equal to the route
# that you were trying to log into before you got redirected

# so in your login route,
# let's access that query parameter.

# and if it exists,
# you will direct the user *there* after they log in.

# 0: you're going to be accessing query parameters
# and you will need to import the request object from flask

''' from flask import request '''

#[1]: go down to the login route,
#[2]: now, you want to get this *after the user logs in*
#(which is the 'login_user(user, remember=form.remember.data)')

#[a]: then you can get the next parameter from the url, if it exists,
# by saying 'next_page = request.args.get('next')'

# note: args is a dictionary
# but you don't want to access 'next' using square brackets and key names
# because that would throw an error if the key doesn't exits.

# and the next parameter is going to be optional.
# so if you use the .get() method, it would simply return None if the next key doesn't exists.
# i.e. be sure to be using the .get() method
# instead of the square brackets and the key that you might be used to.

# to recap, if the 'next' parameter exists, the next_page variable will be equal to that route
# and if it doesn't exists, next_page will be equal to None.

#[b]: now, in the return statement below,
# modify it to redirect to next_page if next_page is not none,
# else redirect to home page:

'''
[1]@app.route('/login', methods=['GET', 'POST'])
[.]    (irrelevant code above)
[2]    login_user(user, remember=form.remember.data)
[a]    next_page = request.args.get('next')
[b]    return redirect(next_page) if next_page else redirect(url_for('home'))
'''

# note: [b] is something called a ternary conditional
# you are basically saying 'redirect to next_page' if next_page exists
# but if next_page is None or False, return the redirect to this homepage.

# now if you restart the server and manually access '/account' upon logging out,
# if you successfully re-login, you'll now be immediately directed to '/account' instead of '/home'.

# you also want to make sure that it directs you to '/home' if the next parameter doesn't exist
# so if you log out and click 'login' link
# and since you went there directly (instead of being prompted to it from '/account')
# that next parameter doesn't exist in the URL 'localhost:5000/login'

# and now, if you log in again,
# you can see that this log in (whereby 'next' parameter did not exist) directs you to '/home'


# # # # # # # # # # # # # # # # continue onto flaskblog20.py # # # # # # # # # # # # # # # #
