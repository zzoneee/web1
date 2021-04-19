from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ex.models import experiment, Student, Report
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

class exListsView(APIView):
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
            # print(user_id)
            data_list = []

            for item in experiment.objects.all():
                active = 0
                if type(user_id) == int:
                    student = Student.objects.filter(id=user_id).first()
                    group_id = student.group_id
                    report = Report.objects.filter(Q(owner_id=group_id)&Q(experiment_id=item.id)).first()
                    if report:
                        active = 1
                        if report.teacher_score != -1:
                            active = 2
                data = {'id': item.id,
                        'name': item.name,
                        'url': item.url,
                        'introduction': item.introduction,
                        'introductionUrl': item.introductionUrl,
                        'active': active,
                }
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

class addExView(APIView):
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

            name = request.data.get('name')
            url = request.data.get('url')
            introduction = request.data.get('introduction')
            introductionUrl = request.data.get('introductionUrl')
            
            ex = experiment(name=name,url=url,introduction=introduction,introductionUrl=introductionUrl)
            ex.save()
            
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

class deleteExView(APIView):
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

            id = request.data.get('id')
            
            ex = experiment.objects.filter(id=id).first()
            ex.delete()
            
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

class getExNameView(APIView):
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

            ex_id = request.GET['ex_id']

            ex_name = experiment.objects.filter(id=ex_id).first().name

            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': ex_name
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })
