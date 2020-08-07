def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the second note on building a python flask application *
~lb(0): updating your code to include some HTML
~lb(1): running your application on debug mode
~lb(2): running your application without environment variable
~lb(3): adding another route (About Page)
~lb(4): adding another route for the same function

'''
#____________from previous flask notes (+ modification)____________

from flask import Flask
app = Flask(__name__)


@app.route('/')  # refer to line E
@app.route('/home')
def home():
    return '<h1>Home Page</h1>'  # refer to line A & line B


@app.route('/about')  # refer to line D
def about():
    return '<h1>About Page</h1>'


if __name__ == '__main__':  # refer to line C
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# so now let's actually update your code to include some actual HTML.

# Line A: you're going to wrap the text here in h1 tags which are HTML heading tags,
# which should make your text appear larger.

# n.b. if you're updating an already-running webserver,
# you need to stop the webserver first (i.e. ctrl + C on Terminal command)
# and then re-run flask

# fyi: within chrome and other browsers aswell,
# you can view the sourcecode of any HTML page by:
# right-click anywhere on the website, and select 'View Page Source'
# returns: <h1>Hello World!</h1>

lb(1)
# so most likely, when you're developing a site,
# you're going to be making a lot of changes to your application,
# and it would be a major pain to have to shut down and restart the webserver each time you make a small change.

# now, you can actually get around this and have the server show changes without restarting your application,
# just by running your application on debugmode.

# one way to do this is to pull up your Terminal
# and set another environment variable to FLASK_DEBUG
# by typing 'export FLASK_DEBUG=1'

# now if you run this application, straight away there is additional information here:
# returns:
'''

 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 277-992-408

'''
# and if you go back to the webbrowser and refresh it, you can see that it is still working.

# Line B: to illustrate, the text was modified from 'Hello World!' to 'Home Page' on the code above,
# and you can see that change take effect just by refreshing the webbrowser.

# i.e. this change reloaded automatically since you're in debug mode.
# you didn't have to restart that webserver like you did before.

lb(2)
# also, if you don't want to work with those environment variables,
# there is another way to run your applications using python.

# Line C:write in the conditional 'if __name__ == '__main__': app.run(debug=True)
# the __name__ is '__main__' if you run this script with python directly.
# but if you import this module to somewhere else, then the name will be the name of your module.
# i.e. this conditional is only true if you run this script directly.

# now, pull up Terminal and, instead of doing 'flask run' that uses the environment variables,
# you could instead just call this script (flaskblog2.py) directly.
#type in 'python flaskblog2.py'

# you can see that you get a similar output, so go back to your browser and refresh your page.

lb(3)
# now that you have this running (directly from python too!)
# let's add another route just to illustrate how easy this is with flask.

# e.g. say you wanted to add an 'About' route to make an About page for your website.
# at this present moment, if you were to simply type in '/about' towards the tailend of localhost:5000,

#i.e. localhost:5000/about
# returns:

'''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
'''

# you will also produce an output on Terminal window that will correspond to the 404 error:
# returns: 127.0.0.1 - - [03/Aug/2020 19:09:39] "GET /about HTTP/1.1" 404 -

# you can see that the GET request returned a 404 response (meaning 'Page doesn't exist!')

# so let's create that About page.
# Line D: copy and paste the Home Page route, and then change a couple of things here.
# for the route, modify to ('/about') from ('/'),
# and change the function name too, to about(): from hello():.
# and lastly, change the text-to-return to '<h1>About Page</h1>'

# now you have a route at /about, and this about() function is returning the information (About Page) for that page
# and when you go back to the browser, you can see that the About Page now runs successfully
#(while Home Page also functions at the same time, which can be accessed by removing '/about' in the URL)!

lb(4)
# now if you wanted to have multiple routes handled by the same function,
# then it's as simple as adding another decorator.

# let's say that you wanted a route of '/home' to direct you to the Home Page, as well as the '/'.
# Line E: just write in @app.route('/home') right below @app.route('/')

# now both the 'localhost:5000' and 'localhost:5000/about' URLs will direct you to the Home Page.

# # # # # # # # # # # # # # # # continue onto flaskblog3.py # # # # # # # # # # # # # # # #
