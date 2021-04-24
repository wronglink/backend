from users.models import ME_ALIAS


class ViewSetWithUsernameMixin:
    def get_username(self, lookup_field: str = 'username'):
        username = self.kwargs[lookup_field]
        if username == ME_ALIAS:
            username = self.request.user.username
        return username
