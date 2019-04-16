""" This is backend Module """
from django.contrib.auth.models import User


class EmailBacked:
    """ This is email backend """

    @classmethod
    def authenticate(cls, request, username=None, password=None):
        """ This is email backend """
        kwargs = {'email': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
