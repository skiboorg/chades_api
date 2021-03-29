from chades_api.celery import app
from .models import *

@app.task
def checkLessons():
    print('checkLessons')
    users = User.objects.all()
    courses = Course.objects.all()
    cur_course = 0
    for course in courses:
        for user in users:
            lessons = AvaiableLessons.objects.filter(course=course,user=user)
            # print('course',course)
            # print('user',user)
            # print(lessons)
            for lesson in lessons:
                if lesson.status == 0:
                    lesson.status = 1
                    lesson.save()
                    break
