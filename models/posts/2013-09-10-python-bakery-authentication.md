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
more robust examples.

{% highlight 'python' %}
{{ gist("6515993", lines=[(1, 51), (82, 85)]) }}
{% endhighlight %}

Lets run through the fields on our user model.  Hopefully you can guess what
`username` and `email` are.  `init` will be the url on the master site at which
the user can edit her account.  It's worth noting that the `id` field *will not*
be the Drupal user id.  Bakery does not sync user id by design.

Another thing worth noting is that our user model does not have a password.
Because all authentication occurs on the Drupal side of things, we don't 
actually need a password.


### Decrypting CHOCOLATECHIP

Bakery stores the encrypted user information into a cookie named
`CHOCOLATECHIP`.  We are going to create a view that will read this cookie and
log in the user.

Getting the cookie is the easy part:

{% highlight 'python' %}
from flask import request
@app.route('/login')
def login():
  
  cookie = request.cookie.get('CHOCOLATECHIP')
{% endhighlight %}

We can't actually *do* anything with this cookie yet, we need to decrypt it
first.  Since the same encryption is used for a couple of things, we'll write
a function we can reuse.  You'll need [PyCrypto][pycrypto] for the actual
encryption, and since the data is serialized using PHP serialization, we also
need [phpserialize][phpserialize].

{% highlight 'python' %}
{{ gist("6515993", filename="bakery.py", version='0c2' ) }}
{% endhighlight %}

Let's walk through this.  The first thing we do is get the Bakery encryption
key.  This is the secret key that we configured in Drupal, I put it into my
app config.

The cookie data itself is url encoded, so we use urllib to decode it. (I'm
not sure if the cookie is url encoded in Drupal, by the browser, or by
Werkzueg.  If it is Werkzueg, then your cookie might already be decrypted if
you are not using Flask)

The cookie is also endcoded as a base64 string, so we need to undo that with
`base64.b64decode`.  To prevent tampering, the encrypted data is signed using
HMAC and the secret key.  The firts 64 bytes of the cookie are the HMAC
signature, and the remaining bytes contain the actual data.  We use the secret
key and `hmac` to regenerate the signature.

If the new HMAC token does not match the signature sent with the cookie, then
the cookie has been tampered with and decryption should abort, so we return
`None`.  The user will have to reauthenticate and get a clean cookie.  You might
want to log this event, as it could mean someone is trying to spoof a user.

Now we can actually decrypt the data.  Bakery uses AES-128 in ECB mode.  AES-128
requires key lengths of 16, 24, or 32 bytes.  PHP's implementation takes care of
padding the key to the appropriate length, but PyCrypto does not.  PHP uses a 
null byte for padding, so we pad our secret key with `\0` using `ljust` to the
nearest appropriate key length.

Lastly, we decrypt and use `phpserialize` to turn the serialized string into a
python dictionary.

### Creating a user

Let's check out the contents of the decrypted cookie.  Here's what mine looks
like:

{% highlight 'python' %}
{
  'name': 'admin',
  'timestamp': 1380497573,
  'calories': 480,
  'init': 'drupal.local/user/1/edit',
  'master': 1,
  'mail': 'sys@drupal.local',
  'type': 'CHOCOLATECHIP',
}
{% endhighlight %}

* **name:** The user's Drupal username
* **timestamp:** The time that the cookie was created.
* **calories:** Unused.  I believe it's a joke.
* **init:** The url at which the user can edit their account
* **master:** A bit indicating if the cookie was created on the master site.
* **mail:** The user's email address
* **type:** The type of the cookie

Now in our login view, we can use this information to lookup the user in the
database, creating them if need be.

{% highlight 'python' %}
{{ gist("6515993", filename="app.py", version='e06', lines=[(53, 79)]) }}
{% endhighlight %}

Now, if you login on your Drupal site, and then visit the `/login` page on your
Flask app, you should be redirected and logged in.

This works if you can guarentee that the user is logged in on Drupal first, but
what if there is no authentication cookie when the user visits your app?  We
will deal with that in the next step.

[part-1]:{{ model.previous_post().url }}
[flask-login]:http://flask-login.readthedocs.org/en/latest

[pycrypto]:https://pypi.python.org/pypi/pycrypto
[phpserialize]:https://pypi.python.org/pypi/phpserialize