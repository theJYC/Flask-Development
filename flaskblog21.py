def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the twenty-first note on building a python flask application *
~lb(0): incorporating UpdateAccountForm into @app.route('/account')
~lb(1): enabling the account update from routes.py
~lb(2): pre-populating the account form with username and email

'''
#____________from previous flask notes (+ modification)____________

from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# now, return to routes.py,
#[a]: to import the newly-created UpdateAccountForm to your routes

#[0]-[2]: and then, head down to the account route
#[b]: whereby you'll create an instance of that form
#(similar to what's been done with login/register routes!)

# and now pass in this form into the render_template on [c]
#[d]: with form='form' as the last argument of the function
# note: [c][d] were broken into two lines to be PEP-8 compliant

'''
[a] from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm

[0] @app.route('/account')
[1] @login_required
[2] def account():
[b]     form = UpdateAccountForm()
[3]     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
[c]     return render_template('account.html', title='Account',
[d]                            image_file=image_file, form='form')
'''

# you'll add the form validation logic here in this route in just a second,
# but first, let's just get this displaying in your template.

# as was discussed earlier, the UpdateAccountForm()
# is similar to the RegistrationForm() with just fewer fields.

# go and open up the register.html template
# and grab the code you used for that so that you can reuse it.

# i.e. copy the entire <div= class "content-section"></div> within the {% block content %}
# and then within the account.html template,
# drop the copied div class into the bottom of the template.

# ok now this is similar to the RegistrationForm but *not exactly the same*.
# so you're going to keep the username and the email fields,
# but you want to get rid of the password and the confirm_password fields.

#(you're going to get rid of the entire <div class="form-group">'s that surround those)

# and lastly, go up to the top to the <legend class="border-bottom mb-4"></legend> (on line 15)
# and modify the text from 'Join today' to 'Account Info'

# with all that done, reload the browser and take note of the new Account page
# with its Account Info title, Username and Email fields, and Update button.

lb(1)
# now, none of this currently does anything when you submit this form.
# you're going to set that up right now.

# and another thing that jumps out is that
# it would be nice to have the Username and Login fields already autofilled in
# when you've navigated to this page.

# go to the routes.py file,
# and first you need to add your allowed messages
# because you're going to be posting this form back to this route
# and that is something that is easy to forget when you add new routes with forms.

# go ahead and grab (methods=['GET', 'POST']) from the @app.route('/account'),
# and paste it into the @app.route('/account')
#(so that you're allowing GET and POST requests on '/account')

#[a]: now you want to put in a conditional for if your form is valid when submitted.
# when your form is valid, you can update your username and email.

#[b]: one good thing about SQLAlchemy is that it makes this really easy:
# so you can simply change the values for the current_user variable
# and then commit those.

#[c]: and you can also set the email by doing the same thing

#[d]: and now, all you need to do is commit the changes

#[e]: and finally, let's also add a flashed message
# to tell the user that their account has been updated
#(the Bootstrap category 'success' to flash a green message box)

#[f]: lastly, let's redirect them to the account page.

'''
[0] @app.route('/account', method=['GET', 'POST'])
[1] @login_required
[2] def account():
[3]     form = UpdateAccountForm()
[a]     if form.validate_on_submit():
[b]         current_user.username = form.username.data
[c]         current_user.email = form.email.data
[d]         db.session.commit()
[e]         flash('Your account has been updated', 'success')
[f]         return redirect(url_for('account'))
[4]     image_file = url_for(
[5]             'static', filename='profile_pics/' + current_user.image_file)
[6]         return render_template('account.html', title='Account', image_file=image_file, form=form)
'''


# note: you do want to redirect here on [f]
# instead of letting it fall down to the render_template line on [6]
# because of something called a 'POST, GET, redirect' pattern.

# you might not know what that is, but it is actually a common phenomenon.
# if you've ever reloaded your browser after submitting a form,
# and you see a weird message that says something like,
# 'are you sure you want to reload? data will be resubmitted'.

# and that is because your browser is telling you
# that you're about to run another POST request when you reload your page.

# so, you redirecting causes your browser to send a GET request,
# and then you won't get that ^.

lb(2)
# so that should take care of your users updating their username and email,

# now to have your form already pre-populated with current user's username and email
# as soon as they go to the account page.

# to do this,
# you can add onto your conditional [a],
'''
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
'''

# those changes should populate your form with current user's data.

# now let's check to see if the changes worked:

# first, pull up the site and create a second user
# to see if the validation that you've put in place is working.

#the login for second user will be:
'''
Username: Fredrick
Email: Fredrick.Thompson@gmail.com
Password: password
Confirm Password: password
'''

#once Fredrick (i.e. User 2) is registered,
#log into jinyoung's account (i.e. User 1)
#and now, try to update your Username and Email using the values of Fredrick's account

#evidently, the validation checks are working:
#throwing you the 'Username already exists' and 'Email already exists'.

#and if you were to empty the Username and Email fields and resubmit
#but this time with non-existing credentials (i.e. username='JYCHOI' and email 'jyc@gmail.com' ),
#the update works: 'Your account has been updated',
#and those values in the heading of the account page is also updated.

#and now you'll update the account back to the old credentials,
#which shouldn't be a problem because the old values should no longer exist in the database.


# # # # # # # # # # # # # # # # continue onto flaskblog22.py # # # # # # # # # # # # # # # #
