=====
Django Markdown Blog
=====

Django Markdown Blog is a simple Django app that will give any Django project a blog that works with markdown.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'polls',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^blog/', include('markdown_blog.urls')),

3. Run `python manage.py migrate` to create the blog models.

4. Start the development server and visit http://localhost:8000/admin/
   to create your first blog post (you'll need the Admin app enabled).

5. Visit http://localhost:8000/polls/ to view your latest blog posts.
