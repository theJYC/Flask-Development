def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the twenty-second note on building a python flask application *
~lb(0):
~lb(1):
~lb(2):

'''
#____________from previous flask notes (+ modification)____________

from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# in flaskblog21.py,
# you built a pretty good account page whereby user can update their info.

# now let's focus on getting this set up,
# so that they can change their profile picture.

# to do this, you're going to add a new field to your form
# that is an input type of file.

# go back to forms.py in your project directory
#[a]: on top of the module, you're going to import a couple more things from flask_wtf:

#[a] from flask_wtf.file import FileField, FileAllowed

# now the 'FileField' is going to be the type of field that this is,
# and 'FileAllowed' is going to be just like a validator
# where you can say what kind of files you want to allow uploaded.
# and, in this case, since you're uploading images,
# you can restrict it to something like .jpg and .png files.

# with those two imported,
# go down to the UpdateAccountForm(),
# and right above the submit (and below the email) fields,

#[b]: add a new 'picture' field
# and just like your other field, you can pass in the label for the field 'Update Profile Picture'
#(remember that the field label is what is visible on the page)

# with the label passed in, now pass in the validator.
# this field will only have one validator, FileAllowed(),
# and the arguments that will be passed into FileAllowed() will be a list of allowed file formats
# which, in this case, is going to be 'jpg' and 'png'

'''
[0] class UpdateAccountForm(FlaskForm):
[1]     username = ... ... ...
[2]
[3]     email= ... ... ...
[4]
[b]     picture=Filefield('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
[5]
[6]     submit= ... ... ...
'''

# with the 'picture' field created into the UpdateAccountForm in forms.py,
# now you need to make sure that this field is going to be rendered into the template.

# pull up the account.html template,

# and right above the <div class="form-group"> </div> that contains the submit field,
# you'll add in the picture field.

#[a]-[i]: now this is going to be a little different to your other fields.

# if you get any validation errors back,
# these errors are a bit different for this file-form field,

#[d]: so you'll just use a simple span to spit out those errors
# you will put in a conditional {% if form.picture.errors %}
#[e]-[g]: and loop over these just like you did with the erros in your other fields,

#[h]: and make sure to close the if conditional

#[f]: for any error, you want to print error, with a </br> (break) put in after the <span></span>
# so that you can get some spacing between those,
# and also give the span a class of "text-danger",
# which will just make sure the error message will be outlined in red text.

# note: you didn't have to do that in your other forms
# because the erros in your other forms were wrapped in the <div class="invalid-feedback"></div>
# but this is a different kind of field (FileField) so you had to do this a little differently.

'''
[a] <div class="form-group">
[b]     {{ form.picture.label() }}
[c]     {{ form.picture(class="form-control-file") }}
[d]     {% if form.picture.errors %}
[e]         {% for error in form.picture.errors %}
[f]             <span class="text-danger">{{ error }}</span></br>
[g]         {% endfor %}
[h]     {% endif %}
[i] </div>
'''

lb(1)
# one thing that you may always forget to do
# is to add a special encoding type for your form.
# and you have to do this in order for your form to process your image data properly.

# so, at the top of the form (on line 11 of account.html),
# also add an encodying type (enctype)

'''
before: <form method='POST' action=''>
after:  <form method='POST' action='' enctype="multipart/form-data" >
'''

# absolutely make sure to put that in,
# because if you don't, the errors that you get will not be entirely obvious.

# now, if you reload the browser,
# you'll see, at the bottom of the /account page, a new input
# whereby you can choose a new profile picture.

# you don't yet have the logic in place to save those images yet,
# but your validation should already work
# if you try to upload anything other than a .jpg or a .png file format.

lb(2)
# now let's actually add the logic to your route
# to actually be able to save a profile picture
# and have it saved for your user.

#so if you go to the account route in routes.py,
#[4]: within your if form.validate_on_submit(): conditional,

#[a]:go ahead and add another conditonal to see if there's any picture data.
#because that's not a required field so you're going to have to make this check.

#and now, within this conditional,
#you want to set the user's profile picture.

#the code to set the user's profile picture
#is logically its own little section of code,
#so it would be nice to just turn this into a different function.

#go ahead and create a new function above the account route:
#[b]:defining the save_picture function, and passing in form_picture as an argument

#now, inside the save_picture function,
#you'll put the logic of saving the picture the user uploaded into the file system.

#first, you don't really want to keep the name of the file they uploaded
#because it might collide with the name of an image that's already in your folder.

#with that considered, it would be nice to just randomise the name of this image
#with something like a randomhex.

#one particular module from which you can import the random hex function is the secrets module.
#[c]: make sure to import secrets up top of routes.py.

#now, inside the save_picture() function,
#create a random hex that will be the base of your file name.

#[d]: random_hex = secrets.token_hex(8)

#and now you need to make sure to be saving this file
#with the same extension as it was uploaded
#(e.g. if they uploaded a .png, the filename will be saved as ''.png)

#and in order to grab the file extension from the file that they uploaded
#you can use the os module.

#[e]: import os

#and now you can use the os.path.splitext() function to get this extension.
#and this function returns two values for e.g. filename.png ('filename', '.png')

#to grab both of those values, you can write:
#[f]: f_name, f_ext = os.path.splitext(form_picture.filename)

#now, the argument will be the form picture that they uploaded (form_picture)
#the form_picture is going to be the data from the field that the user submits,
#and if it's a file, it does have the .filename attribute so you can use that.

#now, you're not actually going to use the f_name variable at all,
#you're just going to use the f_ext extension,

#one thing that people do in python
#when they want to throw away a variable name
#is to use an underscore;

#[g]: i.e. change 'f_name' to '_'.

#n.b. if you don't use an underscore,
#your text editor might gripe about you having a variable that is unused in your application.

#now let's combine the randomhex with the file extension
#in order to get the filename of the image that you're going to save.

#[h]: so set picture_fn (for filename) to random_hex + f_ext
#which will just concatenate the two together.

#now you need to get the full path to where this image will be saved
#so that python knows where you're saving this.

#to do this, you're going to use an attribute that you haven't seen yet: the root_path .
#root_path attribute of your application will give the route path of your application,
# all the way up to your package directory.

#if you want to save this image into profile_pics within your static folder,
#[i]: then you can create a variable called picture_path,
#and you are setting that to:

'''
-app.root_path: which is going to give you the full path,
all the way up to the package directory
-'static/profile_pics': profile_pics folder within the static directory
-picture_fn: which will be the picture filename
(that is the concatenated product of random_hex and f_ext).
(n.b. picture_fn is a variable (and not a string) so make sure not to enclose it within quotes)

'''
#using the os.path.join will make sure
#that all of those will be concatenated properly into one long path.

#[j]: then you can actually save that image by using form_picture.save():
#passing in the path whereby you want to save this, i.e. picture_path

'''
[c] import secrets
[e] import os

[b] def save_picture(form_picture):
[d]     random_hex = secrets.token_hex(8)
[f][g]  _, f_ext = os.path.splitext(form_picture.filename)
[h]     picture_fn = random_hex + f_ext
[i]     picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
[j]     form_picture.save(picture_path)


[0] @app.route('/account', methods=['GET', 'POST'])
[1] @login_required
[2] def account():
[3]     form = UpdateAccountForm()
[4]     if form.validate_on_submit():
[a]         if form.picture.data:
[6]
[0]         current_user.username = form.username.data
[0]         current_user.email = form.email.data
[0]         db.session.commit()
[0]         flash('Your account has been updated', 'success')
[0]         return redirect(url_for('account'))
'''


# # # # # # # # # # # # # # # # continue onto flaskblog23.py # # # # # # # # # # # # # # # #
