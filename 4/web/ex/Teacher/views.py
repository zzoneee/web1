from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ex.models import Teacher,Student,Group,Report,TeamEvaluation
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





class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # username = request.GET['username']
            # password = request.GET['password']
            username = request.data.get('username')
            password = request.data.get('password')
            user = Teacher.objects.filter(id=username).first()
            if not user:
                return Response({
                    'status': 404,
                    'msg': '账号或密码不正确'
                })
            if check_password(password, user.password):
                # payload = {'id': "admin1","username": "admin1"}
                token = create_token({
                    'id': user.id,
                    "username": username
                })
                # print("555" + token)
                data = {
                    'tea_id': user.id,
                    'Authorization': token
                }
                return Response({
                    'status': 200,
                    'msg': '登录成功',
                    'data': data
                })
            else:
                return Response({
                    'status': 404,
                    'msg': '账号或密码不正确'
                })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class ClassMessageView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # 获取token
            # token = request.META.get('HTTP_AUTHORIZATION')
            # 解析token 得到当前用户id
            # get_user_id(token)
            # tea_id = get_user_id(token)
            # print(tea_id)

            try:
                # print(JwtQueryParamAuthentication.authenticate(self, request))
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                # print(payload["id"])
            except Exception as e:
                # print(e.args)
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })

            data_list = []
            for item in Student.objects.all():
                # print(item.group_id)
                if item.group_id == "" or item.group_id == None:
                    group_name = ""
                    role = ""
                else:
                    group_name = Group.objects.filter(id=item.group_id).first().name
                    role = item.role
                # group_name = ""
                # role = ""
                data = {'college': item.college,
                        'class_name': item.class_name,
                        'stu_num': item.stu_num,
                        'name': item.name,
                        'phone': item.phone,
                        'group': group_name,
                        'role': role}
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

class studentMessageReportView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data_list = []
            for item in Student.objects.all():
                data = {'college': item.college,
                        'class_ID': item.class_name,
                        'stu_num': item.stu_num,
                        'stu_name': item.name,
                        'group': Group.objects.filter(id=item.group_id).first().name,
                        'role': item.role}
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

class teacherMessageView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            tea_userId = request.GET['tea_userId']
            user = Teacher.objects.filter(id=tea_userId).first()
            data = {
                'id': user.id,
                'name': user.name,
                'college': user.college,
                'phone': user.phone
            }
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

class editTeacherMessageView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            tea_userId = request.data.get('id')
            user = Teacher.objects.filter(id=tea_userId).first()
            user.name = request.data.get('name')
            user.college = request.data.get('college')
            user.phone = request.data.get('phone')
            user.save()
            return Response({
                'status': 200,
                'msg': '修改成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class editPwdView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            userId = request.data.get('userId')
            old_password = request.data.get('oldPassword')
            new_password = request.data.get('editPassword')
            user = Teacher.objects.filter(id=userId).first()
            if check_password(old_password, user.password):
                user.password = make_password(new_password)
                user.save()
                return Response({
                    'status': 200,
                    'msg': '修改成功'
                })
            else:
                return Response({
                    'status': 404,
                    'msg': '原密码不正确'
                })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class addTeacherView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id')
            password = make_password(request.data.get('password'))
            name = request.data.get('name')
            college = request.data.get('college')
            phone = request.data.get('phone')
            user = Teacher(id=id,password=password,name=name,college=college,phone=phone)
            user.save()
            return Response({
                'status': 200,
                'msg': '修改成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class teacherIDExistView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            username = request.GET['tea_userId']
            user = Teacher.objects.filter(id=username).first()
            if not user:
                return Response({
                    'status': 200,
                    'msg': '账号未注册'
                })
            else:
                return Response({
                    'status': 400,
                    'msg': '账号已注册'
                })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class stuNumExistView(APIView):
    def get(self, request, *args, **kwargs):
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

            username = request.GET['stuNum']
            user = Student.objects.filter(stu_num=username).first()
            if not user:
                return Response({
                    'status': 200,
                    'msg': '账号未注册'
                })
            else:
                return Response({
                    'status': 400,
                    'msg': '账号已注册'
                })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class getGroupListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data_list = []
            for item in Group.objects.all():
                user = Student.objects.filter(group_id=item.id).first()
                if user:
                    data = {'name': item.name}
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

class getGroupListDetailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            OP = request.GET['OP']
            data_list = []
            for item in Group.objects.all():
                user = Student.objects.filter(group_id=item.id).first()
                if user:
                    stu_nameString = ''
                    flag = True
                    for item2 in Student.objects.filter(group_id=item.id):
                        if not flag:
                            stu_nameString += '，'
                        stu_nameString += item2.name
                        if flag:
                            flag = False
                    
                    hasReport = 0
                    id = request.GET['id']
                    report = Report.objects.filter(Q(experiment_id=id) & Q(owner_id=item.id))
                    if report:
                        hasReport = 1

                    data = {'name': item.name, 'stu_nameString': stu_nameString, 'hasReport': hasReport}
                    if OP == '0' or OP == '1' and hasReport == 0 or OP == '2' and hasReport == 1:
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

class addStudentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            stu_num = request.data.get('stu_num')
            password = make_password(request.data.get('password'))
            name = request.data.get('name')
            college = request.data.get('college')
            phone = request.data.get('phone')
            role = request.data.get('role')
            groupName = request.data.get('groupName')
            class_name = request.data.get('class_name')
            if groupName == '':
                user = Student(stu_num=stu_num,password=password,name=name,college=college,phone=phone,class_name=class_name)
            else:
                group_id = Group.objects.filter(name=groupName).first().id
                user = Student(stu_num=stu_num,password=password,name=name,college=college,phone=phone,role=role,group_id=group_id,class_name=class_name)
            user.save()
            return Response({
                'status': 200,
                'msg': '修改成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class updateStuMsgView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('stu_num')
            user = Student.objects.filter(stu_num=username).first()
            user.college = request.data.get('college')
            user.class_name = request.data.get('class_name')
            user.name = request.data.get('name')
            user.phone = request.data.get('phone')
            groupName = request.data.get('groupName')
            if groupName != '' and groupName != None:
                user.group_id = Group.objects.filter(name=request.data.get('groupName')).first().id
                user.role = request.data.get('role')
            else:
                user.group_id = None
                user.role = None
            user.save()
            return Response({
                'status': 200,
                'msg': '修改成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class deleteStuView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('stu_num')
            user = Student.objects.filter(stu_num=username).first()
            user.delete()
            return Response({
                'status': 200,
                'msg': '删除成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class resetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('stu_num')
            user = Student.objects.filter(stu_num=username).first()
            user.password = make_password('123456')
            user.save()
            return Response({
                'status': 200,
                'msg': '重置密码成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class groupNumberDetailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            groupName = request.GET['groupName']
            group_id = Group.objects.filter(name=groupName).first().id
            data_list = []
            for item in Student.objects.all():
                if group_id == item.group_id:
                    data = {'college': item.college,
                            'class_name': item.class_name,
                            'stu_num': item.stu_num,
                            'name': item.name,
                            'phone': item.phone,
                            'group': Group.objects.filter(id=item.group_id).first().name,
                            'role': item.role}
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

class reportDetailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            group_name = request.GET['groupName']
            ex_id = request.GET['reportNum']
            # print(group_name, ex_id)
            group_id = Group.objects.filter(name=group_name).first().id
            data_list = []
            for item in Report.objects.filter(Q(owner_id=group_id) & Q(experiment_id=ex_id)):
                hp_score = 0
                hp_num = 0
                for item2 in TeamEvaluation.objects.all():
                    if item2.Ratee_ID == item.id:
                        hp_num += 1
                        hp_score += item2.score
                if hp_num == 0:
                    hp_score = -1
                else:
                    hp_score //= hp_num
                
                data = {'id': item.id,
                        'create_time': item.create_time.strftime('%Y-%m-%d'),
                        'system_score': item.system_score,
                        'hp_score': hp_score,
                        'url': item.url,
                        'teacher_score': item.teacher_score}
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

class teaReportMarkView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            userId = request.data.get('userId')
            id = request.data.get('id')
            score = request.data.get('score')
            report = Report.objects.filter(id=id).first()

            report.teacher_score = score
            report.save()
            return Response({
                "status": 200,
                "msg": '评分成功',
            })

        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class getReportUrlView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            id = request.GET['id']
            url = Report.objects.filter(id=id).first().url
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': url
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class deleteReportView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id')
            report = Report.objects.filter(id=id).first()
            

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
            length = len(base_dir)
            for i in range(length - 2,0,-1):
                if base_dir[i] == '\\':
                    base_dir = base_dir[0:i]
                    break
            file_path = os.path.join(base_dir, 'static','report', report.url)  # 下载文件的绝对路径

            # print(file_path)

            if os.path.isfile(file_path):  # 判断下载文件是否存在
                os.remove(file_path)
            
            report.delete()
            
            return Response({
                'status': 200,
                'msg': '删除成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class importExcelView(APIView):
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

            insertData = request.data.get('insertData')
            insertData_len = len(insertData)
            # print(insertData[1]['name'])
            for i in range(0,insertData_len):
                stu_num = insertData[i]['stu_num']
                password = make_password("123456")
                name = insertData[i]['name']
                college = insertData[i]['college']
                phone = insertData[i]['phone']
                role = insertData[i]['role']
                groupName = insertData[i]['group']
                class_name = insertData[i]['class_name']
                user = Student.objects.filter(stu_num=stu_num).first()
                if not user:
                    if groupName == '' or groupName == None:
                        user = Student(stu_num=stu_num,password=password,name=name,college=college,phone=phone,class_name=class_name)
                    else:
                        group_id = Group.objects.filter(name=groupName).first().id
                        user = Student(stu_num=stu_num,password=password,name=name,college=college,phone=phone,role=role,group_id=group_id,class_name=class_name)
                    user.save()

            return Response({
                'status': 200,
                'msg': '批量导入成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

# stu_num = request.data.get('stu_num')
#             password = make_password(request.data.get('password'))
#             name = request.data.get('name')
#             college = request.data.get('college')
#             phone = request.data.get('phone')
#             role = request.data.get('role')
#             groupName = request.data.get('groupName')
#             class_name = request.data.get('class_name')
#             if groupName == '':
#                 user = Student(stu_num=stu_num,password=password,name=name,college=college,phone=phone,class_name=class_name)
#             else:
#                 group_id = Group.objects.filter(name=groupName).first().id
#                 user = Student(stu_num=stu_num,password=password,name=name,college=college,phone=phone,role=role,group_id=group_id,class_name=class_name)
#             user.save()