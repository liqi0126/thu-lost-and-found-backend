import json
import xml.etree.ElementTree as Et
from datetime import datetime

import requests
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.http import HttpResponseBadRequest, Http404, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken

from thu_lost_and_found_backend import settings
from thu_lost_and_found_backend.authentication_service.wechat_msg_encryption import WXBizMsgCrypt
from thu_lost_and_found_backend.helpers.toolkits import check_missing_fields
from thu_lost_and_found_backend.user_service.models import User


def create_user_base_on_wechat(open_id):
    return User.objects.create(
        wechat_id=open_id,
        username=str(open_id),
        password=make_password('wechat_default_password'),
        first_name='New',
        last_name='User',
        is_verified=False,
        status='ACT',
        is_staff=False,
        is_superuser=False,
        date_joined=datetime.now()
    )


def wechat_component_verify_ticket(request):
    if request.method != 'POST':
        return Http404()

    token = ''
    encoded_xml = request.body
    msg_signature = request.GET['msg_signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']

    decrypt_test = WXBizMsgCrypt(token, settings.WECHAT_AES_KEY, settings.WECHAT_APP_ID)
    status, decrypted_xml = decrypt_test.DecryptMsg(encoded_xml, msg_signature, timestamp, nonce)

    if status != 0:
        print("Error occurred when decrypting component_verify_ticket")
        return

    component_verify_ticket = Et.fromstring(decrypted_xml).find('ComponentVerifyTicket')

    # Cache for 12 hours
    cache.set('component_verify_ticket', component_verify_ticket, 12 * 60 * 60)

    return 'success'


def wechat_token(request):
    if request.method != 'POST':
        return Http404()

    contents = json.loads(request.body)
    missing_fields = check_missing_fields(contents, ["code"])
    if missing_fields:
        return HttpResponseBadRequest(json.dumps(missing_fields))

    js_code = contents['code']

    component_verify_ticket = cache.get('component_verify_ticket')

    component_access_token = cache.get('component_access_token')

    if not component_verify_ticket:
        print('Missing component_verify_ticket')
        return HttpResponse(status=502)

    if not component_access_token:
        url = 'https://api.weixin.qq.com/cgi-bin/component/api_component_token'
        data = {
            "component_appid": settings.WECHAT_COMPONENT_APP_ID,
            "component_appsecret": settings.WECHAT_COMPONENT_APP_SECRET,
            "component_verify_ticket": component_verify_ticket
        }
        response = requests.post(url, data=data)

        response = json.loads(response.json())

        component_access_token = response['component_access_token']

        # Cache for 2 hours
        cache.set('component_access_token', response['component_access_token'], 7200)

    # Login wechat user
    login_url = f'https://api.weixin.qq.com/sns/component/jscode2session' \
                f'?appid={settings.WECHAT_APP_ID}' \
                f'&js_code={js_code}&grant_type=authorization_code' \
                f'&component_appid={settings.WECHAT_COMPONENT_APP_ID}' \
                f'&component_access_token={component_access_token}'

    login_response = json.loads(requests.get(login_url).json())
    if 'openid' not in login_response:
        print('Error: Wechat login failed')
        return HttpResponseBadRequest('Invalid code')

    open_id = login_response['openid']

    try:
        user = User.objects.get(wechat_id=open_id)
    except User.DoesNotExist:
        user = create_user_base_on_wechat(open_id)

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
