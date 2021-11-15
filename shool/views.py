from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import generics
from .models import CallBackForm
from .tasks import checkLessons
from .pay import do_payment

import settings

class LessonDone(APIView):
    def post(self, request):
        print(request.data['lesson_id'])
        lesson_id = request.data['lesson_id']
        lesson = AvaiableLessons.objects.get(id=lesson_id)
        lesson.status = 2
        lesson.save()
        course = Course.objects.get(id=lesson.course.id)
        # print(course)
        course_finished_lessons = AvaiableLessons.objects.filter(user=request.user,course=course,status=2)
        print('course_lessons', course.lessons.all().count())
        print('course_finished_lessons', course_finished_lessons.count())
        if (course.lessons.all().count() == course_finished_lessons.count()):
            next_cource = Course.objects.get(depence=course)
            request.user.finished_courses.add(course)
            request.user.avaiable_courses.add(next_cource)
            request.user.progress_courses.remove(course)
            request.user.score += course.points_to_balance
            request.user.save()
            return Response(status=201)
        else:
            return Response(status=200)


class NewCB(APIView):
    def post(self,request):
        CallBackForm.objects.create(
            name=request.data['name'],
            email=request.data['email'],
            text=request.data['text'])
        return Response(status=200)


class CourseOpen(APIView):
    def post(self,request):
        checkLessons = AvaiableLessons.objects.filter(user=request.user,course_id=request.data['course'])

        if not checkLessons.exists():
            # print(request.data)
            course = Course.objects.get(id=request.data['course'])
            request.user.progress_courses.add(course)
            # print(course)
            lessons = course.lessons.all()
            # print(lessons)
            x = 0
            for lesson in lessons:
                AvaiableLessons.objects.create(user=request.user,
                                               course=course,
                                               lesson=lesson,
                                               status=1 if x == 0 else 0)
                x += 1
            return Response(status=201)
        else:
            allCourceLessons = Course.objects.get(id=request.data['course'])
            print('allCourceLessons.count()', allCourceLessons.lessons.all().count())
            print('checkLessons.count()', checkLessons.count())
            for lesson in allCourceLessons.lessons.all():
                if checkLessons.filter(lesson=lesson).exists():
                    print('in')
                else:
                    print('not')
                    AvaiableLessons.objects.create(user=request.user,
                                               course=lesson.course,
                                               lesson=lesson,
                                               status=0)
        return Response(status=200)


class GetStages(generics.ListAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer


class GetCourses(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CoursesSerializer


class GetCourse(generics.RetrieveAPIView):
    queryset = Course.objects.filter()
    serializer_class = CourseSerializer


class GetAvaiableLessons(generics.ListAPIView):
    serializer_class = AvaiableLessonsSerializer

    def get_queryset(self):
        lessons = AvaiableLessons.objects.filter(user_id=self.request.query_params.get('user_id'),
                                                 course_id=self.request.query_params.get('course_id')
                                                 )
        return lessons


class GetLessons(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class GetTests(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class GetBanner(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class GetTestChoices(generics.ListAPIView):
    queryset = TestChoice.objects.all()
    serializer_class = TestChoiceSerializer


class StartScript(APIView):
    def get(self,request):
        checkLessons.delay()

        return Response(status=200)


class GetInputTests(generics.ListAPIView):
    GetInputTests = InputTest.objects.all()
    serializer_class = InputTestSerializer

# import logging
# from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
# from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
# from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
# from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
# from alipay.aop.api.domain.SettleInfo import SettleInfo
# from alipay.aop.api.domain.SubMerchant import SubMerchant
# from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
#
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(message)s',
#     filemode='a',)
# logger = logging.getLogger('')
#
#
# class TestPay(APIView):
#
#     def get(self,request):
#         alipay_client_config = AlipayClientConfig()
#         alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
#         alipay_client_config.app_id = settings.APP_ID
#         alipay_client_config.app_private_key = settings.private_key
#         alipay_client_config.alipay_public_key = settings.public_key
#         alipay_client_config.sign_type = 'RSA2'
#
#         client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
#
#         model = AlipayTradePagePayModel()
#         model.out_trade_no = "pay201805020000226"
#         model.total_amount = 1.00
#         model.subject = "测试"
#         model.body = "支付宝测试"
#         model.product_code = "FAST_INSTANT_TRADE_PAY"
#         request = AlipayTradePagePayRequest(biz_model=model)
#         response = client.page_execute(request, http_method="GET")
#         print("alipay.trade.page.pay response:" + response)
#
#         return Response(response,status=200)


from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig
import os
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


APPID = '2021002136604704'
# private_key = '''
# -----BEGIN RSA PRIVATE KEY-----
# MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCYXEPPGnZg585QK6FH5ARBUvd8Xfa0FlY2bx80chzD2L6+VBAZTHAxmzx8osLi/TPkutUamdchbBgWbKtkVxhvGSim7WLg803CsJfdaposcWc93n/8NYNeDrsdbH4Y/njtMRYKUNV6QwPexo3gKWLNKMXtcPX2pupj7nAHJj0Gd87HRl+OUu9/PwCb16JwREFXW2GnAow6HP1EaAMN00fh2zVzFowo1BWyZj1btq2YeniwzbJ/oN5sEtq8mx9cpC89q5SyTbwjiJbwchJEeU4MQ6LIJH6RR76s4yNOdHMyk3nSKLTfXssPk45E8bChd9A9Wy4oxZsK0MxcUVMEKBlBAgMBAAECggEBAIPPvrJb2HI52VmuhVdmwu+o0Yd820Qt1uQ8+qgq2QvuZgbPPyZD5QRloszJGwW5vL1zjY337hByLdyooxap6u+iunLACL1IgMugb6IU6dDtQz5ZUixmN4KWB/eKtwT0krXRs5m1GRsvAxgmevOlml6XmbSz93cuLLXLwIvO3xjKDgEHHVsXJkgGNvAs1yQsFmtX5bFtFpaocR2Q7dTriT5bKVJ3ZFtJoh8kFQKZ6w9FQjlEjY/+n/G4Y2kOdGS2NP/y/qkLe3riTFxmU1iA5vv+hGT+ExQDHjcpqY6ZXHfgCY81FZ1PAWtcdlF85qYXUf9LLxSf7QKG0n2pUd+CXukCgYEA7nU+x8WsXwJJK6xuuvpoGg/1SPI+DJyM9cbiZDT3ZV2WEaWfqFIOVyETc5kXXyQzeBeltNuDYohSwjfHVRCItX415PcgLuPtgSDSCXC5QQgV9Rd8z4laYxrQHxTYRQcP0Z/UHUMXKQ2RyanXjbUSAgr6H1Gt/KiyT/XCKdhdBV8CgYEAo5GWwe+yBIWuanK4a0VoKBN9wE/Cl9FdY2szA5b+qOdihFH0KeSZDl1s4pA6oRErGdqINsOoPBtpYbiSUGIKChQXesb9Kj9j2/pTijpFJEiKQV+yPWStL/ZGaeoA+xR5x8m6xDD4TrFQC0lINVmMDGK9dp4GdnehSQZqGkIfxV8CgYAXWiAFzFPvEfg8cKx/Xxpmwv1QYXi2H3amcw2kppM7uAiEPeX+w9pnqfOPtIRXauIndplhtsWNFrCUGIZKzE23CF8axyC9ttCBfsdS6VkbB0GvONeeM2NIpU2QXag4SlLAQpixLOrNuGh4iUt0szDKRmzsOEGDprmfnv+evXOOnQKBgGzNiWTT1qyfZ9ezG+1vK8uMu5dS9vQZ9m8Nfc+jfx5HXAb8pNfBEfa2Opmyqu09CFiYPwd+usfQzBaOufTyYg82MjAfcYPKytgm+a7298sc3aqCx4ODFpjSzx/g4mohwqgdDjk3AdUGqWH4iynBuSD8BV+D2nSvOv/iXm29EnktAoGARkQuyNQe9krg+T9LfVYEoLSVvyBcU2DwpHq0VfUJZ6D1OBdL91hjrFvg9pDJ7Q77u91dnDs3HRr+IdTktc8ADr6/Fx1iOhy3BiYj9xSkdpNW4n3sQkHkn9/K5qG9kdIIDvfXIIjPZvpjF0D2cife9eRKUbJz9fis2v54eouNnoY=
# -----END RSA PRIVATE KEY-----
# '''
# public_key = '''
# -----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhDM9ADCcOG64I07E58i8+lJtHt6AgDRdmSPEK3O8BBWnOADZI4zaMTbVkKg6/Q7qc7h6c8QCV7RTGxN2yvi4NXjykZYtvpHNFoCCUE8sFaZogav8rUmWUxqtkSgyvbQaE+++oCmgDyDITSO9j9ol56E0SAutdmFRPPMM6GHUUBM8af3mTXGT0Fy/OMREPFLTiKJ/JfCLx4ZCQBYzJMaUD7XYaLVYoLBW+X6nBJFIL8rnxebChXR3h7G+ucPrDK6HobGPtInNILP4xN/SG7p8NAJByo3dMaW2fmgLnZgUqW6OGbq0vSX/UxHpUVjK4trKB0PadduFk3+dZj10WhODVQIDAQAB
# -----END PUBLIC KEY-----
# '''
notify_url = 'http://qrlevel.cn/api/v1/shool/pay_notify'

APIPAY = "https://openapi.alipaydev.com/gateway.do?"
DEBUG=True

# 正式上用这个


BASE_DIR = os.getcwd()
# APPID = '2021002136604704'
private_key = open(os.path.join(BASE_DIR,'private_key.txt')).read()
public_key  = open(os.path.join(BASE_DIR,'public_key.txt')).read()
APIPAY = "https://openapi.alipay.com/gateway.do?"

from alipay import AliPay

import time
# import Response

def alipay():  # 之前是 pay_result
    ap = AliPay(
        appid=APPID,
        app_notify_url=notify_url,  # 默认回调url

        app_private_key_string=private_key,
        alipay_public_key_string=public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=DEBUG  # 默认False ,若开启则使用沙盒环境的支付宝公钥
    )

    return ap

def pay(ap):
    order_string = ap.api_alipay_trade_page_pay(
        total_amount=10,  # 价格
        subject='test pay',  # 主题
        out_trade_no=str(time.time()).replace(',', '')  # 订单ID
    )

    pay_url = APIPAY + order_string  # 调用支付宝支付接口

    return pay_url

class TestPay(APIView):

    def get(self,request):
       #do_payment()
       ap = alipay()
       url = pay(ap)
       print(url)

class PayNotify(APIView):
    def get(self,request):
        print('get')
        print(self.request.query_params)
        return Response(status=200)

    def post(self, request):
        print('post')
        print(request.data)
        return Response(status=200)
