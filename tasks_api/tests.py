from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Team, MyUser


def UserToken():
    user = MyUser(username='testman', password='1234')
    user.save()
    refresh = RefreshToken.for_user(user)
    return user, f'Bearer {refresh.access_token}'




