Wishlist
========

Python library to grab your Amazon wishlist so you can mess with it
programmatically.

Dependencies
------------

Before you can use this you have to have a few things installed, on
Ubuntu, you can run these commands:

::

    $ sudo su
    $ apt-get install --no-install-recommends xvfb

And you need to install Chrome:

::

    $ apt-get install --no-install-recommends libxss1 libappindicator1 libindicator7 
    $ apt-get install --no-install-recommends gconf-service libasound2 libnspr4 libnss3
    $ apt-get install --no-install-recommends libpango1.0-0 xdg-utils fonts-liberation
    $ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    $ dpkg -i google-chrome*.deb
    $ apt-get install unzip
    $ LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
    $ wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip
    $ unzip chromedriver_linux64.zip && ln -s $PWD/chromedriver /usr/local/bin/chromedriver

1 minute gettings started
-------------------------

Is your wishlist private? Then you will need to authenticate on the
command line:

::

    $ wishlist auth

This will prompt you to signin and will even handle 2-factor
authentication, after you signin your cookies will be saved so you can
run now access your Amazon wishlist.

You can check access to your wishlist on the command line by running:

::

    $ wishlist dump NAME

where ``NAME`` is the part of a url like
``https://www.amazon.com/gp/registry/wishlist/NAME``, so, if your
wishlist was found at:
``https://www.amazon.com/gp/registry/wishlist/9YDNFG31NSSRL`` then you
would run:

::

    $ wishlist dump 9YDNFG31NSSRL

If you wanted to do something in another python script, you can do:

.. code:: python

    from __future__ import print_function
    from wishlist.core import Wishlist

    name = "9YDNFG31NSSRL"
    w = Wishlist()
    for item in w.get(name):
        print(w.jsonable())

You can check the ``wishlist.core.WishlistElement`` code to understand
the structure of each wishlist item.

Installation
------------

use pip:

::

    $ pip install wishlist

Or be bleeding edge:

::

    $ pip install "git+https://github.com/Jaymon/wishlist#egg=wishlist"

Other things
------------

-  This only works on **amazon.com**, because I only use **amazon.com**,
   if you want it to use a different Amazon site, I take pull requests
   :)

-  Would you rather use php? `There's a library for
   that <https://github.com/doitlikejustin/amazon-wish-lister>`__ (`also
   related <https://shkspr.mobi/blog/2015/11/an-api-for-amazon-wishlists/>`__).

-  `Amazon's advertising
   api <http://docs.aws.amazon.com/AWSECommerceService/latest/DG/Welcome.html>`__,
   this is where the officially supported wishlist api used to live.


