GazelleAPI is a handy interface for interacting with gazelle based
trackers. This should work on Python 2 and 3.

It is based on `whatapi <https://github.com/isaaczafuta/whatapi>`_ and `xanaxbetter <https://github.com/rguedes/xanaxbetter>`_.

************
Installation
************

Pip
---

.. code:: bash

    pip install gazelleapi

Source
------
.. code:: bash

    git clone https://github.com/itismadness/gazelleapi
    cd gazelleapi
    python setup.py install

*****
Usage
*****

.. code:: bash

    >>> from gazelleapi import GazelleAPI
    >>> api = GazelleAPI(username='user', password='pass', hostname='example.com')
    >>> api.request('index')

To avoid having to always login to the site, we suggest using cookies in the following manner:

.. code:: bash

    >>> from gazelleapi import GazelleAPI
    >>> import pickle
    >>> cookies = pickle.load(open('cookies.dat', 'rb'))
    >>> api = GazelleAPI(username='user', password='pass', hostname='example.com', cookies=cookies)

and to save the cookie on an open session:

.. code:: bash
    
    >>> pickle.dump(api.session.cookies, open('cookies.dat', 'wb'))