import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import generics
from .models import CallBackForm
from .tasks import checkLessons
from .pay import do_payment
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

# import os
# import logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(message)s',
#     filemode='a',)
# logger = logging.getLogger('')
#
#
# APPID = '2021002136604704'
# notify_url = 'http://qrlevel.cn/api/v1/shool/pay_notify/'
# APIPAY = "https://openapi.alipaydev.com/gateway.do?"
#
# DEBUG=True
#
# BASE_DIR = os.getcwd()
# # APPID = '2021002136604704'
# private_key = open(os.path.join(BASE_DIR,'private_key.txt')).read()
# public_key  = open(os.path.join(BASE_DIR,'public_key.txt')).read()
# APIPAY = "https://openapi.alipay.com/gateway.do?"
#
# from alipay import AliPay
#
# import time
# # import Response
#
# def alipay():  # 之前是 pay_result
#     ap = AliPay(
#         appid=APPID,
#         app_notify_url=notify_url,  # 默认回调url
#         app_private_key_string=private_key,
#         alipay_public_key_string=public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#         sign_type="RSA2",  # RSA 或者 RSA2
#         debug=DEBUG  # 默认False ,若开启则使用沙盒环境的支付宝公钥
#     )
#
#     return ap
#
# def pay(ap,amount,subject,out_trade_no):
#     order_string = ap.api_alipay_trade_page_pay(
#         total_amount=amount,  # 价格
#         subject=subject,  # 主题
#         out_trade_no=out_trade_no  # 订单ID
#     )
#     pay_url = APIPAY + order_string  # 调用支付宝支付接口
#     return pay_url
#
# class CreatePay(APIView):
#     def post(self,request):
#         print(request.data)
#         period = int(request.data.get('period'))
#         subject = f'User {request.data.get("user_id")} payment {str(time.time()).replace(",", "")}'
#         out_trade_no = f'qrlevel_reg_{period}_user_{request.data.get("user_id")}_{str(time.time()).replace(",", "")}'
#         amount = 0
#
#         if period == 1:
#             amount = 10
#
#         if period == 2:
#             amount = 20
#
#         if period == 3:
#             amount = 30
#
#         ap = alipay()
#         url = pay(ap,amount=amount,subject=subject,out_trade_no=out_trade_no)
#         return Response(url, status=200)
#
# class PayNotify(APIView):
#     def post(self, request):
#         print('post')
#
#         out_trade_no = request.data.get('out_trade_no')
#         trade_status = request.data.get('trade_status')
#         # print(out_trade_no)
#         # print(trade_status)
#         # print(out_trade_no.split('_'))
#         months = int(out_trade_no.split('_')[2])
#         user_id = out_trade_no.split('_')[4]
#         if trade_status == 'TRADE_SUCCESS':
#             user = User.objects.get(id=user_id)
#             # print(user)
#             # print(datetime.today())
#             # print(datetime.today()+ relativedelta(months=months))
#             user.expiry_time = datetime.today()+ relativedelta(months=months)
#             user.save()
#         return Response(status=200)
#
