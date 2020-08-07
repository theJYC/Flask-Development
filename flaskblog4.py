def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the fourth note on building a python flask application *
~lb(0): if/else conditional statements on flask
~lb(1): passing in a title for flask pages
~lb(2): keeping flask dev. DRY
~lb(3): template inheritance
~lb(4): inheritance in action

'''
#____________from previous flask notes (+ modification)____________

from flask import Flask, render_template
app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)

#_________________________end of app code_________________________

lb(0)
# you saw how to do a for loop in flaskblog3.py;
# let's see how you can do if/else conditional statements aswell.

# e.g. let's say you wanted to pass a title to your webpage.
# but if you didn't pass a title, you'd just want to use the default Jin Young's Blog, or something like that.

# within the home.html template,
# come up to where it says <title></title>, and insert Jin Young's Blog in between the title tags.
# and now let's actually add in an if/else conditional here,
# whereby if you actually passed in a title into this template, it would print out 'Jin Young's Blog — title'

# to do an if statement, start with the code block {% %} you saw when you created a for loop,
# and type 'if title' in between.
# and encapsulate the desired <title>{{ title }} — Jin Young's Blog</title> (noting the title variable here!)
# then put in another code block below with 'else' within,
# now, encapsulate the default <title>Jin Young's Blog</title> line you began with within the else block,
# and below that, another code block with 'end if' to end the if statement:
'''
<head>
    {% if title %}
        <title>{{ title }} — Jin Young's Blog</title>
    {% else %}
        <title>Jin Young's Blog</title>
    {% endif %}
</head>
'''

# also copy this title structure onto the About Page aswell (in the 'about.html' template)!

lb(1)
# if you go back up to your application code,
# let's decide not to pass in a title to the home page,
# because you just want that to be the default for your application.

# Line A: but for the about template, let's pass in a title of 'About' to render_template().

# so for the homepage, where you didn't pass in a title,
# it should come into home.html and run through {% if title %} and see it doesn't have one,
# and thus will just use <title>Jin Young's Blog</title> of the {% else %}.

# and for the aboutpage, where you did just pass in a title (line A),
# it will use <title>{{ title }} — Jin Young's Blog</title> instead.

# so, when loading the website, localhost:5000, will display the default title of 'Jin Young's Blog',
# whereby the About page, locahost:5000/about, will display the passed in title of 'Jin Young's Blog — About'.

lb(2)
# there is one last thing when it comes to templates that should be avoided because it is not good design.
# if you've noticed, the home.html and about.html templates both have a lot of similar repeated code.
# in fact, the only distinction between the two templates lies in the <body><body> portion.

# now, this is never a good thing in programming because it means that if you want to update one of those sections,
# then you'd need to update it in every single locations.

# e.g. if you wanted to change the default title (Jin Young's Blog) of your website,
# you'd have to make that change to both home.html and about.html templates.

# so it's almost always better to have everything that is repeated in a single place,
# so that there's only one place to make changes,
# and that your home.html and about.html templates only contain the information that is unique both pages.

# to accomplish this, you can use something called template inheritance.

lb(3)
# let's see what this looks like.
# e.g. create a new template 'layout.html' within the templates directory where home/about.html are stored.

# within layout.html, you want to pick out all of the repeated sections between your home.html and about.html
# i.e. copy the entirety of either of the templates,
# and just empty the <body></body> section given that this is the only part that is different between the two:
'''
<!DOCTYPE html>
<html>
<head>
    {% if title %}
        <title>{{ title }} - Jin Young's Blog</title>
    {% else %}
        <title>Jin Young's Blog</title>
    {% endif %}
</head>
<body>

</body>
</html>
'''

# with the above, you only have the html that is shared by both of the routes.

# now, you're going to create a block.
# a block is a section that the child templates can override.

# create block within your <body></body> tag, and call this block 'content'
#(you create a block like you do a code block {% %}, but insert 'block' keyword in there)
#(make sure to put in another {% %} to end the block afterwards with the 'endblock' keyword!):
# i.e.:
'''
<body>
    {% block content %}{% endblock %}
</body>
'''

# now, with everything in place, the layout.html would be:
'''
<!DOCTYPE html>
<html>
<head>
    {% if title %}
        <title>{{ title }} - Jin Young's Blog</title>
    {% else %}
        <title>Jin Young's Blog</title>
    {% endif %}
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
'''

lb(4)
# now that you created the parent 'layout' template,
# you are going to have the two route templates (home/about.html) inherit it and get all of this info-
# and then you'll just override the content section with the information that is unique to each page.

# first, switch over to the home.html template,
# and in this template, you want to use 'layout.html' template as the parent,
# so you can get rid of all the information that is repeated in both the layout and home templates,
# i.e. everything that is outside of the <body></body> tags of home.html:
'''
{% for post in posts %}
        <h1>{{ post.title }}<h1>
        <p>By {{ post.author }} on {{ post.date_posted }}</p>
        <p>{{ post.content }}</p>
    {% endfor %}
'''

# now, on top of this for loop, you can use the layout.html template by opening up a code block {% %}
# and typing in the 'extends' keyword, followed by 'layout.html'.
''' {% extends 'layout.html' %} '''

# lastly, to have the for loop content override the content block of the layout template,
# wrap the for loop in a content block as below:
'''
{% extends 'layout.html' %}
{% block content %}
    {% for post in posts %}
        <h1>{{ post.title }}<h1>
        <p>By {{ post.author }} on {{ post.date_posted }}</p>
        <p>{{ post.content }}</p>
    {% endfor %}
{% endblock %}
'''

# the above way to encapsulate block content would work and this is how most people do it,
# but jinja2 allows you to put the name of the block after the endblock.

# now, naming your block is nice
# because if you have multiple blocks it can be easy to lose track of what block you're closing.
# i.e. it's good to be explicit.
# with this in mind, type in 'content' after endblock, as:
# {% endblock content %}

# resulting in below for home.html:
'''
{% extends 'layout.html' %}
{% block content %}
    {% for post in posts %}
        <h1>{{ post.title }}<h1>
        <p>By {{ post.author }} on {{ post.date_posted }}</p>
        <p>{{ post.content }}</p>
    {% endfor %}
{% endblock content %}
'''

# and finally repeat the same inheritance for about.html,
# making sure to tailour the block content with the <h1>About Page</h1>:
'''
{% extends 'layout.html' %}
{% block content %}
    <h1>About Page</h1>
{% endblock content %}
'''

# now, after saving the three templates and running the website again:
# you can see the two routes ('/home' and '/about') still work the same as before
# whereby, behind the scenes, there is no repeated code like before.

# # # # # # # # # # # # # # # # continue onto flaskblog5.py # # # # # # # # # # # # # # # #
