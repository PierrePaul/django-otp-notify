django-otp-notify
=================

.. include:: ../../README.rst


Installation
------------

django-otp-notify can be installed via pip::

    pip install django-otp-notify


Once installed it should be added to INSTALLED_APPS after django_otp core::

    INSTALLED_APPS = [
        ...
        'django_otp',
        'django_otp.plugins.otp_totp',
        'django_otp.plugins.otp_hotp',
        'django_otp.plugins.otp_static',

        'otp_notify',
    ]


Notify SMS Devices
------------------

.. autoclass:: otp_notify.models.NotifySMSDevice
    :members:


Admin
-----

The following :class:`~django.contrib.admin.ModelAdmin` subclass is registered
with the default admin site. We recommend its use with custom admin sites as
well:

.. autoclass:: otp_notify.admin.NotifySMSDeviceAdmin


Settings
--------

.. setting:: OTP_NOTIFY_API_KEY

**OTP_NOTIFY_API_KEY**

Default: ``None``

Your Notify API key.


.. setting:: OTP_NOTIFY_ENDPOINT

**OTP_NOTIFY_ENDPOINT**

Default: ``None``

Your Notify endpoint.


.. setting:: OTP_NOTIFY_CHALLENGE_MESSAGE

**OTP_NOTIFY_CHALLENGE_MESSAGE**

Default: ``"Sent by SMS"``

The message returned by
:meth:`~otp_notify.models.NotifySMSDevice.generate_challenge`. This may contain
``'{token}'``, which will be replaced by the token. This completely negates any
security benefit to the device, but it's handy for development, especially in
combination with :setting:`OTP_NOTIFY_NO_DELIVERY`.


.. setting:: OTP_NOTIFY_SENDER_ID

**OTP_NOTIFY_SENDER_ID**

Default: ``None``

The sender id used to send SMS messages from. This is generated via the Notify dashboard.

.. setting:: OTP_NOTIFY_NO_DELIVERY

**OTP_NOTIFY_NO_DELIVERY**

Default: ``False``

Send tokens to the 'otp_notify.models' logger instead of delivering them by SMS.
Useful for development.


.. setting:: OTP_NOTIFY_THROTTLE_FACTOR

**OTP_NOTIFY_THROTTLE_FACTOR**

Default: ``1``

This controls the rate of throttling. The sequence of 1, 2, 4, 8... seconds is
multiplied by this factor to define the delay imposed after 1, 2, 3, 4...
successive failures. Set to ``0`` to disable throttling completely.


.. setting:: OTP_NOTIFY_TOKEN_VALIDITY

**OTP_NOTIFY_TOKEN_VALIDITY**

Default: ``30``

The number of seconds for which a delivered token will be valid.


Changes
-------

:doc:`changes`


License
-------

.. include:: ../../LICENSE
