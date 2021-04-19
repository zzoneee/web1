# from __future__ import unicode_literals
# import io
# from openpyxl import Workbook, load_workbook
# from openpyxl.writer.excel import save_virtual_workbook, ExcelWriter

# from django.shortcuts import render
# from django.http import HttpResponse,JsonResponse
# from ex.models import Student,Group
# from django.core import serializers


from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
# from plane.models import User, Student, LightList, Light, Score, Visit
# from plane.utils.jwt_auth import create_token, get_user_id
# from django.contrib.auth.hashers import make_password, check_password

import os
from django.http import StreamingHttpResponse


import xlrd

# Create your views here.

class file_downView(APIView):
    def get(self, request, *args, **kwargs):
        """
        下载压缩文件
        :param request:
        :param id: 数据库id
        :return:
        """
        path = request.path
        path_vals = path.split('/')
        file_name = path_vals[-2] # 文件名
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
        length = len(base_dir)
        for i in range(length - 2,0,-1):
            if base_dir[i] == '\\':
                base_dir = base_dir[0:i]
                break
        file_path = os.path.join(base_dir, 'static','report', file_name)  # 下载文件的绝对路径
        # print(file_path)

        if not os.path.isfile(file_path):  # 判断下载文件是否存在
            return HttpResponse("Sorry but Not Found the File")

        def file_iterator(file_path, chunk_size=512):
            """
            文件生成器,防止文件过大，导致内存溢出
            :param file_path: 文件绝对路径
            :param chunk_size: 块大小
            :return: 生成器
            """
            with open(file_path, mode='rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        try:
            # 设置响应头
            # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
            response = StreamingHttpResponse(file_iterator(file_path))
            # 以流的形式下载文件,这样可以实现任意格式的文件下载
            response['Content-Type'] = 'application/octet-stream'
            # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
        except Exception as e:
            return HttpResponse("Sorry but Not Found the File" + file_path)

        return response

# def create_excel_import(path, sheet_name='', ignore_header=0):
#     """
#     加载导入的excel数据
#     :param path: 文件地址
#     :param sheet_name: 获取指定sheet，默认加载全部
#     :param ignore_header: 是否忽略表头数据，即第一行，默认否
#     :return: 返回数组集
#     """
#     wb = load_workbook(path)
#     exl_all = list()
#     print(wb.sheetnames)
#     if sheet_name:
#         exl_all = read_sheet(wb.get_sheet_by_name(sheet_name), ignore_header)
#     else:
#         for sheet in wb.sheetnames:
#             data = read_sheet(wb.get_sheet_by_name(sheet), ignore_header)
#             if len(data) != 0 and data != [[None]]:
#                 exl_all.append(data)
#     return exl_all

class uploadStuMsgView(APIView):
    def post(self, request, *args, **kwargs):
        """
        下载压缩文件
        :param request:
        :param id: 数据库id
        :return:
        """
        path = request.path
        path_vals = path.split('/')
        file_name = path_vals[-2] # 文件名
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
        length = len(base_dir)
        for i in range(length - 2,0,-1):
            if base_dir[i] == '\\':
                base_dir = base_dir[0:i]
                break
        file_path = os.path.join(base_dir, 'static','stuMsgXlsx', file_name)  # 下载文件的绝对路径

        if not os.path.isfile(file_path):  # 判断下载文件是否存在
            return HttpResponse("Sorry but Not Found the File")

        def file_iterator(file_path, chunk_size=512):
            """
            文件生成器,防止文件过大，导致内存溢出
            :param file_path: 文件绝对路径
            :param chunk_size: 块大小
            :return: 生成器
            """
            with open(file_path, mode='rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        try:
            # 设置响应头
            # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
            response = StreamingHttpResponse(file_iterator(file_path))
            # 以流的形式下载文件,这样可以实现任意格式的文件下载
            response['Content-Type'] = 'application/octet-stream'
            # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
        except Exception as e:
            return HttpResponse("Sorry but Not Found the File" + file_path)

        return response
