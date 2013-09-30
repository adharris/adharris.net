from flask import Flask, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
from flask.ext.static import Static

import datetime

from github import Github

SQLALCHEMY_DATABASE_URI = "postgres:///adharris"

# App Setup
app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy()
static = Static(app, db)

assets = Environment(app)
css = Bundle('css/main.scss', filters='scss', output='css/main.css')
assets.register('css', css)

def gist(id, filename=None, version=None, lines=None):
  g = Github()
  gist = g.get_gist(id)

  if version is not None:
    for h in gist.history:
      if h.version[:len(version)] == version:
        gist = h
        break

  f = gist.files[filename or gist.files.keys()[0]]
  if lines:
    content = []
    split = f.content.splitlines()
    for start, stop in lines:
      content.append('\n'.join(split[start - 1:stop]))
    return "\n\n".join(content)

  return f.content

@app.context_processor
def inject_gist():
  return dict(gist=gist)


# Model Definitions
class Series(static.Model):
  tease = db.Column(db.String)


class Post(static.Model):
  __tablename__ = 'posts'

  series_id = db.Column(db.String, db.ForeignKey(Series.model_id))
  series_index = db.Column(db.Integer)
  series = db.relationship(Series, backref=db.backref('posts', order_by="Post.model_id"))

  def next_post(self):
    return Post.query.filter(Post.series_id == self.series_id,
                             Post.series_index > self.series_index)\
                     .order_by(Post.series_index).first()

  def previous_post(self):
    return Post.query.filter(Post.series_id == self.series_id,
                             Post.series_index < self.series_index)\
                     .order_by(Post.series_index.desc()).first()

  @property
  def url(self):
    return url_for('post', id=self.model_id)


# Routes
@app.route('/')
def home():
  posts = Post.query.order_by(Post.date.desc()).all()
  series = Series.query.all()
  return render_template('index.html', posts=posts, series=series)

@app.route('/<id>/')
def post(id):
  post = Post.query.filter(Post.model_id == id).first_or_404()
  return render_template('post.html', post=post)

if __name__ == "__main__":
  app.run(debug=True)
