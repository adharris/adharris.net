---
title: Introduction and Setup
published: true
layout: post
short_title: Introduction and Setup
series_id: bakery
series_index: 1
---

[Bakery][bakery_project] is a Drupal module which provides single sign on to
Drupal sites which are running on the same domain.  This means that a user who
logs in on one Drupal site is transparently logged in to other Drupal sites on
the same domain, and when they log out they are logged out everywhere.![](/models/posts/ballmer.png)

![](/models/posts/ballmer.png)

Bakery performs this magic through the use of a shared domain cookie.  That is,
a cookie that is set with a [leading dot on the domain][wiki-leading-dot], which
is accessible to every subdomain.  So if a cookie is set with a domain of
`.example.com`, it will be accessible to `example.com`, `www.example.com`,
`subdomain.example.com`, etc.

The cookie shares the authenticatd user's username, email address, and a url at
which the the user can edit their username and password.  This cookie is, of
course, encrypted with a shared secret key shared between all sites.

Bakery [does provide some documentation about using it non-Drupal platforms][bakery-non-drupal],
but it is understandably pretty sparse.  This series of posts will how to setup
a basic [Flask][flask] application that that uses a Drupal site for it's user
authentication.

### Setup

We'll need to setup a Drupal site and a Flask application using the same root
domain name.  Since you cant set cookies on `localhost`, I'll set up Drupal on
`drupal.local`, and my Flask application will live at `flask.drupal.local`.

It's a bit out of scope for this post to describe the steps of setting these
sites up.  I'm using nginx and php-fpm to serve Drupal, [As outlined here][nginx-drupal].
Flask is served using the built in server for development and gunicorn for
production, and using nginx to proxy the requests [like this][nginx-flask].
It is also possible to [serve flask applications through Apache][apache-flask],
if that is more to your liking.

#### Drupal

First, lets get bakery setup.  Install Drupal, add the [Bakery Module][bakery_project],
and enable it.  We can then configure bakery at admin/config/system/bakery.

The first thing to do is designate this site as the 'master' site.  This means
that this Drupal site will be the central authority on users and authentication.
Any other site will be a "slave", meaning that it will use the master site for
authentication.  There can only be one master site, in our case `drupal.local`

![Setting the master site][config-master]

For now, we can skip the "Slave Sites" textarea (we will come back to that in a
later step), and we can accept the default for the "Help Text".

The next section controlls the cookies.  First, to avoid problems, we should set
the cookie age to whatever your php `session.cookie_lifetime` is set to.  The
default Drupal settings file sets this to `2000000` seconds, or a little over 23
days.

Now, enter a long and secret key that will be used to encrypt and sign the
shared cookies.  This key will be shared between all your sites, and needs to
be kept secret.  If it becomes known, an attacker will be able to authenticate
as any user!

The last setting here is cookie domain, which is where bakery will set the 
shared cookie.  It should be the root domain of your site, prefixed with a 
single dot.  In our case `.drupal.local`

![Cookie Settings][config-cookie]

Lastly, we can pick which profile fields will be shared in the cookie.  Be sure
that username and email are checked.  Any other fields you want to share are
up to you.

![Profile fields][config-fields]

Save these settings, and then log out of Drupal and back in.  If you insepct
your cookies now, you should see a cookie named `CHOCOLATECHIP` and set on 
`.drupal.local`.  It should contain a base 64 string.  We'll deal with this
cookie later.

#### Flask

The Flask application will be little more than a very basic skeleton at this
point.

{% highlight 'python' %}
from flask import Flask

app = Flask(__name__)

@route('/')
def home()
  return "Home page"
  
if __name__ == "__main__":
  app.run(debug=True)
{% endhighlight %}

That's all we need for right now.  We'll add more in the next step.

[bakery_project]:https://drupal.org/project/bakery
[bakery-non-drupal]:https://drupal.org/node/1213034

[flask]:http://flask.pocoo.org/

[nginx-drupal]:https://github.com/perusio/drupal-with-nginx
[nginx-flask]:http://flask.pocoo.org/mailinglist/archive/2010/12/15/virtually-hosting-flask-apps-with-nginx/#36b73fed96029a0fef05559955ea9485
[apache-flask]:http://flask.pocoo.org/docs/deploying/wsgi-standalone/#deploying-proxy-setups

[wiki-leading-dot]:http://en.wikipedia.org/wiki/HTTP_cookie#Domain_and_Path

[config-master]:{{url_for('static', filename='img/bakery/master.png')}}
[config-cookie]:{{url_for('static', filename='img/bakery/config-cookie.png')}}
[config-fields]:{{url_for('static', filename='img/bakery/config-fields.png')}}