def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the third note on building a python flask application *
~lb(0): writing complex HTML on flask app
~lb(1): leveraging templates 101
~lb(2): using render_template
~lb(3): uploading data onto flask app
~lb(4): for loop on flask data via templating engine (jinja 2)

'''
#____________from previous flask notes (+ modification)____________

from flask import Flask, render_template  # refer to line A
app = Flask(__name__)

posts = [  # refer to line D
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
    return render_template('home.html', posts=posts)  # refer to line B, line E


@app.route('/about')
def about():
    return render_template('about.html')  # refer to line C


if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# in the next series of notes, you'll be learning about templates to return more complex HTML code,
# and also how to pass variables into your webpage.

# starting with the same script that you left off in flaskblog2.py,
# you can see in your two route functions that you're returning these two HTML headings.

# but most HTML files have a lot more HTML code than this.
# it contains an entire structure with a headtag, bodytag, etc.
# now, there is nothing stopping you from returning all of that HTML here,

# you could, for example,
# put in three quotes for a multi-line string, and return e.g. <!doctype html> then open up the <html> tag
# and just kind of keep going there.

# but with a lot of tags and routes, this can get really ugly really fast,
# and you'd create a tonne of HTML like this for every single route.

lb(1)
# so the best way to do this is to, instead, use templates.

# to use templates, you first need to create a templates directory within your project.
# now, within your templates directory, create templates for the two routes that you currently have:
# i.e. one for the home() and another for about().

# within the templates folder, create two new files named 'home.html' and 'about.html'.
# n.b. within Sublime Text, if you just type 'html' and press tab,
# you can see that it fills out a minimal html page structure for you:
'''
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>
    [THIS IS WHERE THE HEADING TAG GOES IN lb(2)]
</body>
</html>
'''

lb(2)
# now that you have a basic HTML structure,
# let's add the heading tag you had in your python script into this home.html template.
# e.g. put in the <h1>Home Page</h1> into the <body> <body> of the home.html:
'''
<body>
    <h1>Home Page</h1>
</body>
'''

# and now that you have the home template ready,
# let's actually use this template when you navigate to your home page.

# i.e. instead of returning plain html into the home() function of the python script,
# you can render the template:
# Line A: add render_template as a class that is to be imported within flask module

# and now, within home(),
# Line B: return render_template() and pass in the template you want to render (i.e. 'home.html')

# now, save the script and run it from Terminal to see if this works.

# you can see that it looks about the same as it did before.
# but if you right click and View Page Source,
# then you see your entire HTML structure here instead of the <h1>Home Page</h1> of before.
# i.e. it is pulling that structure from the home.html template on line B.

# Line C: same procedure was done on the About Page.

lb(3)
# so, if you were just using flask to serve up static HTML pages, then that's basically what you created so far.
# all you'd have to do is just add in more HTML and CSS, and you'll be good to go.

# but pretty much every web application these days doesn't just contain static information.
# it usually has blog posts, updates and all kind of information that is being added to the site on a regular basis.

# let's say that you had a blog post that you wanted to display with your template.
# Line D: first, add some dummy blog posts.
# (in this case, a couple of dictionaries within a list, with each dictionary representing a single blog post)
'''
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
'''
# for now, let's pretend that you made a database call, and got back this list of posts.
# you can pass these posts into your template, just by passing an argument with your data.

# Line E: within your render_template() of home() function, pass in a second argument (posts=posts)
# now, whatever variable name you use as the argument name here that you pass in,
# you will have access to that variable within your template (i.e. home.html)
# and it will be equal to this posts data.

lb(4)
# so now let's switch over to your home.html template to see how you'd loop through this data.
# n.b. the templating engine that flask uses is called jinja2,
# and it allows you to write code here within your template.

# to write a for loop, open up a code block.
# and a code block {% %} is represented by curly braces {} and percentage % signs at each end of the braces.

# within these, you can say 'for post in posts',
# and you also have to tell the templating engine when the for loop ends.
# and you just do that with another code block {% %}, and say 'endfor' within:
'''
<body>
    {% for post in posts %}
    {% endfor %}
</body>
'''

# now within this for loop, you can print out your post information one post at a time.
# e.g. you wanted to print out the post.title in an <h1> tag
#(noting that you can use the .access within the template)

# and you want to print out a variable; this isn't going to be represented the same as the codeblock
# variables are represented by two curly braces. {{ }}:
'''
<body>
    {% for post in posts %}
        {{ post.title }}
    {% endfor %}
</body>
'''

# now, print out the paragraph tag <p> </p> and print out the post.author & post.date_posted:
'''
<body>
    {% for post in posts %}
        <h1>{{ post.title }}<h1>
        <p1>By {{ post.author }} on {{ post.date_posted }}</p>
    {% endfor %}
</body>
'''

# and lastly, print out the actual post.content:
'''
<body>
    {% for post in posts %}
        <h1>{{ post.title }}<h1>
        <p>By {{ post.author }} on {{ post.date_posted }}</p>
        <p>{{ post.content }}</p>
    {% endfor %}
</body>
'''

# # # # # # # # # # # # # # # # continue onto flaskblog4.py # # # # # # # # # # # # # # # #
