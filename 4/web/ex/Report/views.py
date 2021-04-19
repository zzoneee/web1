from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from ex.models import Student,Group,Report,TeamEvaluation,Classes,experiment,experimentData
from django.core import serializers

from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password

from ex.utils.extensions.auth import JwtQueryParamAuthentication

from ex.utils.jwt_auth import create_token, get_user_id
from ex.utils.extensions.auth import JwtQueryParamAuthentication

from docxtpl import DocxTemplate
import os

# Create your views here.

class ReportListView(APIView):
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

            userId = request.data.get('userId')
            user = Student.objects.filter(stu_num=userId).first()
            groupId = user.group_id
            data_list = []

            for item in Group.objects.get(id=groupId).report_set.all():
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
                data = {'ex_ID': item.id, 
                        'ex_Date': item.create_time.strftime('%Y-%m-%d'),
                        'ex_name': experiment.objects.filter(id=item.experiment_id).first().name,
                        'system_score': item.system_score, 
                        'teacher_score': item.teacher_score,
                        'address': item.url,
                        'hp_score': hp_score}
                data_list.append(data)
            
            return Response({
                "status": 200,
                "msg": '返回成功',
                "data": data_list
            })
        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class hp_reportListView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            userId = request.data.get('userId')
            user = Student.objects.filter(stu_num=userId).first()
            groupId = user.group_id
            data_list = []

            for items in Group.objects.filter(~Q(id=groupId)).all():
                for item in Group.objects.get(id=items.id).report_set.all():
                    hp_ex_score = -1
                    teamEvaluate = TeamEvaluation.objects.filter(Q(Rater_ID=groupId) & Q(Ratee_ID=item.id)).first()
                    if teamEvaluate:
                        hp_ex_score = teamEvaluate.score
                    data = {'hp_ex_ID': item.id, 
                            'hp_ex_groupName': Group.objects.filter(id=item.owner_id).first().name,
                            'hp_ex_Date': item.create_time.strftime('%Y-%m-%d'),
                            'hp_ex_name': experiment.objects.filter(id=item.experiment_id).first().name,
                            'hp_ex_address': item.url
                            ,'hp_ex_score': hp_ex_score}
                    data_list.append(data)

            return Response({
                "status": 200,
                "msg": '返回成功',
                # "data": serializers.serialize("json",Group.objects.filter(~Q(id=1)).all())
                "data": data_list
            })

        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })

class hp_reportMarkView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            userId = request.data.get('userId')
            id = request.data.get('id')
            score = request.data.get('score')
            user = Student.objects.filter(stu_num=userId).first()
            # report = Report.objects.filter(id=id).first()
            teamEvaluate = TeamEvaluation.objects.filter(Q(Rater_ID=user.group_id) & Q(Ratee_ID=id)).first()
            if teamEvaluate:
                teamEvaluate.score = score
                teamEvaluate.save()
            else:
                teamEvaluate = TeamEvaluation(Rater_ID=user.group_id,Ratee_ID=id,score=score)
                teamEvaluate.save()
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

class StuReportMsgListsView(APIView):
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
            classesID = request.GET['classesID']
            exID = request.GET['exID']
            OP = request.GET['OP']

            class_name = Classes.objects.filter(id=classesID).first().name

            # print(classesID, exID, class_name)
           
            data_list = []
            for item in Student.objects.filter(class_name=class_name):
                hasReport = 0
                report = Report.objects.filter(Q(experiment_id=exID) & Q(owner_id=item.group_id))
                if report:
                    hasReport = 1
                groupname = None
                role = None
                if item.group_id != None and item.group_id != '':
                    groupname = Group.objects.filter(id=item.group_id).first().name
                    role = item.role
                data = {
                    'stu_num': item.stu_num,
                    'name': item.name,
                    'group': groupname,
                    'role': role,
                    'hasReport': hasReport
                }
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

class createReportView(APIView):
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

            form = request.data.get('form')
            # form = {
            #     'group_id': '', # 团队ID
            #     'experiment_id': '', # 实验ID
            #     'exDate': '', # 实验日期 格式为2021-4-1
            #     'exPurpose': '', # 实验目的
            #     'exSteps': '', # 实验步骤
            #     'exResult': '', # 实验结果
            #     'systemScore': '', # 系统评分
            #     'exExperience': '', # 实验心得
            # }
            # print(form['time'])
            groupName = Group.objects.filter(id=form['group_id']).first().name
            exName = experiment.objects.filter(id=form['experiment_id']).first().name
            groupNumberMsg = ''
            i = 1
            for item in Student.objects.filter(group_id=form['group_id']):
                if i != 1:
                    groupNumberMsg += '\n'
                role = item.role
                if item.role == None or item.role == '':
                    role = '无'
                groupNumberMsg += '队员' + str(i) + '：' + '姓名：' + item.name + ' 学院：' + item.college + ' 班级：' + item.class_name + ' 学号：' + item.stu_num + ' 承担角色：' + role
                i += 1

            # 重复提交的实验报告时，覆盖之前的实验报告
            report = Report.objects.filter(Q(experiment_id=form['experiment_id']) & Q(owner_id=form['group_id'])).first()
            if report:
                id = report.id
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
                length = len(base_dir)
                for i in range(length - 2,0,-1):
                    if base_dir[i] == '\\':
                        base_dir = base_dir[0:i]
                        break
                file_path = os.path.join(base_dir, 'static','report', report.url)  # 下载文件的绝对路径
                if os.path.isfile(file_path):  # 判断下载文件是否存在
                    os.remove(file_path)
                report.delete()

            # 创建实验报告
            # form['exDate']
            # length = len(form['exDate'])
            year = 0
            month = 0
            day = 0
            ff = 0
            for item in form['exDate']:
                if item == '-':
                    ff += 1
                else:
                    if ff == 0:
                        year *= 10
                        year += int(item)
                    elif ff == 1:
                        month *= 10
                        month += int(item)
                    elif ff == 2:
                        day *= 10
                        day += int(item)
            # print(year,month,day)
            data_dic = {
                'exName': exName,
                'groupName': groupName,
                'groupNumberMsg': groupNumberMsg,
                'exPurpose': form['exPurpose'],
                'exSteps': form['exSteps'],
                'exResult': form['exResult'],
                'systemScore': form['systemScore'],
                'teacherScore': '未评分',
                'teamEvaluationScore': '未评分',
                'exExperience': form['exExperience'],
                'year': year,
                'month': month,
                'day': day,
            }
            docxName = 'ex_' + form['experiment_id'] + '_' + form['group_id'] + '.docx'

            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
            length = len(base_dir)
            for i in range(length - 2,0,-1):
                if base_dir[i] == '\\':
                    base_dir = base_dir[0:i]
                    break
            file_path = os.path.join(base_dir, 'static','report', 'tpl.docx')  # 下载文件的绝对路径
            file_path2 = os.path.join(base_dir, 'static','report', docxName)  # 下载文件的绝对路径
            doc = DocxTemplate(file_path) #加载模板文件
            doc.render(data_dic) #填充数据
            doc.save(file_path2) #保存目标文件
            
            # print(type(form['group_id']))
            report = Report(id=str(form['group_id']) + '_' + str(form['experiment_id']),system_score=form['systemScore'],teacher_score=-1,url=docxName,owner_id=form['group_id'],experiment_id=form['experiment_id'])
            report.save()

            experimentData1 = experimentData(report_id=report.id,exPurpose=form['exPurpose'],systemScore=form['systemScore'],exTime=form['exDate'],experiment_id=form['experiment_id'],group_id=form['group_id'],exExperience=form['exExperience'],exResult=form['exResult'],exSteps=form['exSteps'])
            experimentData1.save()


            # exExperience = request.data.get('exExperience')
            # data_dic = {
            #     'exName': '无人机集群编队三维模拟实验',
            #     'groupName': 'group2',
            #     'groupNumberMsg': '张三/计算机171/2020003/项目统筹\n王五/计算机174/2020012/算法研究',
            #     'exPurpose': '按照要求完成无人机编队及灯光设计。',
            #     'exSteps': '1.H型编队设计；\n2.H型变换Z型路线设计；\n3.夜间灯光设计；\n4.N型变换Z型。',
            #     'exResult': exResult,
            #     'systemScore': '87',
            #     'teacherScore': '未评分',
            #     'teamEvaluationScore': '未评分',
            #     'exExperience': exExperience,
            #     'year': '2021',
            #     'month': '3',
            #     'day': '10',
            # }
            # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
            # length = len(base_dir)
            # for i in range(length - 2,0,-1):
            #     if base_dir[i] == '\\':
            #         base_dir = base_dir[0:i]
            #         break
            # file_path = os.path.join(base_dir, 'static','report', 'tpl.docx')  # 下载文件的绝对路径
            # file_path2 = os.path.join(base_dir, 'static','report', '2_group2_8.docx')  # 下载文件的绝对路径
            # doc = DocxTemplate(file_path) #加载模板文件
            # doc.render(data_dic) #填充数据
            # doc.save(file_path2) #保存目标文件

            # report = Report(id='8',system_score=87,teacher_score=-1,url='2_group2_8.docx',owner_id=2,experiment_id=2)
            # report.save()

            return Response({
                "status": 200,
                "msg": '返回成功',
            })

        except Exception as e:
            return Response({
                'status': 204,
                'msg': '遇到了异常错误',
                'err': e.args
            })
