import logging

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.encoding import force_text

from django_otp.models import SideChannelDevice, ThrottlingMixin
from django_otp.util import hex_validator, random_hex

from notifications_python_client.errors import HTTPError
from notifications_python_client.notifications import NotificationsAPIClient

from .conf import settings


logger = logging.getLogger(__name__)


def default_key():  # pragma: no cover
    """ Obsolete code here for migrations. """
    return force_text(random_hex(20))


def key_validator(value):  # pragma: no cover
    """ Obsolete code here for migrations. """
    return hex_validator(20)(value)


class NotifySMSDevice(ThrottlingMixin, SideChannelDevice):
    """
    A :class:`~django_otp.models.SideChannelDevice` that delivers a token via
    the Notify SMS service.

    The tokens are valid for :setting:`OTP_NOTIFY_TOKEN_VALIDITY` seconds. Once
    a token has been accepted, it is no longer valid.

    .. attribute:: number

        *CharField*: The mobile phone number to deliver to. `Notify recommends
        <https://docs.notifications.service.gov.uk/python.html#send-a-text-message>`_ using the
        `E.164 <http://en.wikipedia.org/wiki/E.164>`_ format. For UK numbers,
        this would look like '+447900900123'.
    """
    number = models.CharField(
        max_length=30,
        help_text="The mobile number to deliver tokens to (E.164)."
    )

    class Meta(SideChannelDevice.Meta):
        verbose_name = "Notify SMS Device"

    def get_throttle_factor(self):
        return settings.OTP_NOTIFY_THROTTLE_FACTOR

    def generate_challenge(self):
        """
        Sends the current TOTP token to ``self.number``.

        :raises: Exception if delivery fails.

        """
        self.generate_token(valid_secs=settings.OTP_NOTIFY_TOKEN_VALIDITY)


        if settings.OTP_NOTIFY_NO_DELIVERY:
            logger.info(f"Notify SMS token : {self.token}")
        else:
            self._deliver_token(self.token)

        return self.token

    def _deliver_token(self, token):
        self._validate_config()
        notifications_client = NotificationsAPIClient(
            settings.OTP_NOTIFY_API_KEY,
            base_url=settings.OTP_NOTIFY_ENDPOINT
        )

        try:
            response = notifications_client.send_sms_notification(
                phone_number=self.number,
                template_id=settings.OTP_NOTIFY_TEMPLATE_ID,
                sms_sender_id=settings.OTP_NOTIFY_SENDER_ID,
                personalisation={'token': token},
            )
        except HTTPError as e:
            logger.exception(e.message)
            raise Exception(e.message[0].get("message"))

        return response

    def _validate_config(self):
        if settings.OTP_NOTIFY_API_KEY is None:
            raise ImproperlyConfigured('OTP_NOTIFY_API_KEY must be set to your Notify api key')

        if settings.OTP_NOTIFY_TEMPLATE_ID is None:
            raise ImproperlyConfigured('OTP_NOTIFY_TEMPLATE_ID must be set to your message template id in Notify')

    def verify_token(self, token):
        verify_allowed, _ = self.verify_is_allowed()
        if verify_allowed:
            verified = super().verify_token(token)

            if verified:
                self.throttle_reset()
            else:
                self.throttle_increment()
        else:
            verified = False

        return verified
