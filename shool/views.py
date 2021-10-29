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
#         alipay_client_config.app_private_key = settings.API_PRIVATE_KEY
#         alipay_client_config.alipay_public_key = settings.API_PUBLIC_KEY
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

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


APPID = '2021002136604704'
private_key = '''
-----BEGIN RSA PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCtflV/V6Fmu44vjNWxxmSgx2+fg8YymO4No3khE8VJ7qR/520xiPpaVc/8AdTF/UBzPYLHw2AwoTm5fXcMkCK1+IPryVXL31xfwF8ITK/lwjapVvSPMIrzc/PCpEBTUE3gi+fMj9mhAPjcCbKRjhjT3MazBuCetu9pQSbUvKZ+O77GLuNvmO36mHbqZ+1w7xTLHETzjKo3mEs9StSQyGopPy0gik77IfV2a/9DHTanZYYr3ZM2/vmgKDoJiRnEa8Y2fuGn5wSKG+gY0vE2oPqMkrNNGY0EKOKjgaqHNg08DK7xMTIEF7qeWMRQLvFCmWAeG5zKkF69PQgTSQHph9SRAgMBAAECggEAaAmOM6LVAsoN5a3Kp6SUy2VNJpbaz5StjDgvdwpoEIGu25RoAoBlwK4c3r4qXeAUOgb02d3rXL4R4429SidU6VJxqX8+l9cFidXOJyf1gw4HwVyHoyY07PDniBz/Bfbt/G1pP14z3zy5/xlBn89aTBHkhY7mO8bvomqTYpcOMDubgSYsVIdFkTZupzNXeltF50IcSiOKTw1ziaslT7zCfgJq9OiFd5kM6b+Xy2HptABBL8NPW/m2XE05PSDL2J3MJE96AnCegulBSaWTJKVwBQtNmuH7wNHqdVnXr7ABZZnVOKLBbFnEprIc/OZi3r4lxYtPTcab38OxiCunShCJwQKBgQD31kcPnZDQlal+I+HC1Auhhel6f6Bt2htIwlc93gRcrigxIT55s1yPbcpFqHiOhaEOhH2+UPQ7Y1qcKaRIn1nivtM3wQ/OLpmC6KsHsirZRLNzOv91URMPMesqtlAb1MTPL6V4iE8sNGaHFxxRpa9AyQ1EdgzAXVGd0M9kklB1HQKBgQCzNTQcFQYy9yjeeXAAXXNHEBiiMdiPhNxHj3dVl3jDLVvevaN4T9UAtbfje5LGeYLgc2pdLRBHH1zWHTdhzGQDFe/joRkGBtQ1sfllqOJItp1JC7iMQXhmgihT7YJ68Uc69kHXqYRV0TbSD6XXXYouUQKj8AD2lbOy7kEg9tzHBQKBgQCneTbfyHvZV6kHQjwGqb+KULFrQ98nHGGfkyPc/LA56L3kJTDQkHGVwn0TATsmJAqngsRt3MqNbyAFsuX+5R+aZ5TXcjC6BSdbHNqmArGNzCzvSwjhP/3/IJ5naHdNt0OfNfU9M+88UdSOqQFL8wgwYSwD/Tm0q9rBKB9dOLoByQKBgD+1EDtTdgq0NsEwJpLapdqDbF5snfIXZz/BTskMug+YlmpOvEhPCQfhkee6zGjmVZJ5NTy+gmTmT1iGtmN8B6nZKJihcoXj85jLFj//k8IJuUx4cDjcJXM7nh6H9rTCBXJ+jNWgG71uTLDMg0ZWqILipa+l6JHAkktvy5NubvoJAoGBAIwZsoS8K07SZQqfZDRIlVVtxnNFymKLR9v9EI5M77qGNSlyi+WuSHpI1pHhfdIyAPKo9buBuiboTNdmpPyQysqKaH/i59t2clDFu3vWFL7qh/Hk2+0LkpRs9VXhvBiP7JzFx6YgJ3qZ7bzgkHQ+EKAxvYBq+qogELwXr1AUsuGS
-----END RSA PRIVATE KEY-----
'''
public_key = '''
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArX5Vf1ehZruOL4zVscZkoMdvn4PGMpjuDaN5IRPFSe6kf+dtMYj6WlXP/AHUxf1Acz2Cx8NgMKE5uX13DJAitfiD68lVy99cX8BfCEyv5cI2qVb0jzCK83PzwqRAU1BN4IvnzI/ZoQD43AmykY4Y09zGswbgnrbvaUEm1Lymfju+xi7jb5jt+ph26mftcO8UyxxE84yqN5hLPUrUkMhqKT8tIIpO+yH1dmv/Qx02p2WGK92TNv75oCg6CYkZxGvGNn7hp+cEihvoGNLxNqD6jJKzTRmNBCjio4GqhzYNPAyu8TEyBBe6nljEUC7xQplgHhucypBevT0IE0kB6YfUkQIDAQAB
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
        total_amount=9274700,  # 价格
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

