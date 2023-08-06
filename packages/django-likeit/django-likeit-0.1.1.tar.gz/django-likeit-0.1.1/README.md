<h1> django-likeit</h1>
A simple app for Django that enables users to like and unlike any object/item within any model.
It's developed on Python 3.5 & Python 3.6 for Django 1.10 and later.

<h2> Installation </h2>


* Install django-likeit in your vilrtual env:

<pre>
pip install django-likeit
</pre>

* Add the app to your settings.py

<pre>
INSTALLED_APPS = [
  ...
  "like",
  ...
]
</pre>

* Add likeit urls to your project's <pre>urls.py</pre> file:

<pre>
from django.conf.urls import url, include

urlpatterns = [
  ...
  url(r'^like/', include('like.urls')),
  ...
]
</pre>

* Migrations:

<pre>
python manage.py makemigrations like
python manage.py migrate
</pre>

* Make sure you have jQuery ajax CSRF configuration right, and also you included Font Awesome in your HTML.

<h2> Usage:</h2>


<h3> Template tags: </h3>

* Get the liked objects for a given user:

<pre>
{% with user_likes <user> "app_label.model" as like_list %}
    {% for like_obj in like_list %}
        {# do something with like_obj #}
    {% endfor %}
{% endwith %}
</pre>


* Given an object <pre>obj</pre> you may show it like count like this:

<pre>
<p>Like Count {{ obj|likes_count }}</p>
</pre>


* Get Like instance for an object (obj) and a user (user)

<pre>
{% with obj|get_like_for:user as like_object %}
    ...
{% endwith %}
</pre>

* Like Button for an object <pre>my_obj</pre>:

<pre>
{% like_button my_obj %}
</pre>


<h3> Likes Manager </h3>

* Create a Like instance for a user and object:

<pre>
>>> from django.contrib.auth.models import User
>>> from music.models import Song
>>> user = User.objects.get(username='jdoe')
>>> song = Song.objects.get(pk=1)
>>> like = Like.objects.create(user, song)
</pre>

    or:

<pre>
>>> like = Like.objects.create(user, 1, Song)
</pre>

    or:

<pre>
>>> like = Like.objects.create(user, 1, "music.Song")
</pre>

 * Get the objects liked by a given user:

<pre>
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='jdoe')
>>> Like.objects.for_user(user)
>>> [<Like: Like object 1>, <Like: Like object 2>, <Like: Like object 3>]
</pre>

* Now, get user liked objects belonging to a given model:

<pre>
>>> from django.contrib.auth.models import User
>>> from music.models import Song
>>> user = User.objects.get(username='jdoe')
>>> Like.objects.for_user(user, model=Song)
>>> [<Like: Like object 1>, <Like: Like object 2>, <Like: Like object 3>]
</pre>

* Get the liked object instances of a given model liked by any user:

<pre>
>>> from music.models import Song
>>> Like.objects.for_model(Song)
>>> [<Like: Like object 1>, <Like: Like object 2>, <Like: Like object 3>]
</pre>

* Get a Like instance for a given object and user:

<pre>
>>> from django.contrib.auth.models import User
>>> from music.models import Song
>>> user = User.objects.get(username='jdoe')
>>> song = Song.objects.get(pk=1)
>>> like = Like.objects.get_like(user, song)
</pre>

* Get all Like instances for a given object

<pre>
>>> from music.models import Song
>>> song = Song.objects.get(pk=1)
>>> like = Like.objects.for_object(song)
</pre>