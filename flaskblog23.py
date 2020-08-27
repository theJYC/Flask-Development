def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the twenty-third note on building a python flask application *
~lb(0):
~lb(1): image auto-resizing
~lb(2):

'''
#____________from previous flask notes (+ modification)____________

from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# now at this point, you've actually saved that picture to the file system,
# but the user's image in the database is still set to the default image.
# so you'll need to update that.

# but since this function is just about saving your image so far,
# let's not put that logic in here.

#[a]: instead, let's just return the picture's filename that you created
# so that the user can use that value outside of this function.

# now, back in the conditional that you were writing before creating that function,

#[b]: you can use that function (save_picture()) to save your picture
# and give you back your filename.

# just like you did with username and email,

#[c]you can now set the current_user.image_file to the picture_file
# that was returned from the save_picture(form.picture_data) function.

'''
    def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
        form_picture.save(picture_path)

[a]     return picture_fn

    @app.route('/account', methods=['GET', 'POST'])
    @login_required
    def account():
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:
[b]             picture_file = save_picture(form.picture.data)
[c]             current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated', 'success')
            return redirect(url_for('account'))
'''

lb(1)
# right now,
# you're just accepting any image that the user uploads.

# but the largest image on your site right now (i.e. your uploaded profile picture)
# is just set in CSS to a 120 pixels.

# so there would be no use in having a 4000-pixel image
# that would just be scaled down to 120 pixels.

# it'll take up a lot of space in the file system,
# and it'll also cause your website to run slow
# because it has to send that large image to the browser every time.

# i.e. if you were to upload a large image,
# it'll upload fine, but it'll look small because it is scaled down in CSS.

# if you right click on the image and click 'Open Image in New Tab',
# you can see that the image is actually pretty -redundantly- large

# let's resize these large images before they're saved to the file system.

# to do this, you're going to be using a package called 'pillow',
# that will be used to resize this image to a 450 pixels.

# first, pip/pipenv install Pillow .

# then, on top of the routes.py file, write:

''' from PIL import Image '''

# and now, return to the save_picture function above the account route,
# to put in the resizing functionality before you save it at [5] 'form_picture.save(picture_path):

#[a]: set an output_size to a tuple of the size that you want (450 x 450 pixels)

# and then you can create a new image (i),
#[b]: and set the new image to Image.open() whereby form_picture (that was passed into save_picture())
# will be passed in as an argument.

#[c]: to resize, use the .thumbnail method
# and pass in the desired size that was determined above (output_size)

# finally, you want to save the new image (i)
# i.e. the resized version of form_picture:

#[d]: modify 'form_picture.save(picture_path)' to 'i.save(picture_path)'


'''
    def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

[a]     output_size = (450, 450)
[b]     i = Image.open(form_picture)
[c]     i.thumbnail(output_size)

[d]     i.save(picture_path)

        return picture_fn
'''

# fyi: additional code was added in order to delete the old profile pictures in the file system
#(i.e. only the most recently updated profile picture will remain in /static/profile_pics)

# the code for deleting the old profile pics is as follows (it was extracted from a YT comment):

'''
if form.picture.data:
            old_picture = current_user.image_file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            if old_picture != 'default.jpg':
                os.remove(os.path.join(app.root_path,
                                       'static/profile_pics', old_picture))
'''


# # # # # # # # # # # # # # # # continue onto flaskblog24.py # # # # # # # # # # # # # # # #
