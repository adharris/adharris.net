---
title: Authenticating in Flask
published: false
layout: post

short_title: Authentitication in Flask
series_id: bakery
series_index: 2
---

In this part, we will set up our very basic Flask application to read and
decrypt the bakery cookie, and then use the data to authenticate the user.  If
you dont have Bakery set up yet, then [check out part 1][part-1].

### Users

The first thing we need to do is setup user accounts for our Flask application.
We can make this very simple by using [Flask-Login][flask-login] for login and
[Flask-SQLAlchemy][flask-sqla] for persitance.  Check out those extensions for
examples.  Here's my Flask app with my user model:

{% highlight 'python' %}
{{ gist("6515993", version='7cf' ) }}
{% endhighlight %}

[part-1]:{{ model.previous_post().url }}

[flask-login]:http://flask-login.readthedocs.org/en/latest/