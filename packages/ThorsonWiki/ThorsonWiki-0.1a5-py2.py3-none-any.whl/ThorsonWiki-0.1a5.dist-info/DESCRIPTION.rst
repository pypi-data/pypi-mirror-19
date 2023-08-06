============
Thorson Wiki
============

Thorson Wiki is a simple Django wiki framework. It allows developers to create
one or more wikis quickly and easily. The framework is designed to be both
extensible and easy to work with---it provides basic functionality for simple
cases, and an advanced API for more complex cases. 

------------
Installation
------------

The easiest way to install Thorson Wiki is with either :code:`pip` or
:code:`easy_install`. 

1. Install the package:

   pip install thorson_wiki

2. Add :code:`thorson_wiki` to :code:`INSTALLED_APPS` in your Django
   settings.

3. Run :code:`manage.py migrate` to synchronize your database.

---------------
Creating a Wiki
---------------

To create a wiki, you must first tell Thorson Wiki some information about the
wikis that you want to create. This is done using the
:code:`THORSONWIKI_NAMESPACES` setting. This setting is a dictionary mapping
namespace names to information about that namespace. An example is given below,
containing only the required settings.

::

    THORSONWIKI_NAMESPACES = {
        'mywiki': {
            'title': "My Wiki",
            'description': "A wiki designed by me, for me.",
            'author': "Jacob Collard",
            'landing': "Home Page",
        }
    }

The :code:`title` attribute provides a human-readable title for your wiki
namespace. This appears in most of the templates in the nav bar. The
description appears in the description :code:`<meta>` tag in the template HTML.
Likewise, the :code:`author` appears in the author :code:`<meta>` tag.
:code:`landing` is the name of the Wiki's landing page. 

If you are using the default templates, it is also recommended that you add the
following settings:

::

    THORSONWIKI_DEFAULT_NAMESPACE = 'mywiki'

    LOGIN_URL = reverse_lazy(THORSONWIKI_DEFAULT_NAMESPACE + 'login')
    LOGIN_REDIRECT_URL = reverse_lazy(THORSONWIKI_DEFAULT_NAMESPACE + ':main')

The next thing you need to do is tell your project the URLs for your wiki.
Simple import :code:`include_wiki` from :code:`thorson_wiki.urls` and add the
following to your urlpatterns:

::

    url(r'^my_base_url/', include_wiki('mywiki'))

This will automatically generate URLs beginning with :code:`my_base_url` that
relate to the wiki :code:`mywiki`. Simply navigate to :code:`my_base_url`, and
you will find your wiki is in operation. Note that if you haven't yet created
the landing page, you will be prompted to do so when you visit the wiki.


