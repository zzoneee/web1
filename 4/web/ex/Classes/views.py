from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ex.models import Teacher,Student,Group,Report,TeamEvaluation,Notice,TeacherNewNotice,StudentNewNotice, Classes
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

class classesListsView(APIView):
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

            for item in Classes.objects.all():
                data = {'id': item.id,
                        'name': item.name}
                data_list.append(data)
            
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data_list
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class classesInfoView(APIView):
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

            for item in Classes.objects.all():
                class_amount = 0
                for item2 in Student.objects.all():
                    if item2.class_name == item.name:
                        class_amount += 1
                data = {'id': item.id,
                        'class_name': item.name,
                        'college': item.college,
                        'class_amount': class_amount}
                data_list.append(data)
            
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data_list
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class classesExistView(APIView):
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
            class_name = request.GET['class_name']

            classes = Classes.objects.filter(name=class_name).first()
            data = '0'
            if classes:
                data = '1'

            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class addClassView(APIView):
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

            user_id = payload['id']
            class_name = request.data.get('class_name')
            college = request.data.get('college')

            classes = Classes(name=class_name,college=college)
            classes.save()

            return Response({
                'status': 200,
                'msg': '返回成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class deleteClassView(APIView):
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

            user_id = payload['id']
            classMsg = request.data.get('classMsg')

            # print(classMsg)
            for item in classMsg:
                classes = Classes.objects.filter(id=item['id']).first()
                classes.delete()

                # print(item)

                for item2 in Student.objects.filter(class_name=item['class_name']):
                    item2.delete()

            return Response({
                'status': 200,
                'msg': '返回成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })
