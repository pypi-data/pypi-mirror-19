=====
Usage
=====

To use django-price-level in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_price_level.apps.DjangoPriceLevelConfig',
        ...
    )

Add django-price-level's URL patterns:

.. code-block:: python

    from django_price_level import urls as django_price_level_urls


    urlpatterns = [
        ...
        url(r'^', include(django_price_level_urls)),
        ...
    ]
