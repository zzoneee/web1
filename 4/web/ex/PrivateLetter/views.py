from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ex.models import Teacher,Student,Group,Report,TeamEvaluation,PrivateLetter,ChatBoxIsOpen
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

class getPrivateLetterListsView(APIView):
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
            for item in ChatBoxIsOpen.objects.filter(Q(senderTea_id=user_id) & Q(isOpen=1)):
                msgList = []
                msgList1 = []
                msgList2 = []
                receiver = item.receiverTea_id
                identity = 0
                if item.receiverStu_id != None:
                    receiver = Student.objects.filter(id=item.receiverStu_id).first().stu_num
                    identity = 1
                    for item2 in PrivateLetter.objects.filter(Q(senderTea_id=user_id) & Q(receiverStu_id=item.receiverStu_id)):
                        data = {
                            'id': item2.id,
                            'message': item2.message,
                            'time': str(item2.time.strftime('%Y-%m-%d %H:%M:%S')),
                            'new': item2.new,
                            'Ienter': 1 # 发送
                        }
                        msgList1.append(data)
                    for item2 in PrivateLetter.objects.filter(Q(senderStu_id=item.receiverStu_id) & Q(receiverTea_id=user_id)):
                        data = {
                            'id': item2.id,
                            'message': item2.message,
                            'time': str(item2.time.strftime('%Y-%m-%d %H:%M:%S')),
                            'new': item2.new,
                            'Ienter': 2 # 接收
                        }
                        msgList2.append(data)
                    # msgList.sort()
                    # print(len(msgList1))
                else:
                    for item2 in PrivateLetter.objects.filter(Q(senderTea_id=user_id) & Q(receiverTea_id=receiver)):
                        data = {
                            'id': item2.id,
                            'message': item2.message,
                            'time': str(item2.time.strftime('%Y-%m-%d %H:%M:%S')),
                            'new': item2.new,
                            'Ienter': 1 # 发送
                        }
                        msgList1.append(data)
                    for item2 in PrivateLetter.objects.filter(Q(senderTea_id=receiver) & Q(receiverTea_id=user_id)):
                        data = {
                            'id': item2.id,
                            'message': item2.message,
                            'time': str(item2.time.strftime('%Y-%m-%d %H:%M:%S')),
                            'new': item2.new,
                            'Ienter': 2 # 接收
                        }
                        msgList2.append(data)
                    # msgList.sort()
                len1 = len(msgList1)
                len2 = len(msgList2)
                i1 = 0
                i2 = 0
                for i in range(0,len1 + len2):
                    if i1 >= len1:
                        msgList.append(msgList2[i2])
                        i2+=1
                    elif i2 >= len2:
                        msgList.append(msgList1[i1])
                        i1+=1
                    elif msgList1[i1]['time'] < msgList2[i2]['time']:
                        msgList.append(msgList1[i1])
                        i1+=1
                    else:
                        msgList.append(msgList2[i2])
                        i2+=1

                # print(msgList)
                data = {
                    'id': item.id,
                    'receiver': receiver,
                    'msgList': msgList,
                    'name': receiver + str(identity),
                    'identity': identity
                }
                data_list.append(data)
            # print(data_list)
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

class enterPrivateLetterView(APIView):
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
            receiver = request.data.get('receiver')
            message = request.data.get('message')
            identity = request.data.get('identity')

            if identity == 0:
                privateLetter = PrivateLetter(senderTea_id=user_id,receiverTea_id=receiver,message=message)
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderTea_id=receiver)&Q(receiverTea_id=user_id)).first()
                if not chatBoxIsOpen:
                    chatBoxIsOpen = ChatBoxIsOpen(senderTea_id=receiver,receiverTea_id=user_id)
            else:
                receiverStu_id = Student.objects.filter(stu_num=receiver).first().id
                privateLetter = PrivateLetter(senderTea_id=user_id,receiverStu_id=receiverStu_id,message=message)
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderStu_id=receiverStu_id)&Q(receiverTea_id=user_id)).first()
                if not chatBoxIsOpen:
                    chatBoxIsOpen = ChatBoxIsOpen(senderStu_id=receiverStu_id,receiverTea_id=user_id)
            privateLetter.save()
            chatBoxIsOpen.save()

            return Response({
                'status': 200,
                'msg': '发布私信成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

# 获取最近联系人
class getRecentContactsView(APIView):
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
            for item in PrivateLetter.objects.filter(senderTea_id=user_id):
                if item.receiverTea_id != None and item.receiverTea_id != "":
                    identity = 0
                    receiver = item.receiverTea_id
                else:
                    identity = 1
                    receiver = Student.objects.filter(id=item.receiverStu_id).first().stu_num
                # print(((receiver + str(identity)) not in dict))
                # if (receiver + str(identity)) not in dict:
                    # dict[receiver + str(identity)] = '1'
                data = {
                    # 'id': item.id,
                    'receiver': receiver,
                    'identity': identity #老师：0；学生：1
                }
                data_list.append(data)
            for item in PrivateLetter.objects.filter(receiverTea_id=user_id):
                if item.senderTea_id != None and item.senderTea_id != "":
                    identity = 0
                    receiver = item.senderTea_id
                else:
                    identity = 1
                    receiver = Student.objects.filter(id=item.senderStu_id).first().stu_num
                # print(((receiver + str(identity)) not in dict))
                # if (receiver + str(identity)) not in dict:
                    # dict[receiver + str(identity)] = '1'
                data = {
                    # 'id': item.id,
                    'receiver': receiver,
                    'identity': identity #老师：0；学生：1
                }
                data_list.append(data)
            lenData = len(data_list)
            dict = {}
            data_list1 = []
            for i in range(lenData - 1,-1,-1):
                if (data_list[i]['receiver'] + str(data_list[i]['identity'])) not in dict:
                    dict[data_list[i]['receiver'] + str(data_list[i]['identity'])] = '1'
                    data_list1.append(data_list[i])

            # lenData = len(data_list1)
            # if lenData > 10:
            #     data_list1 = data_list1[lenData - 10:lenData]
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data_list1
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

# 关闭聊天框
class closeChatBoxView(APIView):
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
            receiver = request.data.get('receiver')
            iden = request.data.get('iden')
            
            if iden == 0:
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderTea_id=user_id) & Q(receiverTea_id=receiver)).first()
            else:
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderTea_id=user_id) & Q(receiverStu_id=Student.objects.filter(stu_num=receiver).first().id)).first()
            chatBoxIsOpen.delete()

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

# 打开聊天框
class openChatBoxView(APIView):
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
            receiver = request.data.get('receiver')
            identity = request.data.get('identity')
            
            if identity == 0:
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderTea_id=user_id) & Q(receiverTea_id=receiver)).first()
                if not chatBoxIsOpen:
                    chatBoxIsOpen = ChatBoxIsOpen(senderTea_id=user_id,receiverTea_id=receiver)
            else:
                receiverStu_id = Student.objects.filter(stu_num=receiver).first().id
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderTea_id=user_id) & Q(receiverStu_id=receiverStu_id)).first()
                if not chatBoxIsOpen:
                    chatBoxIsOpen = ChatBoxIsOpen(senderTea_id=user_id,receiverStu_id=receiverStu_id)
            chatBoxIsOpen.save()

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

# 搜索联系人
class searchContactView(APIView):
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
            receiver = request.GET['receiver']
            identity = request.GET['identity']
            # print(receiver,identity=='0')

            # user = Teacher.objects.filter(id=username).first()
            iden = 4
            if identity == '0' and user_id == receiver:
                iden = 3
            elif identity == '0':
                user = Teacher.objects.filter(id=receiver).first()
                if not user:
                    iden = 4
                else:
                    iden = 0
            else:
                user = Student.objects.filter(stu_num=receiver).first()
                if not user:
                    iden = 4
                else:
                    iden = 1
            data = {
                'identity': iden,
                'receiver': receiver
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

class stuGetPrivateLetterListsView(APIView):
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
            for item in ChatBoxIsOpen.objects.filter(Q(senderStu_id=user_id) & Q(isOpen=1)):
                msgList = []
                msgList1 = []
                msgList2 = []
                receiver = item.receiverTea_id
                identity = 0
                if item.receiverStu_id != None:
                    receiver = Student.objects.filter(id=item.receiverStu_id).first().stu_num
                    identity = 1
                    for item2 in PrivateLetter.objects.filter(Q(senderStu_id=user_id) & Q(receiverStu_id=item.receiverStu_id)):
                        data = {
                            'id': item2.id,
                            'message': item2.message,
                            'time': str(item2.time.strftime('%Y-%m-%d %H:%M:%S')),
                            'new': item2.new,
                            'Ienter': 1 # 发送
                        }
                        msgList1.append(data)
                    for item2 in PrivateLetter.objects.filter(Q(senderStu_id=item.receiverStu_id) & Q(receiverStu_id=user_id)):
                        data = {
                            'id': item2.id,
                            'message': item2.message,
                            'time': str(item2.time.strftime('%Y-%m-%d %H:%M:%S')),
                            'new': item2.new,
                            'Ienter': 2 # 接收
                        }
                        msgList2.append(data)
                    # msgList.sort()
                    # print(len(msgList1))
                else:
                    for item2 in PrivateLetter.objects.filter(Q(senderStu_id=user_id) & Q(receiverTea_id=receiver)):
                        data = {
                            'id': item2.id,
                            'message': item2.message,
                            'time': str(item2.time.strftime('%Y-%m-%d %H:%M:%S')),
                            'new': item2.new,
                            'Ienter': 1 # 发送
                        }
                        msgList1.append(data)
                    for item2 in PrivateLetter.objects.filter(Q(senderTea_id=receiver) & Q(receiverStu_id=user_id)):
                        data = {
                            'id': item2.id,
                            'message': item2.message,
                            'time': str(item2.time.strftime('%Y-%m-%d %H:%M:%S')),
                            'new': item2.new,
                            'Ienter': 2 # 接收
                        }
                        msgList2.append(data)
                    # msgList.sort()
                len1 = len(msgList1)
                len2 = len(msgList2)
                i1 = 0
                i2 = 0
                for i in range(0,len1 + len2):
                    if i1 >= len1:
                        msgList.append(msgList2[i2])
                        i2+=1
                    elif i2 >= len2:
                        msgList.append(msgList1[i1])
                        i1+=1
                    elif msgList1[i1]['time'] < msgList2[i2]['time']:
                        msgList.append(msgList1[i1])
                        i1+=1
                    else:
                        msgList.append(msgList2[i2])
                        i2+=1

                # print(msgList)
                data = {
                    'id': item.id,
                    'receiver': receiver,
                    'msgList': msgList,
                    'name': receiver + str(identity),
                    'identity': identity
                }
                data_list.append(data)
            # print(data_list)
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

class stuEnterPrivateLetterView(APIView):
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
            username = payload['username']
            # print(user_id,username)
            receiver = request.data.get('receiver')
            message = request.data.get('message')
            identity = request.data.get('identity')

            if identity == 0:
                privateLetter = PrivateLetter(senderStu_id=user_id,receiverTea_id=receiver,message=message)
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderTea_id=receiver)&Q(receiverStu_id=user_id)).first()
                if not chatBoxIsOpen:
                    chatBoxIsOpen = ChatBoxIsOpen(senderTea_id=receiver,receiverStu_id=user_id)
            else:
                receiverStu_id = Student.objects.filter(stu_num=receiver).first().id
                privateLetter = PrivateLetter(senderStu_id=user_id,receiverStu_id=receiverStu_id,message=message)
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderStu_id=receiverStu_id)&Q(receiverStu_id=user_id)).first()
                if not chatBoxIsOpen:
                    chatBoxIsOpen = ChatBoxIsOpen(senderStu_id=receiverStu_id,receiverStu_id=user_id)
            privateLetter.save()
            chatBoxIsOpen.save()

            return Response({
                'status': 200,
                'msg': '发布私信成功',
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

# 获取最近联系人
class stuRecentContactsView(APIView):
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
            for item in PrivateLetter.objects.filter(senderStu_id=user_id):
                if item.receiverTea_id != None and item.receiverTea_id != "":
                    identity = 0
                    receiver = item.receiverTea_id
                else:
                    identity = 1
                    receiver = Student.objects.filter(id=item.receiverStu_id).first().stu_num
                data = {
                    'receiver': receiver,
                    'identity': identity #老师：0；学生：1
                }
                data_list.append(data)
            for item in PrivateLetter.objects.filter(receiverStu_id=user_id):
                if item.senderTea_id != None and item.senderTea_id != "":
                    identity = 0
                    receiver = item.senderTea_id
                else:
                    identity = 1
                    receiver = Student.objects.filter(id=item.senderStu_id).first().stu_num
                data = {
                    'receiver': receiver,
                    'identity': identity #老师：0；学生：1
                }
                data_list.append(data)
            lenData = len(data_list)
            dict = {}
            data_list1 = []
            for i in range(lenData - 1,-1,-1):
                if (data_list[i]['receiver'] + str(data_list[i]['identity'])) not in dict:
                    dict[data_list[i]['receiver'] + str(data_list[i]['identity'])] = '1'
                    data_list1.append(data_list[i])

            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data_list1
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

# 关闭聊天框
class stuCloseChatBoxView(APIView):
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
            receiver = request.data.get('receiver')
            iden = request.data.get('iden')
            
            if iden == 0:
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderStu_id=user_id) & Q(receiverTea_id=receiver)).first()
            else:
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderStu_id=user_id) & Q(receiverStu_id=Student.objects.filter(stu_num=receiver).first().id)).first()
            chatBoxIsOpen.delete()

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

# 打开聊天框
class stuOpenChatBoxView(APIView):
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
            receiver = request.data.get('receiver')
            identity = request.data.get('identity')
            
            if identity == 0:
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderStu_id=user_id) & Q(receiverTea_id=receiver)).first()
                if not chatBoxIsOpen:
                    chatBoxIsOpen = ChatBoxIsOpen(senderStu_id=user_id,receiverTea_id=receiver)
            else:
                receiverStu_id = Student.objects.filter(stu_num=receiver).first().id
                chatBoxIsOpen = ChatBoxIsOpen.objects.filter(Q(senderStu_id=user_id) & Q(receiverStu_id=receiverStu_id)).first()
                if not chatBoxIsOpen:
                    chatBoxIsOpen = ChatBoxIsOpen(senderStu_id=user_id,receiverStu_id=receiverStu_id)
            chatBoxIsOpen.save()

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

# 搜索联系人
class stuSearchContactView(APIView):
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
            receiver = request.GET['receiver']
            identity = request.GET['identity']
            # print(receiver,identity=='0')

            # user = Teacher.objects.filter(id=username).first()
            # 0：教师，1：学生，2：还未搜索，3：自己，4：用户不存在
            iden = 4
            if identity == '1' and username == receiver:
                iden = 3
            elif identity == '0':
                user = Teacher.objects.filter(id=receiver).first()
                if not user:
                    iden = 4
                else:
                    iden = 0
            else:
                user = Student.objects.filter(stu_num=receiver).first()
                if not user:
                    iden = 4
                else:
                    iden = 1
            data = {
                'identity': iden,
                'receiver': receiver
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
