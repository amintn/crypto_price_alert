import asyncio

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from email_normalize import Normalizer


UserModel = get_user_model()


def normalizer(email):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(Normalizer().normalize(email)).normalized_address


class NormalizedEmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return
        if "@" in username:
            get_user_kwargs = {"email": normalizer(username)}
        else:
            get_user_kwargs = {"phone": username}
        try:
            user = UserModel.objects.get(**get_user_kwargs)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
