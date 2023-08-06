.. image:: https://gitlab.com/mayan-edms/cabinets/raw/master/contrib/art/logo.png

Description
-----------
Mayan EDMS app that stores documents in a multi level hierarchy.

License
-------
This project is open sourced under the Apache 2.0

Installation
------------
Activate the virtualenv where you installed Mayan EDMS.
Install from PyPI::

    pip install mayan-cabinets

In your settings/local.py file add `cabinets` to your `INSTALLED_APPS` list::

    INSTALLED_APPS += (
        'cabinets',
    )

Run the migrations for the app::

    mayan-edms.py migrate


Add the media files from the app::

    mayan-edms.py collectstatic


Development
-----------
Clone repository in a directory outside of Mayan EDMS::

    git clone https://gitlab.com/mayan-edms/mayayn-cabinets.git

Symlink the app into your Mayan EDMS' app folder::

    ln -s <repository directory>/cabinets/ <Mayan EDMS directory>/mayan/apps

In your settings/local.py file add `cabinets` to your `INSTALLED_APPS` list::

    INSTALLED_APPS += (
        'cabinets',
    )

Run the migrations for the app::

    ./manage.py migrate



1.1.0 (2017-02-07)
==================

- Fix cabinet list API endpoint.
- Improve cabinet document API endpoints.
- Add more API tests.

1.0.0 (2017-01-25)
==================

- Initial release.


