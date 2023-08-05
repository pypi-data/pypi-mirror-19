Django-Box
==========


Django-Box is a new way for fragmenting template in Django, Django-Box will load a template fragment that called in
used template or base template. It provides a 'box' django inclusion tag, where every box can has its own separate function.
The main view doesn't have to provide data for every fragment, the data will be populate in its own function (fragmenting)

Installing
**********

1. Install using ``pip``::

    pip install django_box

   or via ``github``::

    pip install -r git+https://github.com/hqms/django-box.git


2. In your settings add  the following:

   .. code-block:: python

       INSTALLED_APPS = (
           ...
           'django_box',
           ...
       )

       BOX_MODULE_PATH   = 'frontend'

       BOX_TEMPLATE_PATH = 'box'

3. Create python package for your box controller same as **BOX_MODULE_PATH**

4. Create template directory same as **BOX_TEMPLATE_PATH**


Usage
*****

1. Add box template tag in template (whether it is in regular template or base template)

   .. code-block:: html+django

     <h1>This is box fragment</h1>
     <p>{% box 'fragment1' %}</p>

2. Create a **fragment1.py** in **BOX_MODULE_PATH** location, and create a class with same name of that fragment with Box class as it parent

   .. code-block:: python

     from django_box import Box

     class fragment1(Box):
         template_name = 'fragment1.html'

3. Create a file in **BOX_TEMPLATE_PATH** within template directory with name same as template_name


