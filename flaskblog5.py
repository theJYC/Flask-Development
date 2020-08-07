def line_break(x):
    print(str(x) + '---------' + str(x) + '---------' +
          str(x) + '---------' + str(x) + '---------')


lb = line_break

'''
~appendix
* this is the fifth note on building a python flask application *
~lb(0): demo. of the power of inheritance pt.1
~lb(1): demo. of the power of inheritance pt.2
~lb(2): recap of template inheritance
~lb(3): giving the flask app some ~style~
~lb(4): CSS file in flask development
~lb(5): further customisation of layout.html
'''
#____________from previous flask notes (+ modification)____________

from flask import Flask, render_template, url_for  # refer to line A
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
# let's see why inheritance is so powerful.
# say that you wanted to now update the entire website to use Bootstrap.

# Bootstrap is an extremely popular library that makes it easy to add some nice styles to your website.
# n.b. you'll be using Bootstrap in this series because it'll allow you to use nice styles,
# without taking away the focus from flask development itself.

# to add Boostrap to your website,
# open up the stater template from the official Bootstrap documentation
#(URL: https://getbootstrap.com/docs/4.3/getting-started/introduction/)
# you will have to make changes to your templates so that this template is included in them all:
'''
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <h1>Hello, world!</h1>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  </body>
</html>
'''

# if you were not using template inheritance,
# you'd have to make these changes to every template in your flask application.
# and not to mention how easy it would be to make a mistake when doing that,
# it would be almost impossible to maintain once the number of pages of your website grew to a certain level.

# but now, with the newfound knowledge of template inheritance,
# you can make these changes to that single 'layout.html' template that your other templates inherit from.

lb(1)
# now, to do this, copy the <!-- Required meta tags --> and the <!-- Bootstrap CSS -->,
# and add it to the <head></head> of the layout.html.
# then, grab the <!-- Optional JavaScript -->
# and paste that above the closing <body></body> tag of layout.html.

# and finally, use a Bootstrap specific class (container) to see if it works.
# wrap your {% block content %}{% endblock %} in a <div></div> with a class of container
# which will give content some good padding and spacing.
'''
    <div class='container'>
        {% block content %}{% endblock %}
    </div>
'''

# simply adding in the JavaScript and CSS should be enough for your application to now be using Bootstrap.
# save everything and do a hard refresh on your website with command + shift + r
#(hard refresh will also clear the cache).

# you can see that when you reloaded localhost:5000/home, the text changed and the margins are also different.
# likewise, the localhost:5000/about displays these change too.

# it works on both of those pages because both templates are inheriting from the single 'layout.html' template.

lb(2)
# now, this was all a lot to take in,
# so here is the recap of what you just did re: template inheritance:

# 1: you created a new template called 'layout.html', which became your parent template.
# this has the main structure of your HTML, which is going to be included on every page.
# now, you can have multiple blocks but, right now, the single block called {% block content %}
# is what the other templates are going to override.
# and when they override the content block with data, it'll place that data in this location in the HTML.

# 2: in the home.html and about.html templates, you can see that you are extending the layout.html template,
# and you are specifying that you want to put some information into your content block.
# and that information is the dummy post data that you've seen before.

# 3: so, when it's all said and done, if you go to the home page in the browser and 'View Page Source',
# you can see that you have all of the information from the layout template,
# and then your two dummy blog posts are there in the container div where your content block was located

lb(3)
# now that you have a base layout in place,
# let's add a navigation bar and some global styles to your website so that it looks a little nicer.
# n.b. this is a good bit of HTML so grab it from the code snippets in the description of this YT video.

# e.g. copy the entirety of navigation.html and go back to the layout.html file.
# and paste all of navigation.html right below the opening of the <body></body> tags,
# so what you just added here is a navigation bar with some bootstrap classes that will make this look nice.
# also the navigation bar is responsive so that if you're on a smaller screen, it will resize automatically.

# now also create a new main section that contains your content block,
# copy the entirety of main.html and, in 'layout.html',
# replace the current <div class='container'></div> with main.html .

lb(4)
# there are also some custom styles that are not Bootstrap specific that are going to be main.css
# since this will be a CSS file in your actual project, you'll need to put it somewhere.

# now in flask, static files like CSS and javascript need to be located in a 'static' directory:
# create a new directory called 'static' (all lowercase) within Flask_Blog.
# and within your 'static' directory, create a 'main.css' file.

# now, within the 'main.css', copy and paste in the snippet from main.css in the Corey Schafer GitHub.
# once that is done, you want to include main.css into the layout.html template.
# and you're going to need to use a new flask function called 'url_for'

#'url_for' is a function that will find the exact location of routes for you,
# so you don't need to worry about it in the background.

# Line A: so let's go ahead and import 'url_for' from flask
# and now, return to layout.html and go to the <head></head> section of your website,
# you're going to want to add this style below the <!-- Bootstrap CSS --> style:

# grab the opening part of the Bootstrap style,
# and type in <link rel="stylesheet" type="text/css" href="">,
# whereby the quotations after 'href=' is to indicate where the CSS file is located.

# this is where you are going to use the 'url_for' function.
# open up some double curly braces and say href="{{ url_for('static', filename='main.css') }}".

# so now the stylesheet at the top of your layout is linking to this main.css file within the static folder
# and now the 'url_for()' function will take care of finding that exact location for you.

# now, it's a good idea to use url_for() for just about as many links as you can in your site,
# so it'd also be good for you to use this in your navigation aswell.
# but your navigation bar currently has two routes that you haven't created yet,
# so you'll be creating those in flaskblog6.py
# i.e. you'll actually change those navigation links once those actually exist.

# at this point you should be pretty close to being done,
# save everything and load the webpage again to view the new style and the navigation bar on your website.

lb(5)
# there are only a few more touches that you'd like to add.
# it'd be nice to visually split up the Blog Post 1 and Blog Post 2,
# and the main.css file that you already added has some styles for that-
# you'd just need to put in the correct HTML.

# so within the snippets folder of Corey Schafer's GitHub,
# grab the entirety of article.html (this file is just some updated code for how your posts are displayed)
# and put this within your loop for your blog post which is currently on your homepage.

# go ahead and open up your home.html template,
# and replace <h1> ... </p> with your new code from article.html,
# by which the below will be your updated home.html template:
'''
{% extends 'layout.html' %}
{% block content %}
    {% for post in posts %}
        <article class="media content-section">
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="#">{{ post.author }}</a>
              <small class="text-muted">{{ post.date_posted }}</small>
            </div>
            <h2><a class="article-title" href="#">{{ post.title }}</a></h2>
            <p class="article-content">{{ post.content }}</p>
          </div>
        </article>
    {% endfor %}
{% endblock content %}
'''
# now you can see that the Blog Posts are looking nice and split up a little bit better than before.

# # # # # # # # # # # # # # # # continue onto flaskblog6.py # # # # # # # # # # # # # # # #
