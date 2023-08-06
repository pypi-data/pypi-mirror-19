=====
Django Markdown Blog
=====

Django Markdown Blog is a simple Django app that will give any Django project a blog that works with markdown.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "django_markdown" and "blog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_markdown',
        'blog'
    ]

2. Include the blog URLconf and django_markdown URLconf in your project urls.py like this::

    url(r'^markdown/', include( 'django_markdown.urls')),
    url(r'^blog/', include('blog.urls', namespace='blog')),

3. Run `python manage.py migrate` to create the blog models.

4. Start the development server and visit http://localhost:8000/admin/
   to create your first blog post (you'll need the Admin app enabled).

5. Visit http://localhost:8000/blog/ to view your latest blog posts.


