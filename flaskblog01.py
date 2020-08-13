def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the first note on building a python flask application *
~lb(0): flask is fun: what is going on here?
~lb(1): starting the flask app
~lb(2): updating your code to include some HTML

'''
lb(0)
# flask's official website offers the simplest application you can build on flask,
# named 'Flask is Fun':

from flask import Flask  # [0]
app = Flask(__name__)  # [1]


@app.route('/')
def hello_world():  # [2]
    return 'Hello World!'  # [3]

# now, what is going on here with these four lines of code?

#[0]: importing your flask class from the Flask module

#[1]: then creating this app variable and setting it to an instance of Flask class.
# now, passing in the __name__ an seem a bit confusing,
# but __name__ is just a special variable in python that is just the name of the module *
# *note: if you run the script with python directly,*
# *__name__ can be equal to __main__ (you'll see that in just a second)*
# *(basically, that is so Flask knows where to look for your templates and static files, etc.)*

# so, now that you have an intantiated flask application in this app variable,
# you can then create your routes.
# routes are what you type into your browser to go different pages.
# e.g. you have probably been to a webstie that has 'About' or 'Contents' pages,
# in flask, you create these using route decorators.

# note: you don't need to know the 100% in-and-out of decorators,
# but basically decorators are just a way to add additional functionality to existing functions

#[2]: in this case, the @app.route decorator will handle all of the complicated backend stuff
# and simply allow you to write a function that returns the information that will be shown on your website
# for this specific route.

# this foreward slash (/) is just the route page of your website, which you can think of it as a homepage.

#[3]: and you are simply returning the text "Hello World!"
# this is normally where you would want to return some HTML,
# but you'll start off with this text just to make sure it all works.

# i.e. when you start your application,
# if you navigate to the homepage, it should show you this text "Hello World!"

lb(1)
# to start the app, return to Terminal and navigate to the project directory.
# right click on 'Flask_Directory' folder and select 'New Terminal at Folder'

# before you run your application,
# you want to set an environment variable to the file that you want to be your flask application.

# type 'export FLASK_APP=flaskblog.py' into Terminal
# and once the environment variable is set, simply type in 'flask run' into Terminal
#returns (in terminal):

'''
* Serving Flask app "flaskblog.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
0---------0---------0---------0---------
1---------1---------1---------1---------
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [03/Aug/2020 17:51:46] "GET / HTTP/1.1" 200 -
'''

#the 127.0.0.1 is the IP address of your local machine and
# the :5000/ is the port number.

#note: this is a running webserver (which actually comes with flask itself).
#you have to have this terminal message running while you view your site
#or else you won't be able to see it.

#if you copy the 'http://127.0.0.1:5000/' onto your web browser,
#you should see your sample application (Hello World!)
#this 'Hello World!' is what you returned from your home route.

#n.b. there is also an alias for the IP address '127.0.0.1',
#and that alias is 'localhost'
#i.e. entering 'http://localhost:5000/' into the webbrowser will yield the same (Hello World!).

# # # # # # # # # # # # # # # # continue onto flaskblog2.py # # # # # # # # # # # # # # # #
