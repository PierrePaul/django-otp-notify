import django.conf
import django.test.utils


class Settings(object):
    """
    This is a simple class to take the place of the global settings object. An
    instance will contain all of our settings as attributes, with default
    values if they are not specified by the configuration.
    """
    _defaults = {
        'OTP_NOTIFY_API_KEY': None,
        'OTP_NOTIFY_ENDPOINT': 'https://api.notifications.service.gov.uk',
        'OTP_NOTIFY_TEMPLATE_ID': None,
        'OTP_NOTIFY_SENDER_ID': None,
        'OTP_NOTIFY_NO_DELIVERY': False,
        'OTP_NOTIFY_THROTTLE_FACTOR': 1,
        'OTP_NOTIFY_TOKEN_VALIDITY': 30,
    }

    def __getattr__(self, name):
        if hasattr(django.conf.settings, name):
            value = getattr(django.conf.settings, name)
        elif name in self._defaults:
            value = self._defaults[name]
        else:
            raise AttributeError(name)

        return value


settings = Settings()
