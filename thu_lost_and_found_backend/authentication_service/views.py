import json
from datetime import datetime

import requests
from django.contrib.auth.hashers import make_password
from django.http import Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from thu_lost_and_found_backend import settings
from thu_lost_and_found_backend.helpers.toolkits import check_missing_fields
from thu_lost_and_found_backend.user_service.models import User


def create_user_base_on_wechat(open_id):
    return User.objects.create(
        wechat_id=open_id,
        username=str(open_id),
        password=make_password('wechat_default_password'),
        first_name='Thu',
        last_name='Student',
        is_verified=False,
        status='ACT',
        is_staff=False,
        is_superuser=False,
        date_joined=datetime.now()
    )


@csrf_exempt
def wechat_token(request):
    if request.method != 'POST':
        return Http404()

    contents = json.loads(request.body)
    missing_fields = check_missing_fields(contents, ["code"])
    if missing_fields:
        return HttpResponseBadRequest(json.dumps(missing_fields))

    js_code = contents['code']
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': settings.WECHAT_APP_ID,
        'secret': settings.WECHAT_APP_SECRET,
        'js_code': js_code,
        'grant_type': 'authorization_code'
    }

    response = requests.get(url=url, params=params)

    response = response.json()

    if response['errcode'] != 1:
        return HttpResponseBadRequest('Invalid code')

    open_id = response['openid']

    try:
        user = User.objects.get(wechat_id=open_id)
    except User.DoesNotExist:
        user = create_user_base_on_wechat(open_id)

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
