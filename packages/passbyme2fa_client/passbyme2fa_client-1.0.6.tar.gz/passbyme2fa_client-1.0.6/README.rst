PassBy[ME] Mobile ID client
===========================

This library provides you with functionality to handle PassBy[ME]
messages.

For further information on PassBy[ME] please visit:
`www.passbyme.com <https://www.passbyme.com>`__ and sign up for a free
account. You can download our API documentation after login.

Table of contents
=================

-  `Installation <#installation>`__
-  `Usage <#usage>`__

   -  `PassByME2FAClient <#passbyme2faclient>`__
   -  `Handling messages <#handling-messages>`__

      -  `Sending messages <#sending-messages>`__
      -  `Tracking messages <#tracking-messages>`__
      -  `Cancelling messages <#cancelling-messages>`__
      -  `SessionInfo <#sessioninfo>`__

   -  `Errors <#errors>`__

      -  `HTTPError <#httperror>`__
      -  `PassByMEError <#passbymeerror>`__

-  `Build <#build>`__
-  `Release History <#release-history>`__

Installation
============

::

    pip install passbyme2fa_client

Usage
=====

To use the PassBy[ME] Mobile ID SDK first you have to acquire the
following:

-  Account authentication PEM file and its password

You can get these after registering at
`www.passbyme.com <https://www.passbyme.com>`__, by hitting the "Sign up
for free" button. To complete the registration you will need an Android,
iOS or Windows Phone device with the PassBy[ME] application installed.

If you login after registration you can download the PEM from the
Application menu. You can add new applications to your registration by
hitting the "New application". The application (along with its
Application Id) will appear in the table below.

*We suggest you to read the available User Guides and API documentation
before you continue with the integration. You can download these from
the Documentation section of the administration website after login.*

PassByME2FAClient
-----------------

.. code:: python

    from passbyme2fa_client import *

    pbm = PassByME2FAClient(
      key = "auth.pem",
      cert = "auth.pem",
      password = "<auth.pem password>"
    )

The **PassByME2FAClient** constructor accepts the following parameters:

-  **key**: the path of the authentication key PEM file.
-  **cert**: the path of the authentication certificate PEM file. (May
   be the same as **key** if the PEM file contains both the certificate
   and the key.)
-  **address**: The address of the PassBy[ME] service to use. This
   parameter is optional. by default the SDK will connect to
   auth-sp.passbyme.com.

Throws a
`ValueError <https://docs.python.org/3/library/exceptions.html#ValueError>`__
when a required parameter is missing.

Handling Messages
-----------------

Sending messages
~~~~~~~~~~~~~~~~

.. code:: python

    session_info = pbm.send_message(
      recipients = ["test@pers.on"],
      availability = 300,
      type = PassByME2FAClient.MessageType.AUTHORIZATION,
      subject = "Test subject", body = "Test message"
    )

The **send\_message** method accepts the following parameters:

-  **recipients**: An array containing the PassBy[ME] ID-s of the
   recipients
-  **subject**: The subject of the message
-  **body**: The body of the message
-  **availability**: The availability of the message in seconds
-  **type**: One of the following types:

   -  **PassByME2FAClient.MessageType.AUTHORIZATION** - for
      authorization requests
   -  **PassByME2FAClient.MessageType.MESSAGE** - to send a general
      message with arbitrary body
   -  **PassByME2FAClient.MessageType.ESIGN** - if the message body
      contains an esign url

When successful, returns a `SessionInfo <#sessioninfo>`__ object.

Throws a
`ValueError <https://docs.python.org/3/library/exceptions.html#ValueError>`__
when a required parameter is missing. Throws an
`HTTPError <#httperror>`__ if an error in HTTP communication occurs.
**HTTPError.response** contains the HTTP response. Throws a
`PassByMEError <#passbymeerror>`__ if a PassBy[ME] specific error
occurs. **PassByMEError.response** contains the JSON response received
from the PassBy[ME] server as a dictionary.

Tracking messages
~~~~~~~~~~~~~~~~~

.. code:: python

    session_info.refresh()

To track messages, the most efficient way is to call
**SessionInfo.refresh()**. After a successful call, the
`SessionInfo <#sessionInfo>`__ object will contain up-to-date
information about the message.

Throws an `HTTPError <#httperror>`__ if an error in HTTP communication
occurs. Throws a `PassByMEError <#passbymeerror>`__ if a PassBy[ME]
specific error occurs.

Cancelling messages
~~~~~~~~~~~~~~~~~~~

.. code:: python

    session_info.cancel()

To cancel the message, the most efficient way is to call
**SessionInfo.cancel()**. After a successful call, the message will be
cancelled and the `SessionInfo <#sessionInfo>`__ object will contain
up-to-date information about the message.

Throws an `HTTPError <#httperror>`__ if an error in HTTP communication
occurs. Throws a `PassByMEError <#passbymeerror>`__ if a PassBy[ME]
specific error occurs.

SessionInfo
~~~~~~~~~~~

The **SessionInfo** object describes the state of a message session. It
consists of the following attributes:

-  **message\_id**: The id of the message that can be used to reference
   the message
-  **expiration\_date**: The date and time (as an
   `Arrow <http://crsmithdev.com/arrow/#arrow.arrow.Arrow>`__ object)
   until which the message can be downloaded with the PassBy[ME]
   applications
-  **recipient\_statuses**: An array of **RecipientStatus** objects.
   Each object consist of the following fields:

   -  **user\_id**: The PassBy[ME] ID of the user represented by this
      recipient object
   -  **status**: The delivery status of this message for this user

Available statuses are (all constants available as
**PassByME2FAClient.MessageStatus.**\ \*):

-  **PENDING**: Initial status of the message.
-  **NOTIFIED**: The recipient has been notified about a new message.
-  **DOWNLOADED**: The recipient has downloaded the message, but has not
   uploaded the evidence yet.
-  **SEEN**: The recipient has seen the message and uploaded the
   evidence.
-  **NOT\_SEEN**: The recipient has not seen the message.
-  **NOT\_NOTIFIED**: The recipient has not received the notification.
-  **NOT\_DOWNLOADED**: The recipient received the notification about
   the message but has not downloaded the message
-  **NO\_DEVICE**: The message could not be sent because the recipient
   had no PassBy[ME] ready device that supports messaging.
-  **FAILED**: The message could not be sent because of an error.
-  **DISABLED**: The message could not be sent because the recipient is
   disabled.
-  **CANCELLED**: The message was cancelled by the sender.
-  **APPROVED**: Authentication has finished successfully.
-  **DENIED**: The user has cancelled the authentication.

Errors
------

HTTPError
~~~~~~~~~

Denotes that the server responded with a HTTP error code. Its readable
**response** attribute contains the
`HTTPResponse <https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse>`__
received from the server.

PassByMEError
~~~~~~~~~~~~~

Denotes a PassBy[ME] specific error. See the API documentation for the
possible error codes. Its readable **response** attribute contains the
JSON message received from the server as a dictionary.

Build
=====

To build the package, first we have to run our tests, which can be done
typing

::

    python setup.py test

If the tests all pass, we can create the distribution package using the
command

::

    python setup.py sdist
