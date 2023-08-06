.. _mail:

=====
Email
=====

.. contents:: :local:

Introduction
============

Websauna provides facilities to send out emails

* Outgoing email is tied to the success of transaction - if your code fails in some point no email is sent

* Rich-text HTML emails are supported with `premailer package <https://pypi.python.org/pypi/premailer>`_ which will turn :term:`CSS` styles to inline styles for emails

* `pyramid_mailer <https://github.com/Pylons/pyramid_mailer>`_ package provides low-level interface for outgoing email

Configuring email
=================

Local development: no outgoing email traffic by default
-------------------------------------------------------

When you run a development server, no email goes out by default. Instead it is printed into your console where :ref:`ws-pserve` is running. This is the default behavior of :ref:`development.ini`.

Setting up real SMTP service
----------------------------

For actual outgoing emails you need to have an SMTP service agreement from some of the providers. You may or may not want to use Postfix server as a local buffer. The default behavior of :ref:`production.ini` is to use local SMTP server at localhost:25.

.. note ::

    You need to change outbound email settings in :ref:`development.ini` if you want to test email out from your local laptop.

See :ref:`outbound-email-ini` below for more information.

Sending out email
=================

Mixed HTML and plain text email
-------------------------------

Websauna supports mixed HTML + plain text emails. Websauna email messages are assembled from three different templates with a specific naming convention. Email templates are not different from web page templates, same Jinja templating engine is utilized.

* ``$message.body.html`` - HTML email body

* ``$message.body.txt`` - Plain text email body

* ``$message.subject.txt`` - Email subject

Below is a sample email.

``email/welcome.subject.txt``:

.. code-block:: jinja

    {% extends "email/base_subject.txt" %}
    {% block subject %}Welcome to {{site_name}}{% endblock %}

``email/welcome.body.txt``:

.. code-block:: jinja

    Welcome to {{ site_name }}!

    Thank you for signing up!
    Please visit the link below to see how {{ site_name }} will make your life simpler.

    {{ request.route_url('home') }}

``email/welcome.body.html``:

.. code-block:: html+jinja

    {% extends "email/base.html" %}

    {% block content %}
        <p>
        Welcome to {{site_name}},
        </p>

        <p>
        Thank you for signing up! Please visit the link below to see how {{ site_name }} will make your life simpler.
        </p>

        <p style="text-align: center">
            <a class="btn-primary" href="{{ request.route_url('home') }}">Visit {{ site_name }}</a>
        </p>

    {% endblock %}

To send out this email use :py:func:`websauna.system.mail.send_templated_mail`:

.. code-block:: python

    from websauna.system.mail import send_templated_mail

    def my_view(request):
        user = request.user
        send_templated_mail(request, [user.email], "email/welcome", context={})

Email and transaction bounderies
--------------------------------

Email is send out only if the transaction commits. If the request fails (HTTP 500) and the transaction is aborted then no email is sent.

If you are doing email out from command line jobs or :ref:`tasks` make sure you close your transactions properly or there is no email out.

If you are sending email outside the normal transaction lifecycle check out ``immediate`` parameter of :py:func:`websauna.system.mail.send_templated_mail`:

.. code-block:: python

    # Do not wait for the commit
    send_templated_mail(request, [user.email], "email/welcome", context={}, immediate=True)

Sender envelope header
----------------------

If you want to have the email "To:" header to contain the full name of the receiver you can do the following.

TODO

Raw pyramid_mail API
--------------------

Sending out test mail with raw pyramid_mailer:

.. code-block:: python

    from pyramid_mailer import get_mailer
    from pyramid_mailer.message import Message

    sender = request.registry.settings["mail.default_sender"]

    message = Message(subject="pyramid_mailer test", sender="no-reply@redinnovation.com", recipients=["mikko@redinnovation.com"], body="yyy")

    mailer = get_mailer(request)
    mailer.send_immediately(message)

HTML layout
===========

To edit HTML layout and CSS styles make a copy of :ref:`email/base.html <template-email/base.html>` to your application. Edit syles inside `<style>`.

Testing HTML layout
-------------------

You can render a dummy HTML email in your browser by going to:

    http://localhost:6543/sample-html-email

See :ref:`websauna.sample_html_email` configuration for more information.

Accessing email in tests
========================

For a peek into outbound email you can do::

    TODO


.. _outbound-email-ini:

Configuring outbound email
==========================

Below is an :term:`INI` configuration example to send emails through `Sparkpost <https://www.sparkpost.com/>`_. This will make *pyramid_mailer* directly to talk remote SMTP server. These settings are good for local development when you need to see the actual outbound email message content properly.

External service example:

.. code-block:: ini

    [main]

    # ...
    # other settings go here
    # ...

    websauna.mailer = mail
    mail.default_sender = no-reply@wattcoin.com
    mail.default_sender_name = Example Tech Corp
    mail.tls = true
    mail.host = smtp.sparkpostmail.com
    mail.port = 587
    mail.username = SMTP_Injection
    mail.password = <your Sparkpost API token>

Local Postix example:

.. code-block:: ini

    [main]

    # ...
    # other settings go here
    # ...

    websauna.mailer = mail
    mail.host = localhost
    mail.port = 25
    mail.username =
    mail.password =

For more complex production environment outbound email with local :term:`Postfix` buffering, see :ref:`outbound email chapter in Ansible playbook <outbound-email>`.

Testing outbound email from console
-----------------------------------

You can test outbound email in Python console (:ref:`notebook` or :ref:`ws-shell`):

.. code-block:: python

    from pyramid_mailer import get_mailer
    from pyramid_mailer.message import Message
    from websauna.utils.time import now

    sender = "no-reply@youroutboundmaildomain.net"
    recipients = ["mikko@example.com"]
    subject = "Test mail"
    text_body = "This is a test message {}".format(now())
    mailer = get_mailer(request)

    message = Message(subject=subject, sender=sender, recipients=recipients, body=text_body)
    message.validate()
    mailer.send_immediately(message)



