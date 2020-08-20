def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the twentieth note on building a python flask application *
~lb(0): adding default profile_pic to account.html
        (from '/static/profile_pics' directory)
~lb(1): creating UpdateAccountForm for account page

'''
#____________from previous flask notes (+ modification)____________

from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# in this series of notes
# you'll be finishing the user account page where your user can update their information,
# and you'll also give them the ability to upload a profile picture aswell.

# firstly, let's update the account.html template for the account page.
# currently, account.html looks like this:
'''
[0] {% extends "layout.html" %}
[1] {% block content %}
[2]     <h1>{{ current_user.username}}</h1>
[3] {% endblock content %}
'''

# go to snippets folder and paste in the additional html [a]-[j]
# into the content block:

'''
[0] {% extends "layout.html" %}
[1] {% block content %}
[a]     <div class="content-section">
[b]       <div class="media">
[c]         <img class="rounded-circle account-img" src="userimage.jpg">
[d]         <div class="media-body">
[e]           <h2 class="account-heading">Username</h2>
[f]           <p class="text-secondary">username@email.com</p>
[g]         </div>
[h]       </div>
[i]       <!-- FORM HERE -->
[j]     </div>
[3] {% endblock content %}
'''

# n.b. this HTML has some Bootstrap classes to make everything look nicer
# plus some styles from the main.css file that you added earlier to the 'static' directory
# which is referenced in your layout.html template.

# in the snippet that you pasted in here,
# you have an image for the user's image and that is currently hardcoded into "userimage.jpg"

# you also have the <h2> heading with the user's username
# and a <p> tag with the user's email.

# so let's change the username and email on [e] and [f]
# to be the current user's username and email:

'''
[e]           <h2 class="account-heading">{{ current_user.username }}</h2>
[f]           <p class="text-secondary">{{ current_user.email }}</p>
'''

# you also have an image here for the user's profile picture on [c],
# with the source for the user hardcoded in,

# but you want this to be set to the user's image if they've uploaded one,
# and to display a default image if they haven't uploaded an image.

# if you remember from 'Part 4-Database' notes in flaskblog10-12,
# you set the user's image to be equal to default.jpg by default:

''' image_file = db.Column(db.String(20), nullable=False, default='default.jpg') '''

# so you need to actually create this default image so that you can display that for now.

# and you can use any image as the default user image,
# though make sure to add that to the project directory's static folder ('./flaskblog/static')
# so that you can use the url_for() function to grab that image.

# once you've moved the desired default image to the static folder,
# go ahead and update the hardcoded image source within the account.html template,
# to be equal to the user's image (which will be default.jpg if they haven't uploaded any image yet)

# you're actually going to set this in your routes and pass it into your template.

# first, open up routes.py file,

#[1]:navigate to the bottom where the account route is,

#[a]: and set the image_file that you want to pass to that template.

'''
[0] @app.route('/account')
[1] @login_required
[2] def account():
[a]     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
[3]     return render_template('account.html', title='Account')
'''

# so you now have an image_file variable that is set to the url_for() your static directory,
# and within your static directory, the profile_pics folder, and then the user's image file.
#(flaskblog/static/profile_pics/).

# now let's pass that image file into the account template [3].
# just like you've done before, you can just pass additional arguments into render_template()

'''
[a]     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
[b]     return render_template('account.html', title='Account', image_file=image_file)
'''

# now, within the account.html template,
# you can use the image_file as the source (src)
# instead of the hardcoded filler value 'userimage.jpg' that you currently have [c]:

''' <img class="rounded-circle account-img" src='{{ image_file }}'> '''

# n.b. making sure to put in image_file within the double curly braces since it's a variable.
# n.b.2. also make sure that the double curly braces are also enclosed within quotes ''.

# now, saving all the files you made changes to,
# load up the server again and see the basic account page that you created.

# as you can see, this basic account page shows your default image, username, and email.

lb(1)
# now, within this account page,
# you also want to be able to update your username and email address
# and also upload a personal profile picture aswell.

# and you'd need to create forms for that.

# open up forms.py in your project directory,
# whereby you're going to create a form to update user's account information.

# and this is going to be similar to the RegisterForm,
# because it's going to allow you to update your username and email address.

# i.e. copy everything enclosed within class RegistrationForm(FlaskForm),

# and make the following modifications:

#[a]: change name from 'RegistrationForm' to 'UpdateAccountForm'

#[0]-[3]: keep 'username' and 'email' fields but delete 'password' and 'confirm_password'
# since you don't need the latter two.

# note: you are going to have the ability to update password,
# but it's not going to be through this form.

#[b]: change 'SubmitField('Sign Up')' to 'SubmitField('Update')'.

# and, for the username and email validations,
# these are going to stay pretty similar.

# but you have to realise:
# your user could submit this form
# without actually changing either their username or email
# and that should still be valid.

# the way that this is set up right now in RegistrationForm,
# is that it will query the database and find their current username and email in the database
# and see that the value is taken and throw a ValidationError.

# so you only want to run these validation checks
# if the data that they submit is *different* than their current username and email.

#[-]: so let's import the current user from flask_login
# so that you can use that to make this check.

# then go back down to the UpdateAccountForm,

# and now you want to say that you only want to do these validation checks
# if the username/email that they entered is different from their current username and email.

# i.e. for the username validation check on [6],
#[c]: you could say that if username.data (the username they entered)
# is *not* equal to the current_user.username
#(the username that is in the database for this current user)
#(hence, if username.data *is* equal to current_user.username, you're just not going to validate it)

#[d]: copy and paste the conditional [c] and modify it for the email validation check:

'''
[-] from flask_login import current_user
[a] class UpdateAccountForm(FlaskForm):
[0]     username = StringField('Username', validators=[
[1]                            DataRequired(), Length(min=2, max=20)])
[2]
[3]     email = StringField('Email', validators=[DataRequired(), Email()])
[4]
[b]     submit = SubmitField('Update')
[5]
[6]     def validate_username(self, username):
[c]         if username.data != current_user.username:
[7]             user = User.query.filter_by(username=username.data).first()
[8]             if user:
[9]                 raise ValidationError('Username already exists')
[10]
[11]    def validate_email(self, email):
[d]         if email.data != current_user.email:
[12]            user = User.query.filter_by(email=email.data).first()
[13]            if user:
[14]                raise ValidationError('Email already exists')
'''


# # # # # # # # # # # # # # # # continue onto flaskblog21.py # # # # # # # # # # # # # # # #
