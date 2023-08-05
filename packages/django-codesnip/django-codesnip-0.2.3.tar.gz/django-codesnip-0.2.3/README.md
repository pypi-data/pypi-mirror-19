Codesnip
========

Codesnip is a Django app to store code snippets with syntax highlighting.
**This app requires [pygments](http://pygments.org/).**

Detailed documentation is in the "docs" directory.

Quick start
-----------

1.  Add "shortcodes" to your INSTALLED\_APPS setting like this:
    ```python
    INSTALLED_APPS = [
        ...
        'codesnip',
    ]
    ```

2.  Run `python manage.py migrate` to create the Snippet model.

3.  Start the development server and visit http://127.0.0.1:8000/admin/ to
    create a code snippet (you'll need the Admin app enabled).
