from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import generics
from .models import CallBackForm
from .tasks import checkLessons

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


import logging
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradeCreateRequest import AlipayTradeCreateRequest
from alipay.aop.api.response.AlipayTradeCreateResponse import AlipayTradeCreateResponse
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')
class TestPay(APIView):
    def get(self,request):
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
        # alipay_client_config.app_id = '请填写appi_id'
        # alipay_client_config.app_private_key = '请填写开发者私钥去头去尾去回车，单行字符串'
        # alipay_client_config.alipay_public_key = '请填写支付宝公钥，单行字符串'
        client = DefaultAlipayClient(alipay_client_config, logger)
        # 构造请求参数对象
        model = AlipayTradeCreateModel()
        model.out_trade_no = "20150320010101001";
        model.total_amount = "88.88";
        model.subject = "Iphone6 16G";
        model.buyer_id = "2088102177846880";
        request = AlipayTradeCreateRequest(biz_model=model)
        # 执行API调用
        response_content = ''
        try:
            response_content = client.execute(request)
        except Exception as e:
            print(e)
        if not response_content:
            print("failed execute")
        else:
            # 解析响应结果
            response = AlipayTradeCreateResponse()
            response.parse_response_content(response_content)
            # 响应成功的业务处理
            if response.is_success():
                # 如果业务成功，可以通过response属性获取需要的值
                print("get response trade_no:" + response.trade_no)
            # 响应失败的业务处理
            else:
                # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
                print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
