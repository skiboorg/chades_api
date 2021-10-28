# -*- coding: UTF-8 -*-
import base64
import collections
import copy
import json
from datetime import datetime
from urllib import request, parse
import rsa
from alipay import AliPay
import  os

BASE_DIR = os.getcwd()
APPID = '2021002136604704'
# private_key = open(os.path.join(BASE_DIR,'private_key.pem')).read()
# public_key  = open(os.path.join(BASE_DIR,'public_key.pem')).read()
# APPID = '2021000118619554'
private_key = '''
-----BEGIN RSA PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCtflV/V6Fmu44vjNWxxmSgx2+fg8YymO4No3khE8VJ7qR/520xiPpaVc/8AdTF/UBzPYLHw2AwoTm5fXcMkCK1+IPryVXL31xfwF8ITK/lwjapVvSPMIrzc/PCpEBTUE3gi+fMj9mhAPjcCbKRjhjT3MazBuCetu9pQSbUvKZ+O77GLuNvmO36mHbqZ+1w7xTLHETzjKo3mEs9StSQyGopPy0gik77IfV2a/9DHTanZYYr3ZM2/vmgKDoJiRnEa8Y2fuGn5wSKG+gY0vE2oPqMkrNNGY0EKOKjgaqHNg08DK7xMTIEF7qeWMRQLvFCmWAeG5zKkF69PQgTSQHph9SRAgMBAAECggEAaAmOM6LVAsoN5a3Kp6SUy2VNJpbaz5StjDgvdwpoEIGu25RoAoBlwK4c3r4qXeAUOgb02d3rXL4R4429SidU6VJxqX8+l9cFidXOJyf1gw4HwVyHoyY07PDniBz/Bfbt/G1pP14z3zy5/xlBn89aTBHkhY7mO8bvomqTYpcOMDubgSYsVIdFkTZupzNXeltF50IcSiOKTw1ziaslT7zCfgJq9OiFd5kM6b+Xy2HptABBL8NPW/m2XE05PSDL2J3MJE96AnCegulBSaWTJKVwBQtNmuH7wNHqdVnXr7ABZZnVOKLBbFnEprIc/OZi3r4lxYtPTcab38OxiCunShCJwQKBgQD31kcPnZDQlal+I+HC1Auhhel6f6Bt2htIwlc93gRcrigxIT55s1yPbcpFqHiOhaEOhH2+UPQ7Y1qcKaRIn1nivtM3wQ/OLpmC6KsHsirZRLNzOv91URMPMesqtlAb1MTPL6V4iE8sNGaHFxxRpa9AyQ1EdgzAXVGd0M9kklB1HQKBgQCzNTQcFQYy9yjeeXAAXXNHEBiiMdiPhNxHj3dVl3jDLVvevaN4T9UAtbfje5LGeYLgc2pdLRBHH1zWHTdhzGQDFe/joRkGBtQ1sfllqOJItp1JC7iMQXhmgihT7YJ68Uc69kHXqYRV0TbSD6XXXYouUQKj8AD2lbOy7kEg9tzHBQKBgQCneTbfyHvZV6kHQjwGqb+KULFrQ98nHGGfkyPc/LA56L3kJTDQkHGVwn0TATsmJAqngsRt3MqNbyAFsuX+5R+aZ5TXcjC6BSdbHNqmArGNzCzvSwjhP/3/IJ5naHdNt0OfNfU9M+88UdSOqQFL8wgwYSwD/Tm0q9rBKB9dOLoByQKBgD+1EDtTdgq0NsEwJpLapdqDbF5snfIXZz/BTskMug+YlmpOvEhPCQfhkee6zGjmVZJ5NTy+gmTmT1iGtmN8B6nZKJihcoXj85jLFj//k8IJuUx4cDjcJXM7nh6H9rTCBXJ+jNWgG71uTLDMg0ZWqILipa+l6JHAkktvy5NubvoJAoGBAIwZsoS8K07SZQqfZDRIlVVtxnNFymKLR9v9EI5M77qGNSlyi+WuSHpI1pHhfdIyAPKo9buBuiboTNdmpPyQysqKaH/i59t2clDFu3vWFL7qh/Hk2+0LkpRs9VXhvBiP7JzFx6YgJ3qZ7bzgkHQ+EKAxvYBq+qogELwXr1AUsuGS
-----END RSA PRIVATE KEY-----
'''
public_key = '''
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArX5Vf1ehZruOL4zVscZkoMdvn4PGMpjuDaN5IRPFSe6kf+dtMYj6WlXP/AHUxf1Acz2Cx8NgMKE5uX13DJAitfiD68lVy99cX8BfCEyv5cI2qVb0jzCK83PzwqRAU1BN4IvnzI/ZoQD43AmykY4Y09zGswbgnrbvaUEm1Lymfju+xi7jb5jt+ph26mftcO8UyxxE84yqN5hLPUrUkMhqKT8tIIpO+yH1dmv/Qx02p2WGK92TNv75oCg6CYkZxGvGNn7hp+cEihvoGNLxNqD6jJKzTRmNBCjio4GqhzYNPAyu8TEyBBe6nljEUC7xQplgHhucypBevT0IE0kB6YfUkQIDAQAB
-----END PUBLIC KEY-----
# '''
notify_url = 'http://127.0.0.1/reback'
DEBUG=False

class alipay:
    def __init__(self,  charset='gbk', sign_type='RSA2',
                 version='1.0'):
        self.requesturl = 'https://openapi.alipay.com/gateway.do' if DEBUG is False else "https://openapi.alipaydev.com/gateway.do"

        self.private_key = private_key
        self.public_key = public_key
        self.params = dict(app_id=APPID, charset=charset, sign_type=sign_type, version=version,
                           biz_content={}, timestamp='', notify_url=notify_url)

    def _sort(self, params):
        #print(collections.OrderedDict(sorted(dict(params).items(), key=lambda x: x[0])))
        return collections.OrderedDict(sorted(dict(params).items(), key=lambda x: x[0]))

    @staticmethod
    def make_goods_etail(goods_detail=None, alipay_goods_id=None, goods_name=None, quantity=None, price=None,
                         goods_category=None, body=None, show_url=None):
        params = dict(goods_detail=goods_detail, alipay_goods_id=alipay_goods_id, goods_name=goods_name,
                      quantity=quantity, price=price, goods_category=goods_category, body=body, show_url=show_url)
        return dict(filter(lambda x: x[1] is not None, params.items()))

    def _make_sign(self, params, **kwargs):

        private_key = rsa.PrivateKey.load_pkcs1(kwargs.get('private_key', None) or self.private_key)
        # print(self.private_key)
        # breakpoint()
        sign = base64.b64encode(rsa.sign(params.encode(), private_key, "SHA-256")).decode('gbk')

        # print(sign)
        return sign

    def _check_sign(self, message, sign, **kwargs):
        message = self._sort(message)
        data = '{'
        for key, value in message.items():
            data += '"{}":"{}",'.format(key, value)
        data = data[:-1] + '}'
        sign = base64.b64decode(sign)
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(kwargs.get('public_key', None) or self.public_key)

        try:
            rsa.verify(data.encode(), sign, public_key)
            return True
        except Exception as e:
            print("出现如下异常%s" % e)
            return False

    def _make_request(self, params, biz_content, **kwargs):
        buf = ''
        params['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params['biz_content'] = json.dumps(self._sort(biz_content))

        for key, value in kwargs.items():
            params[key] = value
        params = self._sort(params)

        for key in params:
            buf += '{}={}&'.format(key, params[key])

        params['sign'] = self._make_sign(buf[:-1], **kwargs)

        # 发射http请求取回数据
        data = request.urlopen(self.requesturl, data=parse.urlencode(params).encode('gbk')).read().decode('gbk')
       # print(parse.urlencode(params).encode('gbk'))
        return data

    def parse_response(self, params, **kwargs):
        sign = params['sign']
        if self._check_sign(dict(filter(lambda x: 'sign' not in x[0], params.items())), sign, **kwargs):
            return True
        else:
            return False

    def trade_pre_create(self, out_trade_no, total_amount, subject, seller_id=None, discountable_amount=None,
                         undiscountable_amount=None, buyer_logon_id=None, body=None, goods_detail=None,
                         operator_id=None, store_id=None, terminal_id=None, timeout_express='5m', alipay_store_id=None,
                         royalty_info=None, extend_params=None, **kwargs):
        """
        :param out_trade_no:    商户订单号,64个字符以内、只能包含字母、数字、下划线；需保证在商户端不重复.
        :param total_amount:    订单总金额，单位为元，精确到小数点后两位.
        :param subject:         订单标题.
        :param seller_id:       卖家支付宝用户ID。 如果该值为空，则默认为商户签约账号对应的支付宝用户ID.
        :param discountable_amount:可打折金额. 参与优惠计算的金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000]
        :param undiscountable_amount:不可打折金额. 不参与优惠计算的金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000]
        :param buyer_logon_id:      买家支付宝账号
        :param body:                对交易或商品的描述
        :param goods_detail:        订单包含的商品列表信息.使用make_goods_etail生成. 其它说明详见：“商品明细说明”
        :param operator_id:         商户操作员编号
        :param store_id:            商户门店编号
        :param terminal_id:         商户机具终端编号
        :param timeout_express:     该笔订单允许的最晚付款时间，逾期将关闭交易。取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天
        :param alipay_store_id:     支付宝店铺的门店ID
        :param royalty_info:        描述分账信息   暂时无效
        :param extend_params:       业务扩展参数	暂时无效
        :param kwargs:              公共参数可在此处暂时覆盖
        :return:
        """
        params = copy.deepcopy(self.params)
        params['method'] = 'alipay.trade.precreate'
        total_amount = round(int(total_amount), 2)
        if discountable_amount:
            discountable_amount = round(int(discountable_amount), 2)
        if undiscountable_amount:
            undiscountable_amount = round(int(undiscountable_amount), 2)
        if discountable_amount:
            if undiscountable_amount is not None:
                if discountable_amount + undiscountable_amount != total_amount:
                    return '传入打折金额错误'
        biz_content = dict(out_trade_no=out_trade_no[:64], total_amount=total_amount, seller_id=seller_id,
                           subject=subject,
                           discountable_amount=discountable_amount, undiscountable_amount=undiscountable_amount,
                           buyer_logon_id=buyer_logon_id, body=body, goods_detail=goods_detail, operator_id=operator_id,
                           store_id=store_id, terminal_id=terminal_id, timeout_express=timeout_express,
                           alipay_store_id=alipay_store_id, royalty_info=royalty_info, extend_params=extend_params)

        resp = self._make_request(params, dict(filter(lambda x: x[1] is not None, biz_content.items())), **kwargs)

        check = eval(resp)
        resp = json.loads(resp)['alipay_trade_precreate_response']
        #print(check)
        if self._check_sign(check['alipay_trade_precreate_response'], check['sign']):

            return resp
        return False

    def trade_refund(self, refund_amount, out_trade_no=None, trade_no=None,
                     refund_reason=None, out_request_no=None, operator_id=None, store_id=None,
                     terminal_id=None, **kwargs):
        """

        :param refund_amount:   需要退款的金额，该金额不能大于订单金额,单位为元，支持两位小数
        :param out_trade_no:    商户订单号，不可与支付宝交易号同时为空
        :param trade_no:        支付宝交易号，和商户订单号不能同时为空
        :param refund_reason:   退款的原因说明
        :param out_request_no:  标识一次退款请求，同一笔交易多次退款需要保证唯一，如需部分退款，则此参数必传。
        :param operator_id:     商户的操作员编号
        :param store_id:        商户的门店编号
        :param terminal_id:     商户的终端编号
        :param kwargs:          公共参数可在此处临时覆盖
        :return:
        """
        params = copy.deepcopy(self.params)
        params['method'] = 'alipay.trade.refund'
        refund_amount = round(float(refund_amount), 2)

        biz_content = dict(refund_amount=refund_amount, out_trade_no=out_trade_no, trade_no=trade_no,
                           refund_reason=refund_reason, out_request_no=out_request_no, operator_id=operator_id,
                           store_id=store_id, terminal_id=terminal_id)
        resp = self._make_request(params, dict(filter(lambda x: x[1] is not None, biz_content.items())), **kwargs)
        check = eval(resp)
        resp = json.loads(resp)['alipay_trade_refund_response']
        if self._check_sign(check['alipay_trade_refund_response'], check['sign']):
            return int(resp['code']) == 10000
        return False

    def trade_query(self, out_trade_no, trade_no=None, **kwargs):
        params = copy.deepcopy(self.params)
        params['method'] = 'alipay.trade.query'

        biz_content = dict(out_trade_no=out_trade_no, trade_no=trade_no)
        resp = self._make_request(params, dict(filter(lambda x: x[1] is not None, biz_content.items())), **kwargs)
        check = eval(resp)
        resp = json.loads(resp)['alipay_trade_query_response']
        if self._check_sign(check['alipay_trade_query_response'], check['sign']) and resp['code'] == 10000:
            return resp
        return False

    def init_alipay_cfg(self):
        alipay = AliPay(
            appid=APPID,
            app_notify_url=notify_url,  # 默认回调url
            app_private_key_string=private_key,
            alipay_public_key_string=public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=DEBUG  # 默认False ,若开启则使用沙盒环境的支付宝公钥

        )
        return alipay