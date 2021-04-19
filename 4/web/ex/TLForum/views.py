from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ex.models import Group,TLPost,TLComment,TLVote,TLGroupVote
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
# from plane.models import User, Student, LightList, Light, Score, Visit
# from plane.utils.jwt_auth import create_token, get_user_id
# from django.contrib.auth.hashers import make_password, check_password

from ex.utils.jwt_auth import create_token, get_user_id

from ex.utils.extensions.auth import JwtQueryParamAuthentication

import time
import datetime

from django.db.models import Q

# Create your views here.

class postMsgView(APIView):
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
            
            group_id = request.GET['group']
            st1 = request.GET['st']
            ed1 = request.GET['ed']
            PostOptionsValue = request.GET['PostOptionsValue']
            st = int(st1) - 1
            ed = int(ed1) - 1

            data_list = []
            
            if PostOptionsValue == '1':
                for item in TLPost.objects.all():
                    commentNum = 0
                    for item2 in TLComment.objects.filter(tlPost_id=item.id):
                        commentNum += 1

                    groupName = Group.objects.filter(id=item.group_id).first().name
                    data = {
                        'id': item.id,
                        'user_id': groupName,
                        'group_id': item.group_id,
                        'title': item.title,
                        'message': item.message,
                        'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                        'commentNum': commentNum,
                    }
                    data_list.append(data)
            else:
                for item in TLPost.objects.filter(group_id=group_id):
                    commentNum = 0
                    for item2 in TLComment.objects.filter(tlPost_id=item.id):
                        commentNum += 1

                    groupName = Group.objects.filter(id=item.group_id).first().name
                    data = {
                        'id': item.id,
                        'user_id': groupName,
                        'group_id': item.group_id,
                        'title': item.title,
                        'message': item.message,
                        'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                        'commentNum': commentNum,
                    }
                    data_list.append(data)

            len1 = len(data_list)
            allPostLists = []
            data_list2 = []

            if len1 > 0:
                for i in range(max(len1 - 1 - st,0),max(len1 - 2 - ed,-1),-1):
                    data_list2.append(data_list[i])
                for i in range(len1 - 1,-1,-1):
                    allPostLists.append(data_list[i])
            
            dataRes = {
                'data': data_list2,
                'numTotal': len1,
                'allPostLists': allPostLists
            }
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': dataRes
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class releasePostView(APIView):
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

            group_id = request.data.get('group')
            title = request.data.get('title')
            message = request.data.get('message')
            
            tlPost = TLPost(group_id=group_id,title=title,message=message)
            tlPost.save()
            data = tlPost.id
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

class deletePostView(APIView):
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
            
            tlPost = TLPost.objects.filter(id=id).first()
            tlPost.delete()
            
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

class commentPostView(APIView):
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
            message = request.data.get('message')
            group_id = request.data.get('group')
            
            if group_id == 'ai':
                time.sleep(20)

            tlComment = TLComment(group_id=group_id,tlPost_id=id,message=message)
            tlComment.save()

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

class commentMsgView(APIView):
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

            id = request.GET['id']
            st1 = request.GET['st']
            ed1 = request.GET['ed']
            st = int(st1) - 1
            ed = int(ed1) - 1

            data_list = []
            for item in TLComment.objects.filter(tlPost_id=id):
                groupName = Group.objects.filter(id=item.group_id).first().name
                data = {
                    'id': item.id,
                    'user_id': groupName,
                    'group_id': item.group_id,
                    'message': item.message,
                    'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                }
                data_list.append(data)
            
            len1 = len(data_list)
            data_list2 = []

            if len1 > 0:
                for i in range(max(len1 - 1 - st,0),max(len1 - 2 - ed,-1),-1):
                    data_list2.append(data_list[i])
            
            dataRes = {
                'data': data_list2,
                'numTotal': len1
            }
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': dataRes
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class deleteCommentView(APIView):
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
            
            tlComment = TLComment.objects.filter(id=id).first()
            tlComment.delete()
            
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

class votePostCommentMsgView(APIView):
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

            tlCommentID = request.GET['tlCommentID']

            tlComment = TLComment.objects.filter(id=tlCommentID).first()
            tlPost = TLPost.objects.filter(id=tlComment.tlPost_id).first()

            data = {
                'title': tlPost.title,
                'tlPostMessage': tlPost.message,
                'tlCommentMessage': tlComment.message,
            }
            
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data,
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class initiateVoteView(APIView):
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

            tlCommentID = request.data.get('tlCommentID')
            endTimeRadio = request.data.get('endTimeRadio')
            group_id = request.data.get('group_id')

            # 2021-03-31 19:47:43.781687
            
            tlVote = TLVote(group_id=group_id,tlComment_id=tlCommentID)
            tlVote.save()
            if endTimeRadio == 1:
                tlVote.endTime = tlVote.time + datetime.timedelta(minutes=1)
            elif endTimeRadio == 2:
                tlVote.endTime = tlVote.time + datetime.timedelta(minutes=10)
            else:
                tlVote.endTime = tlVote.time + datetime.timedelta(hours=1)
            tlVote.save()
            
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

class voteListsView(APIView):
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

            data_list = []
            for item in TLVote.objects.all():
            # for item in TLVote.objects.filter(group_id=group_id):
                tlComment = TLComment.objects.filter(id=item.tlComment_id).first()
                tlPost = TLPost.objects.filter(id=tlComment.tlPost_id).first()
                num = 0
                for item2 in TLGroupVote.objects.filter(tlVote_id=item.id):
                    num += 1
                isVote = -1
                tlGroupVote = TLGroupVote.objects.filter(Q(group_id=group_id) & Q(tlVote_id=item.id)).first()
                if tlGroupVote:
                    if tlGroupVote.result == 0:
                        isVote = 0
                    else:
                        isVote = 1
                
                isOver = 0
                if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') > item.endTime.strftime('%Y-%m-%d %H:%M:%S'):
                    isOver = 1

                answer = 0
                if tlComment.group_id == 'ai':
                    answer = 1
                
                result0 = 0
                result1 = 0
                for item2 in TLGroupVote.objects.filter(tlVote_id=item.id):
                    if item2.result == 0:
                        result0 += 1
                    else:
                        result1 += 1
                    
                data = {
                    'id': item.id,
                    'time': item.time.strftime('%Y-%m-%d %H:%M:%S'),
                    'endTime': item.endTime.strftime('%Y-%m-%d %H:%M:%S'),
                    'group_id': item.group_id,
                    'group_name': Group.objects.filter(id=item.group_id).first().name,
                    'tlComment_id': item.tlComment_id,
                    'tlComment_idMessage': tlComment.message,
                    'tlPost_id': tlComment.tlPost_id,
                    'tlPost_idMessage': tlPost.message,
                    'title': tlPost.title,
                    'num': num,
                    'isVote': isVote,
                    'isOver': isOver,
                    'answer': answer,
                    'result0': result0,
                    'result1': result1,
                }
                data_list.append(data)

            data_list2 = data_list[::-1]

            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data_list2,
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class myVoteListsView(APIView):
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

            data_list = []
            for item in TLVote.objects.all():
            # for item in TLVote.objects.filter(group_id=group_id):
                if item.group_id == group_id or TLGroupVote.objects.filter(Q(group_id=group_id) & Q(tlVote_id=item.id)):
                    tlComment = TLComment.objects.filter(id=item.tlComment_id).first()
                    tlPost = TLPost.objects.filter(id=tlComment.tlPost_id).first()
                    num = 0
                    for item2 in TLGroupVote.objects.filter(tlVote_id=item.id):
                        num += 1
                    isVote = -1
                    tlGroupVote = TLGroupVote.objects.filter(Q(group_id=group_id) & Q(tlVote_id=item.id)).first()
                    if tlGroupVote:
                        if tlGroupVote.result == 0:
                            isVote = 0
                        else:
                            isVote = 1
                    
                    isOver = 0
                    if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') > item.endTime.strftime('%Y-%m-%d %H:%M:%S'):
                        isOver = 1

                    answer = 0
                    if tlComment.group_id == 'ai':
                        answer = 1
                    
                    result0 = 0
                    result1 = 0
                    for item2 in TLGroupVote.objects.filter(tlVote_id=item.id):
                        if item2.result == 0:
                            result0 += 1
                        else:
                            result1 += 1
                    
                    data = {
                        'id': item.id,
                        'time': item.time.strftime('%Y-%m-%d %H:%M:%S'),
                        'endTime': item.endTime.strftime('%Y-%m-%d %H:%M:%S'),
                        'group_id': item.group_id,
                        'group_name': Group.objects.filter(id=item.group_id).first().name,
                        'tlComment_id': item.tlComment_id,
                        'tlComment_idMessage': tlComment.message,
                        'tlPost_id': tlComment.tlPost_id,
                        'tlPost_idMessage': tlPost.message,
                        'title': tlPost.title,
                        'num': num,
                        'isVote': isVote,
                        'isOver': isOver,
                        'answer': answer,
                        'result0': result0,
                        'result1': result1,
                        'diff': (item.endTime - item.time).seconds//60,
                    }
                    data_list.append(data)

            data_list2 = data_list[::-1]

            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data_list2,
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class toVoteView(APIView):
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

            group_id = request.data.get('group_id')
            result = request.data.get('result')
            tlVote_id = request.data.get('tlVote_id')

            if datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') < TLVote.objects.filter(id=tlVote_id).first().endTime.strftime('%Y-%m-%d %H:%M:%S'):
                tlGroupVote = TLGroupVote(group_id=group_id,tlVote_id=tlVote_id,result=result)
                tlGroupVote.save()
            else:
                return Response({
                    'status': 201,
                    'msg': '投票已截止'
                })
            
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

class voteDetailView(APIView):
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
            
            tlVote_id = request.GET['tlVote_id']

            result0 = 0
            result1 = 0
            for item in TLGroupVote.objects.filter(tlVote_id=tlVote_id):
                if item.result == 0:
                    result0 += 1
                else:
                    result1 += 1
                
            data = {
                'result0': result0,
                'result1': result1,
            }
            return Response({
                'status': 200,
                'msg': '返回成功',
                'data': data,
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })
