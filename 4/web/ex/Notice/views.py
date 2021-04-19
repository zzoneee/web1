from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ex.models import Teacher,Student,Group,Report,TeamEvaluation,Notice,TeacherNewNotice,StudentNewNotice
from django.core import serializers


from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
# from plane.models import User, Student, LightList, Light, Score, Visit
# from plane.utils.jwt_auth import create_token, get_user_id
# from django.contrib.auth.hashers import make_password, check_password

# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate

import os

from ex.utils.jwt_auth import create_token, get_user_id

from ex.utils.extensions.auth import JwtQueryParamAuthentication

from django.db.models import Q

# Create your views here.

class releaseNoticeView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            try:
                # print(JwtQueryParamAuthentication.authenticate(self, request))
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                # print(payload["id"])
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })

            user_id = payload['id']
            title = request.data.get('title')
            message = request.data.get('message')
            if request.data.get('top'):
                top = 1
            else:
                top = 0
            notice = Notice(title=title,message=message,user_id=user_id,top=top)
            notice.save()

            return Response({
                'status': 200,
                'msg': '发布公告成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class noticeListsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })

            user_id = payload['id']
            
            data_list = []

            for item in Notice.objects.all():
                if item.top == 0:
                    isnew = 0
                    teacherNewNotice = TeacherNewNotice.objects.filter(Q(notice_id=item.id) & Q(teacher_id=user_id)).first()
                    if not teacherNewNotice:
                        teacherNewNotice2 = TeacherNewNotice(notice_id=item.id,teacher_id=user_id,new=0)
                        teacherNewNotice2.save()
                        isnew = 1
                    data = {'id': item.id,
                            'title': item.title,
                            'message': item.message,
                            'time': item.time.strftime('%Y-%m-%d %H:%M:%S'),
                            'top': item.top,
                            'user_id': item.user_id,
                            'new': isnew}
                    data_list.append(data)

            for item in Notice.objects.all():
                if item.top == 1:
                    isnew = 0
                    teacherNewNotice = TeacherNewNotice.objects.filter(Q(notice_id=item.id) & Q(teacher_id=user_id)).first()
                    if not teacherNewNotice:
                        teacherNewNotice2 = TeacherNewNotice(notice_id=item.id,teacher_id=user_id,new=0)
                        teacherNewNotice2.save()
                        isnew = 1
                    data = {'id': item.id,
                            'title': item.title,
                            'message': item.message,
                            'time': item.time.strftime('%Y-%m-%d %H:%M:%S'),
                            'top': item.top,
                            'user_id': item.user_id,
                            'new': isnew}
                    data_list.append(data)

            data_list2 = data_list[::-1]
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data_list2
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class deleteNoticeView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })

            id = request.data.get('id')
            notice = Notice.objects.filter(id=id).first()
            notice.delete()

            return Response({
                'status': 200,
                'msg': '删除公告成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class topNoticeView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })

            id = request.data.get('id')
            notice = Notice.objects.filter(id=id).first()
            notice.top = 1
            notice.save()

            return Response({
                'status': 200,
                'msg': '删除公告成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class noTopNoticeView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })

            id = request.data.get('id')
            notice = Notice.objects.filter(id=id).first()
            notice.top = 0
            notice.save()

            return Response({
                'status': 200,
                'msg': '删除公告成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class editNoticeView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })

            id = request.data.get('id')
            title = request.data.get('title')
            message = request.data.get('message')
            notice = Notice.objects.filter(id=id).first()
            notice.title = title
            notice.message = message
            notice.save()

            return Response({
                'status': 200,
                'msg': '删除公告成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class stuNoticeListsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })

            user_id = payload['id']
            username = payload['username']
            # print(user_id,username)
            data_list = []
            
            for item in Notice.objects.all():
                if item.top == 0:
                    isnew = 0
                    studentNewNotice = StudentNewNotice.objects.filter(Q(notice_id=item.id) & Q(student_id=user_id)).first()
                    if not studentNewNotice:
                        studentNewNotice2 = StudentNewNotice(notice_id=item.id,student_id=user_id,new=0)
                        studentNewNotice2.save()
                        isnew = 1
                    data = {'id': item.id,
                            'title': item.title,
                            'message': item.message,
                            'time': item.time.strftime('%Y-%m-%d %H:%M:%S'),
                            'top': item.top,
                            'user_id': item.user_id,
                            'new': isnew}
                    data_list.append(data)

            for item in Notice.objects.all():
                # print(item.id)
                if item.top == 1:
                    isnew = 0
                    studentNewNotice = StudentNewNotice.objects.filter(Q(notice_id=item.id) & Q(student_id=user_id)).first()
                    if not studentNewNotice:
                        studentNewNotice2 = StudentNewNotice(notice_id=item.id,student_id=user_id,new=0)
                        studentNewNotice2.save()
                        isnew = 1
                    data = {'id': item.id,
                            'title': item.title,
                            'message': item.message,
                            'time': item.time.strftime('%Y-%m-%d %H:%M:%S'),
                            'top': item.top,
                            'user_id': item.user_id,
                            'new': isnew}
                    data_list.append(data)

            data_list2 = data_list[::-1]
            # print(data_list)
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data_list2
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })
