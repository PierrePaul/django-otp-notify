from unittest import mock

from django.db import IntegrityError
from django.test.utils import override_settings

from django_otp.tests import TestCase, ThrottlingTestMixin
from freezegun import freeze_time

from .conf import settings


class NotifyDeviceMixin:
    def setUp(self):
        try:
            alice = self.create_user('alice', 'password')
            bob = self.create_user('bob', 'password')
        except IntegrityError:
            self.skipTest("Unable to create test users.")
        else:
            self.device = alice.notifysmsdevice_set.create(number='test')
            self.device2 = bob.notifysmsdevice_set.create(number='test')


@override_settings(
    OTP_NOTIFY_NO_DELIVERY=True,
    OTP_NOTIFY_CHALLENGE_MESSAGE='{token}',
    OTP_NOTIFY_THROTTLE_FACTOR=0,
)
class TestNotifySMS(NotifyDeviceMixin, TestCase):
    def setUp(self):
        super().setUp()

        self._delivered = None

    def test_instant(self):
        """ Verify a code the instant it was generated. """
        with freeze_time():
            token = self.device.generate_challenge()
            ok = self.device.verify_token(token)

        self.assertTrue(ok)

    def test_barely_made_it(self):
        """ Verify a code at the last possible second. """
        with freeze_time() as frozen_time:
            token = self.device.generate_challenge()
            frozen_time.tick(delta=(settings.OTP_NOTIFY_TOKEN_VALIDITY - 1))
            ok = self.device.verify_token(token)

        self.assertTrue(ok)

    def test_too_late(self):
        """ Try to verify a code one second after it expires. """
        with freeze_time() as frozen_time:
            token = self.device.generate_challenge()
            frozen_time.tick(delta=(settings.OTP_NOTIFY_TOKEN_VALIDITY + 1))
            ok = self.device.verify_token(token)

        self.assertFalse(ok)

    def test_code_reuse(self):
        """ Try to verify the same code twice. """
        with freeze_time():
            token = self.device.generate_challenge()
            ok1 = self.device.verify_token(token)
            ok2 = self.device.verify_token(token)

        self.assertTrue(ok1)
        self.assertFalse(ok2)

    def test_cross_user(self):
        with freeze_time():
            token = self.device.generate_challenge()
            ok = self.device2.verify_token(token)

        self.assertFalse(ok)

    @override_settings(
        OTP_NOTIFY_NO_DELIVERY=False,
    )
    def test_format(self):
        with mock.patch('otp_notify.models.NotifySMSDevice._deliver_token', self._deliver_token):
            self.device.generate_challenge()

        self.assertEqual(self.device.token, self._delivered)

    #
    # Utilities
    #

    def _deliver_token(self, token):
        self._delivered = token


@override_settings(
    OTP_NOTIFY_NO_DELIVERY=True,
    OTP_NOTIFY_THROTTLE_FACTOR=1,
)
class ThrottlingTestCase(NotifyDeviceMixin, ThrottlingTestMixin, TestCase):
    def valid_token(self):
        if self.device.token is None:
            self.device.generate_token()

        return self.device.token

    def invalid_token(self):
        return -1
