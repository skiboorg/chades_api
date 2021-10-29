import webbrowser
from requests import Response
import os

# 沙箱模式用这个
APPID = '2021000118619554'
private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAgLYqRKDpdV18eKzGVR4hsBBrD9W8uS5gf4MrYnt4iM3hTC/Z2bisvgdJFP80YNPaeehBohAX9FAwBbYT6Qqf9jw5BAzWYp9KP1xBVUJGsiGoDlTp3FUtoFAs+DSG3Z9HdINr6Vx5714e0qnMzAPm7se0F8Pe8pChOp+qkqMtum3rvsvcl/btJ5MRQSauedZMB/FZZDRQfI5ozbgA3UhnAafzvquFkVAkVr9KTirrJfp8Hz5+LjGJSQ9zMp+G9/0n+GsbLBOu2322KnXZ/JCvxqxhbwZjIAAl1IGWmfCz3QNGsxYTEzI1rbFyd6wdDUCjVhag0oYzqILu6gWcHOb3HQIDAQABAoIBACZYHpd7aJFyXFaHAj7xTw/olDyPbD2ut0jFhvM73VjEHM5Zowjdn3itKvR6YtxFwNx4eLUTHk/GY8gPyjau16C/qCywtl2DHtdpYH1J1U3UAQDkAxeEuKb9u6fl3hfAD8WCMW/AAQNygrQ3qa9NqkqQa/J4g763n5CbaHFu83yKPPlehViyLzQuIm8bYI3f8Yd1jOeZ5IkpJ7+LX5VmWKv0zbi/kcNf0essfN4PhDI95Ear1ZB4vXShhavmEEwAXMR5ef1Au0E39SG07//0uWavpPiqfBBQcWDYJJW4qhr9fsrZ/V7P8en65HBs3pgCG/1lWr5yVOMH0pgfZ+eOQIECgYEA1o534hVGN9i7sWpRaH5xoPQXBDYValC/7oe2r8FllRyi634OamM/f/U1SR2zVvMm352HSHpGlimeeh848leD5E7qNPLYB4BaIxnIV6dlmWt0sKnNaX1yf0a4pc6v5S/SUqGCsD3Dar6NnjghYRZ8fafyreJI9Gv3gbVhAhnTWxUCgYEAmZLHsj8/eUaxvBRUx5C0+XFuwa43E3JGXMnRtIpr8ekJ8Lw3o2bl7qk0Tbr6WvRVVdn8Ej5nR359sAyV/cIwdL4jglOGwMSR/+0Jy7IzuTdG2kC+0ETfwyx5M1OMwTOsf4YocO6Jy0aqYS+HLjy5FKQa7REcNp379ZJk7daFDekCgYBmdfjYNbKnvs+7ZPtlfGTFKWvIbg+CCvftcFAU1LWvJNLExRkbQzQy5iXBOfbIAixBQ5g0S3hkA5IT3c8zJAnvQKRmDsaNpoTlGE3tVhqVzpQWPbDDvM2t7FcHj5G+UD0PiuO/SG+HDWLR+RovpC5lT4v78AFJADpdbgHan/yoFQKBgH8l21hkrTTHpxfE7Xxc/rkXhU+t4cOj9UWVgp4rjLu46ZX6/0W2R+CVDszcZbMwYAa4d87TA8dZns5HXVe/k0bUtamNZh/rn8V4h4eyfsh2T58bw9/DZk+9Xot0PTEoi0T52jnGBSfb1eyo4Q8TD1lblT95zxYZLyZeklmoJnkhAoGBAIbR+xSszlg3sVizSA4vn0bnSU7+FKhoc1HSKYQo1VGNCGhI96YgKNzmODttP4/e9cFg4eSk5SgGd46VBfnEBqeBS7RXrSciU+HlbfzbDIZ6zk+VazCT2yalnofDCWvfIMCI+W4IK92JB5iVO7yfTuf47FpIkqar3poM3c7QIaSH
-----END RSA PRIVATE KEY-----
'''
public_key = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwDAFim/BUOoLn0uSIarARf9uzwqViDJV06/Mk5h2sU+9QtCnZSWPOU8B2jwVjM+iUm0VzNTbWTs4uyVLvDb0iy2zzkwc2OYzoLHNoqZ+LklYEprRKyeAThpRf8EyPmNkklvHRt+TQ6KUGzJz94lJsenpon+Zyv7J8QkSUzo058lkbi/Qem1uHn1pw8JTMj3DzVUwYBoQcPzngGTHZhcCfB5SNHaOEL76LLmihVd808cerqG84hzfT/PjjXZx2pa4ZkPq2W8HZ1cozKjfpYbXsCI/y3MyqZLneWYIkO2mcDrogo78BLUbIyAOO1yJB9shLPed8oa2Ay0hAtMFbUa9rwIDAQAB
-----END PUBLIC KEY-----
'''
notify_url = 'http://127.0.0.1/reback'

APIPAY = "https://openapi.alipaydev.com/gateway.do?"
DEBUG=True

# 正式上用这个

# BASE_DIR = os.getcwd()
# APPID = '2021002136604704'
# private_key = open(os.path.join(BASE_DIR,'private_key.txt')).read()
# public_key  = open(os.path.join(BASE_DIR,'public_key.txt')).read()
#APIPAY = "https://openapi.alipay.com/gateway.do?"

from alipay import AliPay

import time
# import Response
class test():
    def alipay(self):  # 之前是 pay_result
        ap = AliPay(
            appid=APPID,
            app_notify_url=notify_url,  # 默认回调url
            app_private_key_string=private_key,
            alipay_public_key_string=public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=DEBUG  # 默认False ,若开启则使用沙盒环境的支付宝公钥
        )

        return ap
    def pay(self,ap):

        order_string = ap.api_alipay_trade_page_pay(
            total_amount=9274700,     # 价格
            subject='test pay',     # 主题
            out_trade_no=str(time.time()).replace(',','')   # 订单ID
        )

        pay_url = APIPAY+order_string  # 调用支付宝支付接口

        return pay_url





