from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ex.models import Student,Group,loginRecord
from django.core import serializers


from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
# from plane.models import User, Student, LightList, Light, Score, Visit
# from plane.utils.jwt_auth import create_token, get_user_id
# from django.contrib.auth.hashers import make_password, check_password

from ex.utils.jwt_auth import create_token, get_user_id

from ex.utils.extensions.auth import JwtQueryParamAuthentication

# Create your views here.



# def login(request):
#     # db = Student.objects.all()

# 	# return JsonResponse({'res':db[0].stu_num})
#     json = serializers.serialize("json",Student.objects.all())
#     return JsonResponse({'res':json})

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = Student.objects.filter(stu_num=username).first()
            if not user:
                return Response({
                    'status': 404,
                    'msg': '账号或密码不正确'
                })
            if check_password(password, user.password):
                token = create_token({
                    'id': user.id,
                    "username": username
                })
                data = {
                    'id': user.stu_num,
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


class EditPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            userId = request.data.get('userId')
            old_password = request.data.get('oldPassword')
            new_password = request.data.get('editPassword')
            user = Student.objects.filter(stu_num=userId).first()
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
            
            # return Response({
            #     'status': 404,
            #     'msg': '原密码不正确'
            # })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class GetGroupInfoView(APIView):
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

            # token = request.META.get('HTTP_AUTHORIZATION')
            # username = get_user_id(token)
            # user = User.objects.filter(id=id).first()
            userId = request.data.get('userId')
            user = Student.objects.filter(stu_num=userId).first()
            groupId = user.group_id
            group = Group.objects.filter(id=groupId).first()

            users = Student.objects.filter(group_id=groupId).all()
            users_json = serializers.serialize("json",users)
            # users_json = [i.pk for i in users]

            # JSONArray newjsonArray = new JSONArray()
            # if (jsonArray != null && jsonArray.size() > 10) {
            #     for (int i = 0; i < 10; i++) {
            #         newjsonArray.add(jsonArray.get(i));
            #     }
            #     return newjsonArray;
            # }
            # return jsonArray;

            # for i in users_json:
            #     print(i)

            # li = []
            # li.append({'aa':'111'})
            # li.append({'bbb':'1161'})
            # print(li)

            # qq = users_json
            # qqq = json.loads(qq)
            # print(li)

            data = {
                # 'username': user.username,
                # 'group_name': user.name,
                'group_name': group.name,
                'users': users_json
            }

            return Response({
                'status': 200,
                'msg': '信息返回成功',
                'data': data
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class isStuHasGroupView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                username = payload['username']
                # print(payload['username'])
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })
            
            hasGroup = True
            user = Student.objects.filter(stu_num=username).first()
            if user.group_id == "" or user.group_id == None:
                hasGroup = False
            data = {
                'hasGroup': hasGroup
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

class groupListMsgView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                username = payload['username']
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })
            
            data_list = []
            for item in Group.objects.all():
                num = 0
                for item2 in Student.objects.all():
                    if item2.group_id == item.id:
                        num += 1
                if num != 0:
                    data = {'name': item.name, 'num': num}
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

class joinGroupView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                username = payload['username']
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })
            
            groupName = request.data.get('groupName')
            group_id = Group.objects.filter(name=groupName).first().id
            user = Student.objects.filter(stu_num=username).first()
            user.group_id = group_id
            user.save()

            return Response({
                'status': 200,
                'msg': '加入团队成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class groupNameExistView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                username = payload['username']
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })
            
            groupNameExist = False
            groupName = request.GET['groupName']
            group = Group.objects.filter(name=groupName).first()
            if group:
                groupNameExist = True
            data = {
                'groupNameExist': groupNameExist
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

class createGroupView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                username = payload['username']
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })
            
            groupName = request.data.get('groupName')

            newGroup = Group(id=groupName,name=groupName)
            newGroup.save()

            user = Student.objects.filter(stu_num=username).first()
            user.group_id = groupName
            user.save()

            return Response({
                'status': 200,
                'msg': '创建并加入团队成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class addStuCheckView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                username = payload['username']
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })

            stuNum = request.GET['stuNum']
            stuStatus = 0 #0：可添加 1：学号不存在 2：该学生已加入团队
            user = Student.objects.filter(stu_num=stuNum).first()
            if not user:
                stuStatus = 1
            elif user.group_id != None and user.group_id != "":
                stuStatus = 2
            data = {
                'stuStatus': stuStatus
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

class addGroupNumberView(APIView):
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
            
            stu_num = request.data.get('stu_num')
            groupName = request.data.get('groupName')
            role = request.data.get('role')
            group_id = Group.objects.filter(name=groupName).first().id
            user = Student.objects.filter(stu_num=stu_num).first()
            user.group_id = group_id
            user.role = role
            user.save()

            return Response({
                'status': 200,
                'msg': '添加成员成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class editRoleView(APIView):
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
            
            stu_num = request.data.get('stu_num')
            role = request.data.get('role')
            user = Student.objects.filter(stu_num=stu_num).first()
            user.role = role
            user.save()

            return Response({
                'status': 200,
                'msg': '修改承担角色成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class quitTeamView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                username = payload['username']
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })
            
            user = Student.objects.filter(stu_num=username).first()
            user.group_id = None
            user.role = None
            user.save()

            return Response({
                'status': 200,
                'msg': '修改承担角色成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class stuMsgView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                username = payload['username']
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })
            
            user = Student.objects.filter(stu_num=username).first()
            data = {
                'stu_num': username,
                'name': user.name,
                'college': user.college,
                'class_name': user.class_name,
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

class editStuMsgView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            try:
                payload = JwtQueryParamAuthentication.authenticate(self, request)[0]
                username = payload['username']
            except Exception as e:
                return Response({
                    'status': 403,
                    'msg': '未登录',
                    'err': e.args
                })
            
            editMsg = request.data.get('editMsg')
            user = Student.objects.filter(stu_num=username).first()

            user.name = editMsg['name']
            user.college = editMsg['college']
            user.class_name = editMsg['class_name']
            user.phone = editMsg['phone']
            user.save()

            return Response({
                'status': 200,
                'msg': '修改信息成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class addLoginRecordView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            user = Student.objects.filter(stu_num=username).first()
            lRecord = loginRecord(student_id=user.id)
            lRecord.save()

            return Response({
                'status': 200,
                'msg': '返回成功'
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class getLoginNumberView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            year = request.GET['year']
            month = request.GET['month']
            day = request.GET['day']
            # print(year, month, day)
            data = []

            er = 28
            if int(year) % 100 != 0 and int(year) % 4 == 0 or int(year) % 400 == 0:
                er = 29
            monthDay = [0,31,er,31,30,31,30,31,31,30,31,30,31]
            num = 7
            
            while num > 0:
                if len(month) == 1:
                    month = '0' + month
                if len(day) == 1:
                    day = '0' + day
                num -= 1
                number = 0
                for item in loginRecord.objects.all():
                    # print(item.time.strftime('%Y-%m-%d'),year + '-' + month + '-' + day)
                    if item.time.strftime('%Y-%m-%d') == year + '-' + month + '-' + day:
                        number += 1
                data.append(number)
                
                intday = int(day) - 1
                intmonth = int(month)
                intyear = int(year)
                # print(intyear,intmonth,intday)
                if intday == 0:
                    intmonth -= 1
                    if intmonth == 0:
                        intmonth = 12
                        intyear -= 1
                    intday = monthDay[intmonth]
                day = str(intday)
                month = str(intmonth)
                year = str(intyear)
            # print(data)
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

class getGroupNameView(APIView):
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
            
            group_id = request.GET['group_id']
            data = Group.objects.filter(id=group_id).first().name
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

class groupNameByStu_nameView(APIView):
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
            
            stu_num = request.GET['stu_num']
            data = Student.objects.filter(stu_num=stu_num).first().group_id
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

class getGroupNumbersMsgView(APIView):
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
            
            group_id = request.GET['group_id']

            # data = Student.objects.filter(stu_num=stu_num).first().group_id
            data_list = []
            for item in Student.objects.filter(group_id=group_id):
                data = {
                    'name': item.name,
                    'class_name': item.class_name,
                    'stu_num': item.stu_num,
                    'role': item.role,
                    'college': item.college,
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
