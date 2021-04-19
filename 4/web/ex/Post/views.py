from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ex.models import Teacher,Student,Group,Report,TeamEvaluation,PrivateLetter,ChatBoxIsOpen,Post,Comment,ThumbsUp
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
            
            TeaUser_id = payload['id']
            st1 = request.GET['st']
            ed1 = request.GET['ed']
            PostOptionsValue = request.GET['PostOptionsValue']
            st = int(st1) - 1
            ed = int(ed1) - 1

            # print(st1,ed1,PostOptionsValue)

            data_list = []
            
            if PostOptionsValue == '1':
                for item in Post.objects.all():
                    identity = 0
                    if item.userTea_id != None and item.userTea_id != '':
                        identity = 0
                        user_id = item.userTea_id
                    else:
                        identity = 1
                        user_id = Student.objects.filter(id=item.userStu_id).first().stu_num
                    commentNum = 0
                    for item2 in Comment.objects.filter(post_id=item.id):
                        commentNum += 1
                    thumbsUpNum = 0
                    for item2 in ThumbsUp.objects.filter(post_id=item.id):
                        thumbsUpNum += 1
                    thumbsUp = 0
                    thumbsUpTable = ThumbsUp.objects.filter(Q(post_id=item.id) & Q(userTea_id=TeaUser_id)).first()
                    if not thumbsUpTable:
                        thumbsUp = 0
                    else:
                        thumbsUp = 1
                    data = {
                        'id': item.id,
                        'user_id': user_id,
                        'title': item.title,
                        'message': item.message,
                        'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                        'identity': identity, #老师：0；学生：1
                        'commentNum': commentNum,
                        'thumbsUpNum': thumbsUpNum,
                        'thumbsUp': thumbsUp
                    }
                    data_list.append(data)
            else:
                for item in Post.objects.filter(userTea_id=TeaUser_id):
                    identity = 0
                    if item.userTea_id != None and item.userTea_id != '':
                        identity = 0
                        user_id = item.userTea_id
                    else:
                        identity = 1
                        user_id = Student.objects.filter(id=item.userStu_id).first().stu_num
                    commentNum = 0
                    for item2 in Comment.objects.filter(post_id=item.id):
                        commentNum += 1
                    thumbsUpNum = 0
                    for item2 in ThumbsUp.objects.filter(post_id=item.id):
                        thumbsUpNum += 1
                    thumbsUp = 0
                    thumbsUpTable = ThumbsUp.objects.filter(Q(post_id=item.id) & Q(userTea_id=TeaUser_id)).first()
                    if not thumbsUpTable:
                        thumbsUp = 0
                    else:
                        thumbsUp = 1
                    data = {
                        'id': item.id,
                        'user_id': user_id,
                        'title': item.title,
                        'message': item.message,
                        'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                        'identity': identity, #老师：0；学生：1
                        'commentNum': commentNum,
                        'thumbsUpNum': thumbsUpNum,
                        'thumbsUp': thumbsUp
                    }
                    data_list.append(data)

            len1 = len(data_list)
            allPostLists = []
            data_list2 = []

            

            # print(max(len1 - 1 - st,0),max(len1 - 2 - ed,-1))

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

            user_id = payload['id']
            title = request.data.get('title')
            message = request.data.get('message')
            # print(user_id,title,message)

            posts = Post(userTea_id=user_id,title=title,message=message)
            posts.save()
            
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
            
            posts = Post.objects.filter(id=id).first()
            posts.delete()
            
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

            user_id = payload['id']
            id = request.data.get('id')
            message = request.data.get('message')
            
            # print(id,message)
            comment = Comment(userTea_id=user_id,post_id=id,message=message)
            comment.save()

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

            # user_id = payload['id']
            id = request.GET['id']
            st1 = request.GET['st']
            ed1 = request.GET['ed']
            st = int(st1) - 1
            ed = int(ed1) - 1

            data_list = []
            for item in Comment.objects.filter(post_id=id):
                identity = 0
                if item.userTea_id != None and item.userTea_id != '':
                    identity = 0
                    user_id = item.userTea_id
                else:
                    identity = 1
                    user_id = Student.objects.filter(id=item.userStu_id).first().stu_num
                data = {
                    'id': item.id,
                    'user_id': user_id,
                    'message': item.message,
                    'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                    'identity': identity #老师：0；学生：1
                }
                data_list.append(data)
            # print(data_list)
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
            
            comment = Comment.objects.filter(id=id).first()
            comment.delete()
            
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

class thumbsUpView(APIView):
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

            thumbsUp = ThumbsUp(userTea_id=user_id,post_id=id)
            thumbsUp.save()

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

class thumbsDownView(APIView):
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
            
            thumbsUp = ThumbsUp.objects.filter(Q(userTea_id=user_id) & Q(post_id=id)).first()
            thumbsUp.delete()
            
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

class replyListsView(APIView):
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
            for item in Comment.objects.all():
                thisUser_id = Post.objects.filter(id=item.post_id).first().userTea_id
                if thisUser_id == user_id and item.userTea_id != user_id:
                    identity = 0
                    if item.userTea_id != None and item.userTea_id != '':
                        identity = 0
                        user_id2 = item.userTea_id
                    else:
                        identity = 1
                        user_id2 = Student.objects.filter(id=item.userStu_id).first().stu_num
                    data = {
                        'id': item.id,
                        'user_id': user_id2,
                        'message': item.message,
                        'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                        'post_id': item.post_id,
                        'identity': identity #老师：0；学生：1
                    }
                    data_list.append(data)
            
            data_list2 = data_list[::-1]
            # print(data_list2)
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

class replyPostView(APIView):
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

            TeaUser_id = payload['id']

            post_id = request.GET['id']
            item = Post.objects.filter(id=post_id).first()
            identity = 0
            if item.userTea_id != None and item.userTea_id != '':
                identity = 0
                user_id = item.userTea_id
            else:
                identity = 1
                user_id = Student.objects.filter(id=item.userStu_id).first().stu_num
            commentNum = 0
            for item2 in Comment.objects.filter(post_id=item.id):
                commentNum += 1
            thumbsUpNum = 0
            for item2 in ThumbsUp.objects.filter(post_id=item.id):
                thumbsUpNum += 1
            thumbsUp = 0
            thumbsUpTable = ThumbsUp.objects.filter(Q(post_id=item.id) & Q(userTea_id=TeaUser_id)).first()
            if not thumbsUpTable:
                thumbsUp = 0
            else:
                thumbsUp = 1
            data = {
                'id': item.id,
                'user_id': user_id,
                'title': item.title,
                'message': item.message,
                'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                'identity': identity, #老师：0；学生：1
                'commentNum': commentNum,
                'thumbsUpNum': thumbsUpNum,
                'thumbsUp': thumbsUp
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

class stuPostMsgView(APIView):
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
            
            StuUser_id = payload['id']
            st1 = request.GET['st']
            ed1 = request.GET['ed']
            PostOptionsValue = request.GET['PostOptionsValue']
            st = int(st1) - 1
            ed = int(ed1) - 1

            data_list = []
            
            if PostOptionsValue == '1':
                for item in Post.objects.all():
                    identity = 0
                    if item.userTea_id != None and item.userTea_id != '':
                        identity = 0
                        user_id = item.userTea_id
                    else:
                        identity = 1
                        user_id = Student.objects.filter(id=item.userStu_id).first().stu_num
                    commentNum = 0
                    for item2 in Comment.objects.filter(post_id=item.id):
                        commentNum += 1
                    thumbsUpNum = 0
                    for item2 in ThumbsUp.objects.filter(post_id=item.id):
                        thumbsUpNum += 1
                    thumbsUp = 0
                    thumbsUpTable = ThumbsUp.objects.filter(Q(post_id=item.id) & Q(userStu_id=StuUser_id)).first()
                    if not thumbsUpTable:
                        thumbsUp = 0
                    else:
                        thumbsUp = 1
                    data = {
                        'id': item.id,
                        'user_id': user_id,
                        'title': item.title,
                        'message': item.message,
                        'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                        'identity': identity, #老师：0；学生：1
                        'commentNum': commentNum,
                        'thumbsUpNum': thumbsUpNum,
                        'thumbsUp': thumbsUp
                    }
                    data_list.append(data)
            else:
                for item in Post.objects.filter(userStu_id=StuUser_id):
                    identity = 0
                    if item.userTea_id != None and item.userTea_id != '':
                        identity = 0
                        user_id = item.userTea_id
                    else:
                        identity = 1
                        user_id = Student.objects.filter(id=item.userStu_id).first().stu_num
                    commentNum = 0
                    for item2 in Comment.objects.filter(post_id=item.id):
                        commentNum += 1
                    thumbsUpNum = 0
                    for item2 in ThumbsUp.objects.filter(post_id=item.id):
                        thumbsUpNum += 1
                    thumbsUp = 0
                    thumbsUpTable = ThumbsUp.objects.filter(Q(post_id=item.id) & Q(userStu_id=StuUser_id)).first()
                    if not thumbsUpTable:
                        thumbsUp = 0
                    else:
                        thumbsUp = 1
                    data = {
                        'id': item.id,
                        'user_id': user_id,
                        'title': item.title,
                        'message': item.message,
                        'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                        'identity': identity, #老师：0；学生：1
                        'commentNum': commentNum,
                        'thumbsUpNum': thumbsUpNum,
                        'thumbsUp': thumbsUp
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

class stuReleasePostView(APIView):
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
            title = request.data.get('title')
            message = request.data.get('message')
            # print(user_id,title,message)

            posts = Post(userStu_id=user_id,title=title,message=message)
            posts.save()
            
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

class stuCommentPostView(APIView):
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
            message = request.data.get('message')
            
            # print(id,message)
            comment = Comment(userStu_id=user_id,post_id=id,message=message)
            comment.save()

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

class stuThumbsUpView(APIView):
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

            thumbsUp = ThumbsUp(userStu_id=user_id,post_id=id)
            thumbsUp.save()

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

class stuThumbsDownView(APIView):
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
            
            thumbsUp = ThumbsUp.objects.filter(Q(userStu_id=user_id) & Q(post_id=id)).first()
            thumbsUp.delete()
            
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

class stuReplyListsView(APIView):
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
            for item in Comment.objects.all():
                thisUser_id = Post.objects.filter(id=item.post_id).first().userStu_id
                if thisUser_id == user_id and item.userStu_id != user_id:
                    identity = 0
                    if item.userTea_id != None and item.userTea_id != '':
                        identity = 0
                        user_id2 = item.userTea_id
                    else:
                        identity = 1
                        user_id2 = Student.objects.filter(id=item.userStu_id).first().stu_num
                    data = {
                        'id': item.id,
                        'user_id': user_id2,
                        'message': item.message,
                        'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                        'post_id': item.post_id,
                        'identity': identity #老师：0；学生：1
                    }
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

class stuReplyPostView(APIView):
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

            TeaUser_id = payload['id']

            post_id = request.GET['id']
            item = Post.objects.filter(id=post_id).first()
            identity = 0
            if item.userTea_id != None and item.userTea_id != '':
                identity = 0
                user_id = item.userTea_id
            else:
                identity = 1
                user_id = Student.objects.filter(id=item.userStu_id).first().stu_num
            commentNum = 0
            for item2 in Comment.objects.filter(post_id=item.id):
                commentNum += 1
            thumbsUpNum = 0
            for item2 in ThumbsUp.objects.filter(post_id=item.id):
                thumbsUpNum += 1
            thumbsUp = 0
            thumbsUpTable = ThumbsUp.objects.filter(Q(post_id=item.id) & Q(userStu_id=TeaUser_id)).first()
            if not thumbsUpTable:
                thumbsUp = 0
            else:
                thumbsUp = 1
            data = {
                'id': item.id,
                'user_id': user_id,
                'title': item.title,
                'message': item.message,
                'time': str(item.time.strftime('%Y-%m-%d %H:%M:%S')),
                'identity': identity, #老师：0；学生：1
                'commentNum': commentNum,
                'thumbsUpNum': thumbsUpNum,
                'thumbsUp': thumbsUp
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
