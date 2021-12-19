from datetime import datetime

from config import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36, urlsafe_base64_decode, urlsafe_base64_encode


class EmailVerificationTokenGenerator:
    """
    Strategy object used to generate and check tokens for the password
    reset mechanism.
    """
    try:
        key_salt = settings.CUSTOM_SALT
    except AttributeError:
        key_salt = "django-email-verification.token"
    algorithm = None
    secret = settings.SECRET_KEY

    def make_token(self, user, expiry=None):
        """
        Return a token that can be used once to do a password reset
        for the given user.
        Args:
            user (Model): the user
            expiry (datetime): optional forced expiry date
        Returns:
             (tuple): tuple containing:
                token (str): the token
                expiry (datetime): the expiry datetime
        """
        if expiry is None:
            return self._make_token_with_timestamp(user, self._num_seconds(self._now()))
        return self._make_token_with_timestamp(user, self._num_seconds(expiry) - settings.EMAIL_TOKEN_LIFE)

    def check_token(self, token):
        """
        Check that a password reset token is correct.
        Args:
            token (str): the token from the url
        Returns:
            (tuple): tuple containing:
                valid (bool): True if the token is valid
                user (Model): the user model if the token is valid
        """

        try:
            email_b64, ts_b36, _ = token.split("-")
            email = urlsafe_base64_decode(email_b64).decode()
            if hasattr(settings, 'EMAIL_MULTI_USER') and settings.EMAIL_MULTI_USER:
                users = get_user_model().objects.filter(email=email)
            else:
                users = [get_user_model().objects.get(email=email)]
            ts = base36_to_int(ts_b36)
        except (ValueError, get_user_model().DoesNotExist):
            return False, None

        user = next(filter(lambda u: constant_time_compare(self._make_token_with_timestamp(u, ts)[0], token), users),
                    None)

        if not user:
            return False, None

        now = self._now()
        if (self._num_seconds(now) - ts) > settings.EMAIL_TOKEN_LIFE:
            return False, None

        return True, user

    def _make_token_with_timestamp(self, user, timestamp):
        email_b64 = urlsafe_base64_encode(user.email.encode())
        ts_b36 = int_to_base36(timestamp)
        hash_string = salted_hmac(
            self.key_salt,
            self._make_hash_value(user, timestamp),
            secret=self.secret,
        ).hexdigest()
        # print(hash_string)
        return f'{email_b64}-{ts_b36}-{hash_string}', \
               datetime.fromtimestamp(timestamp + settings.EMAIL_TOKEN_LIFE)

    @staticmethod
    def _make_hash_value(user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + user.password + str(login_timestamp) + str(timestamp)

    @staticmethod
    def _num_seconds(dt):
        return int((dt - datetime(2001, 1, 1)).total_seconds())

    @staticmethod
    def _now():
        return datetime.now()


default_token_generator = EmailVerificationTokenGenerator()