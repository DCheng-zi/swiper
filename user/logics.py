import random

import requests
from django.core.cache import cache

from swiper import conf

def gen_rand_code(length=6):
    '''产生指定长度随机验证码'''
    chars = []
    for i in range(length):
        chars.append(str(random.randint(0,9)))
    return ''.join(chars)



def send_sms(mobile):
    '''发送短信验证码'''

    key = 'Vcode-%s' % mobile


    #检查短信发送状态，防止重复发送
    if cache.get(key):
        return True  #之前发送过，直接返回True

    vcode = gen_rand_code() #产生验证码
    print ('验证码:%s' % vcode)

    args = conf.YZX_SMS_ARGS.copy()
    args['param'] = vcode
    args['mobile'] = mobile

    response =  requests.post(conf.YZX_SMS_API,json=args)
    if response.status_code == 200:
        result =  response.json()
        print('短信发送状态:%s' % result.get('msg'))
        if result.get('code') == '000000':
            cache.set(key,vcode,600)
            return True
        else:
            return False
    return False