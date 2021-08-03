from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from social_core.exceptions import AuthForbidden

from users.forms import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))

    response = requests.get(api_url)

    if response.status_code != 200:
        return

    data = response.json()['response'][0]

    if 'sex' in data:
        if data['sex'] == 1:
            user.userprofile.gender = UserProfile.FEMAL
        elif data['sex'] == 2:
            user.userprofile.gender = UserProfile.MALE

    if 'about' in data:
        user.userprofile.about_me = data['about']

    if 'bdate' in data:
        bdate = datetime.strptime(data['bdate'], "%d.%m.%Y")
        age = datetime.now().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.userprofile.age = age

    user.save()
