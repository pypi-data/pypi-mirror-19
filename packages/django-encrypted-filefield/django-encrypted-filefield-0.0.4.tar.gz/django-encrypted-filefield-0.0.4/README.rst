django-encrypted-filefield
==========================

Encrypt uploaded files, store them wherever you like and stream them back
unencrypted.


Why This Exists
---------------

It's increasingly common to use products like S3 to host static files, but
sometimes those static files aren't exactly meant for public eyes.  You might
push some bit of personal client information into S3 and then anyone with the
URL will be able to see it.

Sure, the URL may be really hard to guess, but I'm not a fan of "security
through obscurity" so I wrote this to encrypt stuff I push to S3.  Now, only
encrypted blobs are available publicly, but internally, behind a
``MyPermissionRequiredMixin``, the images and documents are loaded magically
and transparently.


How's It Work?
--------------

``EncryptedFileField`` is a thin wrapper around Django's native ``FileField``
that transparently encrypts whatever the user has uploaded and passes off the
now encrypted data to whatever storage engine you've specified.  It also
overrides the ``.url`` value to return a reference to your own view, which does
the decryption for you on the way back to the user.

So where you may have once had this:

.. code:: python

    # my_app/models.py

    class MyModel(models.Model):

        name = models.CharField(max_length=128)
        attachment = models.FileField(upload_to="attachments")
        image = models.ImageField(
            upload_to="images",
            width_field="image_width",
            height_field="image_height"
        )
        image_width = models.PositiveIntegerField()
        image_height = models.PositiveIntegerField()

All you have to do is change the file fields and you've got encrypted files

.. code:: python

    # settings.py

    DEFF_SALT = b"The secret key.  This should be long."
    DEFF_PASSWORD = b"The password.  This should be long too."
    DEFF_FETCH_URL_NAME = "whatever-url-name-you-want"


    # my_app/models.py

    from django_encrypted_filefield.fields import (
        EncryptedFileField,
        EncryptedImageField
    )

    class MyModel(models.Model):

        name = models.CharField(max_length=128)
        attachment = EncryptedFileField(upload_to="attachments")
        image = EncryptedImageField(
            upload_to="images",
            width_field="image_width",
            height_field="image_height"
        )
        image_width = models.PositiveIntegerField()
        image_height = models.PositiveIntegerField()


    # my_app/views.py

    from django.contrib.auth.mixins import AuthMixin
    from django_encrypted_filefield.views import FetchView


    class MyPermissionRequiredMixin(AuthMixin)
        """
        Your own rules live here
        """
        pass


    class MyFetchView(MyPermissionRequiredMixin, FetchView):
        pass


    # my_app/urls.py

    from .views import MyFetchView

    urlpatterns = [
        # ...
        url(
            r"^my-fetch-url/(?P<path>.+)",  # up to you, but path is required
            MyFetchView.as_view(),          # your view, your permissions
            name=settings.DEFF_FETCH_URL_NAME
        ),
        # ...
    ]


Is There a Demo?
----------------

There is!  Just check out the code and run the mini django app in the ``demo``
directory:

.. code:: bash

    $ git clone git@github.com:danielquinn/django-encrypted-filefield.git
    $ cd django-encrypted-filefield/demo
    $ ./manage migrate
    $ ./manage.py runserver

...then open http://localhost:8000 and submit two files via the form.  In this
case we're using Django's default_storage, but the same logic should apply to
all storage engines.

You can also run the tests from there:

.. code:: bash

    $ ./manage.py test


What's the Status of the Project?
---------------------------------

Alpha.  I'm actively developing this, so if you find a bug, please let me know.
If you use it yourself, great!  But if it breaks, you've been warned.
