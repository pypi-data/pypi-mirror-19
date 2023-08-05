pymonzo
=======

|Build status| |Test coverage| |PyPI version| |Python versions|
|License|

An - dare I say it - awesome Python library that smartly wraps
`Monzo <https://monzo.com/>`__ public API and allows you to use it
directly in your Python project.

It creates a layer of abstraction and returns Python objects instead of
just passing the received JSONs. It also deals with authentication and
allows using either an access token or fully authenticate via OAuth 2
that's a PITA to set up but is then automatically refreshed in the
background.

Installation
------------

>From PyPI:

::

    $ pip install pymonzo

Authentication
--------------

Access token
~~~~~~~~~~~~

If you want to just play around then you can simply get the access token
taken from `Monzo API
Playground <https://developers.getmondo.co.uk/api/playground>`__, either
pass it explicitly to ``MonzoAPI()`` class or save it as an environment
variable (``$ export MONZO_ACCESS_TOKEN='...'``) and you're good to go.
Everything works as expected *but* the token is valid only for couple of
hours.

OAuth 2
~~~~~~~

The second authentication option is to go through OAuth 2, which doesn't
sound bad (everyone is using it!) but from my experience is a PITA when
setting up for server side applications. So.

Some technical background: Monzo currently only allows OAuth 2
'authorization code' grant type and automatic token refreshing is only
allowed for 'confidential' clients.

First, you need to create said client
`here <https://developers.getmondo.co.uk/apps/home>`__. Name and logo
don't really matter but you need to set the redirect URL to this repo
(``https://github.com/pawelad/pymonzo``) and set it to be confidential.

Got it? Cool. You now have required 'Client ID' and 'Client secret' and
only need the auth code. You get it by creating a link with your client
ID:

::

    https://auth.getmondo.co.uk/?client_id=$ClientID&response_type=code&redirect_uri=https://github.com/pawelad/pymonzo

You then go to the link and authorise the app. You should get an email
with a link back to the GitHub repo and the authorization code,
something like:

::

    https://github.com/pawelad/pymonzo?code=$AuthCode

You now have all three needed values - client ID, client secret and the
auth code. As with the access token, you can either pass them directly
to ``MonzoAPI()`` class or save them as environment variables:

::

    $ export MONZO_CLIENT_ID='...'
    $ export MONZO_CLIENT_SECRET='...'
    $ export MONZO_AUTH_CODE='...'

That's it! The token is then saved (``~/.pymonzo``) on the disk and is
automatically refreshed when needed via the awesome
`requests-oauthlib <https://github.com/requests/requests-oauthlib>`__ so
all this *should* be one time only.

Roadmap
-------

The library currently does not implement feed items, webhooks and
attachments endpoints - I plan to add them in the future, but they
were't essential to my current needs and they could be completely
different in the future - per
`docs <https://monzo.com/docs/#introduction>`__: > The Monzo API is
under active development. Breaking changes should be expected.

I plan to implement all API functionality as soon as it comes out of
beta and stabilizes.

API
---

There's no documentation as of now, but the code is commented and
*should* be pretty straightforward to use.

But feel free to ask me via
`email <mailto:pawel.adamczak@sidnet.info>`__ or `GitHub
issues <https://github.com/pawelad/pymonzo/issues/new>`__ if anything is
unclear.

Tests
-----

Package was tested with the help of ``py.test`` and ``tox`` on Python
2.7, 3.4, 3.5 and 3.6 (see ``tox.ini``).

Code coverage is available at
`Coveralls <https://coveralls.io/github/pawelad/pymonzo>`__.

To run tests yourself you need to set environment variables with access
token before running ``tox`` inside the repository:

.. code:: shell

    $ pip install -r requirements/dev.txt
    $ export MONZO_ACCESS_TOKEN='...'
    $ tox

Contributions
-------------

Package source code is available at
`GitHub <https://github.com/pawelad/pymonzo>`__.

Feel free to use, ask, fork, star, report bugs, fix them, suggest
enhancements, add functionality and point out any mistakes.

Authors
-------

Developed and maintained by `Paweł
Adamczak <https://github.com/pawelad>`__.

Released under `MIT
License <https://github.com/pawelad/pymonzo/blob/master/LICENSE>`__.

.. |Build status| image:: https://img.shields.io/travis/pawelad/pymonzo.svg
   :target: https://travis-ci.org/pawelad/pymonzo
.. |Test coverage| image:: https://img.shields.io/coveralls/pawelad/pymonzo.svg
   :target: https://coveralls.io/github/pawelad/pymonzo
.. |PyPI version| image:: https://img.shields.io/pypi/v/pymonzo.svg
   :target: https://pypi.python.org/pypi/pymonzo
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/pymonzo.svg
   :target: https://pypi.python.org/pypi/pymonzo
.. |License| image:: https://img.shields.io/github/license/pawelad/pymonzo.svg
   :target: https://github.com/pawelad/pymonzo/blob/master/LICENSE


