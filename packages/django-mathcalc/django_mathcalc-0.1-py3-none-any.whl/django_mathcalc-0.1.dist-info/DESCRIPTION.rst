========
Mathcalc
========

Mathcalc is a simple app created for the class requirement.
Detailed documentation (if any!) is with in the source files as comments.

(I'd suggested to go through the source, since that would be an easier task than to
figure out manually)

Quick start
-----------

1. Add "shopcart" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = [
        ...
        'mathcalc',
   ]

2. Include the shopcart urlconf in your project urls.py like this::

   urlpatterns = [
        ...
        url(r'^mathcalc/', include('mathcalc.urls')),
   ]

3. Start the development server and visit http://127.0.0.1:8000/mathcalc/ to view the
   mathcalc app



