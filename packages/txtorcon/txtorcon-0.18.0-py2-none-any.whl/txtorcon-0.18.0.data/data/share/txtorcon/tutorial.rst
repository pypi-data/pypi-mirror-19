txtorcon Tutorial
=================

.. note::

    **NOT COMPLETE** this is a work-in-progress against an in-development API.

This builds up, step-by-step, a tiny program that uses the main
features of txtorcon. We will:

  - copy-pasta some Twisted boilerplate;
  - launch our own Tor instance (or connect to one);
  - show all the circuits;
  - add a simple Onion service;
  - change our Tor's configuration;
  - shut down the Tor instance;

We concentrate on the highest-level API, the :class:`txtorcon.Tor`
class. There are lower-level APIs available for everything that's done
here, but this is the easiest. To see the other available APIs you can
use the API-docs, some of the HOWTOs and the many :ref:`examples`.


Before We Begin
---------------

All the file-listings quoted below are in ``./tutorial/*.py`` for
convenience.

If you do not yet have a development environment with txtorcon
installed, please see :ref:`installing`. You can prove your
environment is working by opening a file called `tutorial0.py` with
your favourite editor and typing:

Listing :download:`tutorial0.py <../tutorial/tutorial0.py>`:

.. literalinclude:: ../tutorial/tutorial0.py


Then, run ``python tutorial0.py`` in a terminal. If everything is set
up properly, your terminal should show something like this:

.. code-block:: shell-session

    $ python ./tutorial/tutorial0.py
    it worked!
    $

If you are having problems, the best thing is to contact me on IRC;
see :ref:`getting help`.


Twisted's main
--------------

If you do not already know how to do event-based programming in
Twisted, you should learn that first. Start with `Twisted's narrative
documentation
<http://twistedmatrix.com/documents/current/core/howto/index.html>`_
or the very fine `Twisted tutorial
<http://krondo.com/an-introduction-to-asynchronous-programming-and-twisted/>`_
by Dave Peticolas.

We use the `task <https://twistedmatrix.com/documents/current/api/twisted.internet.task.html>`_ and `endpoints <https://twistedmatrix.com/documents/current/api/twisted.internet.endpoints.html>`_ APIs from Twisted and
`@inlineCallbacks <http://twistedmatrix.com/documents/current/core/howto/defer-intro.html#inline-callbacks-using-yield>`_ extensively; if you're used to calling
``reactor.run`` you'll want to read about `task.react
<http://twistedmatrix.com/documents/current/api/twisted.internet.task.html#react>`_.

In any case, we need some Twisted boilerplate to get a running
"client"-style program; if any of this looks confusing please see the
documentation linked above.

Listing :download:`tutorial1.py <../tutorial/tutorial1.py>`:

.. literalinclude:: ../tutorial/tutorial1.py


Default Values
--------------

txtorcon strives to have sane, safe defaults. For all APIs if you're
in doubt about whether to pass an optional argument, it is most likely
that you can simply allow the default value to be assigned. If you
think you've found a case where this *isn't* true, please file a bug!


Launching (or Connecting to) Tor
--------------------------------

Obviously, txtorcon depends on having a running tor daemon to talk to;
if you're having trouble with installing and running tor itself, see
`Tor's documentation
<https://www.torproject.org/docs/documentation.html.en>`_.

"A running tor" is abstracted in txtorcon with instances of the
:class:`txtorcon.Tor` class. This can be either a Tor that we
ourselves launched, or one that was already running that we connect
to. From there, we can ask this instance to create other useful
txtorcon objects.

.. note::

    Tor allows multiple control connections, and txtorcon can
    instantiate multiple "Tor" class instances talking to the same
    underlying tor daemon. This complicates a few things, but for the
    most part will work "as expected" from the outside. See the
    :class:`txtorcon.Tor` API documentation for how shutdown is
    handled. See :class:`txtorcon.TorState` for a caveat about what
    "up to date" means.

For simplicity, we will launch our own Tor instance.  So, building on
the "Twisted boilerplate" from above, we do the simplest possible
launching (don't panic if this doesn't immediately work; we add more
information + debugging :ref:`immediately below`):

Listing :download:`tutorial2.py <../tutorial/tutorial2.py>`:

.. literalinclude:: ../tutorial/tutorial2.py

The launching may take a while (e.g. several minutes) depending upon
your connection. Although the above looks simple, there's a lot going
on under the hood. Before explaining that, lets at least add three
very useful things:

  - progress message updates (1);
  - an explicit ``DataDirectory`` for Tor (2);
  - Tor's raw stdout output (useful for debugging) (3).


.. _immediately below:

Listing :download:`tutorial3.py <../tutorial/tutorial3.py>`:

.. literalinclude:: ../tutorial/tutorial3.py

Now we can at least see what Tor is doing while it launches! Giving an
explicit ``DataDirectory`` means that txtorcon will no longer delete
the whole thing when we exit; this saves the Tor directory authorities
some bandwidth and makes our startup time much shorter. Try running
the above twice in a row to illustrate this.

You can pass any file-like object to ``stdout=`` and ``stderr=``. See
:func:`txtorcon.launch_tor` for all options.

Now that we know how to create our :class:`txtorcon.Tor` instance
we'll want to do something with it. "Something" can be broadly
categorized as "server-side" or "client-side". Either use may or may
not include monitoring some aspects of Tor's current state.

In Tor, "service-side" things are called "Onion Services" (or before
that "Hidden Services"). In Twisted, a server-side endpoint (see
`Twisted docs
<http://twistedmatrix.com/documents/current/core/howto/endpoints.html>`_)
must implement IServerStreamEndpoint_ and a client-side one implements
IClientStreamEndpoint_.

.. _IServerStreamEndpoint: https://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IStreamServerEndpoint.html
.. _IClientStreamEndpoint: https://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IStreamClientEndpoint.html

First, however, we'll look at listening to and changing Tor's state.


Protocol, State and Configuration
---------------------------------

Each :class:`txtorcon.Tor` instance contains one instance that
implements :class:`txtorcon.ITorControlProtocol` (this is currently
always a :class:`txtorcon.TorControlProtocol` but the interface
declares the public API).

If you want to queue tor control commands directly or add listeners
for Tor events directly, you can use this class. However, this is
pretty "low level" stuff and you should be able to use one of
:class:`txtorcon.TorState` or :class:`txtorcon.TorConfig`.

These instances are created with :meth:`txtorcon.Tor.create_state` or
:meth:`txtorcon.Tor.create_config`. It is also possible to create a
``TorConfig`` instance without a protocol connection -- used when
launching a fresh Tor instance, for example. (Note that when used in
this manner, the very same TorConfig instance as passed to ``launch``
will be returned by ``create_config``).

So, here's an example which shows all current circuits and streams in
Tor, utilizing :class:`txtorcon.TorState`. Note that this provides
"live" Tor state -- ``TorState`` subscribes to certain events and
updates structures accordingly.

Listing :download:`tutorial4.py <../tutorial/tutorial4.py>`:

.. literalinclude:: ../tutorial/tutorial4.py

Some things to notice:

 - all of the "accessing data" usage of the API is attribute-access
   style;
 - "doing things" to data is a method call, often returning Deferred;
 - all the data is "live", so we can keep printing things in a loop
   and they'll represent current Tor state;
 - no need to yield for each bit of data/state required.

If you're really interested in when circuits appear or disappear (or
streams), it's much better to use the "listener" API. That means
implementing a :class:`txtorcon.IStreamListener` (or
subclassing :class:`txtorcon.StreamListenerMixin`). There
are similar ones for circuits:
:class:`txtorcon.ICircuitListener` and
:class:`txtorcon.CircuitListenerMixin`.

You can add instances implementing these interfaces with
:meth:`txtorcon.TorState.add_circuit_listener` or
:meth:`txtorcon.TorState.add_stream_listener`.

Modifying the example to listen for stream events:

Listing :download:`tutorial5.py <../tutorial/tutorial5.py>`:

.. literalinclude:: ../tutorial/tutorial5.py

To make some streams through this launched Tor instance, we need to
speak SOCKS5 to port 9999, for example with ``curl``::

    curl --socks5-hostname localhost:9999 https://check.torproject.org/api/ip

You'll note that the ``tutorial5.py`` code causes every second stream
to be immediately closed, which should manifest as an error on the
``curl`` side for ever other request.


Server-Side Endpoints
---------------------

To create an object that implements IServerStreamEndpoint_, you call :meth:`txtorcon.Tor.create_onion_endpoint`. This creates a "disk-based" onion service, where the configuration (i.e. public/private keys) are in a ``HiddenServiceDir`` someone on the filesystem. This is in contrast to :meth:`txtorcon.Tor.create_ephemeral_onion_endpoint` which instead uses the ``ADD_ONION`` API from Tor to create an onion service whose keys are only ever communicated over the Tor control protocol.

In either case, when you call ``.listen()`` on the endpoint, the
appropriate things will happen such that the Tor we're talking to has
a new hidden-service added to it. You get back a
:class:`txtorcon.TorOnionListeningPort` when that Deferred fires
(shhhh! you're only supposed to know it's a Twisted IListeningPort_!)
which gives a :class:`txtorcon.TorOnionAddress` back from
``.getHost``. This is how you gain access to the public-key hash which
makes up the ``timaq4ygg2iegci7.onion`` address.

It sounds more complex than in practice, where it works naturally with
things like Twisted's ``Site`` for Web.

Listing :download:`tutorial6.py <../tutorial/tutorial6.py>`:

.. literalinclude:: ../tutorial/tutorial6.py

One thing that happens after the ``.listen()`` call is that a
"descrpitor" is uploaded to the Tor network, which can take a bit of
time. For details of how the hidden-service system works overall, see
Tor's `hidden service protocol
<https://www.torproject.org/docs/hidden-services.html.en>`_ page.



**Connecting, instead**: all of this tutorial and any use for the
:class:`txtorcon.Tor` APIs will work the same with a "launched" or
"connected to" tor -- so if you prefer, you should be able to follow
along by calling :meth:`txtorcon.connect` instead of
:meth:`txtorcon.launch`; see the API documentation for details.
