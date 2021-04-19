from django.db import models

# Create your models here.

# 教师
class Teacher(models.Model):
	id = models.CharField(max_length=20, primary_key=True)
	password = models.CharField(max_length=255)
	name = models.CharField(max_length=20, null=True)
	college = models.CharField(max_length=20, null=True)
	phone = models.CharField(max_length=20, null=True)
	
# 团队
class Group(models.Model):
	id = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=20, null=True)

# 学生
class Student(models.Model):
	# id = models.CharField(max_length=20, primary_key=True)
	stu_num = models.CharField(max_length=20)
	password = models.CharField(max_length=255)
	name = models.CharField(max_length=20, null=True)
	college = models.CharField(max_length=20, null=True)
	class_name = models.CharField(max_length=20, null=True)
	phone = models.CharField(max_length=20, null=True)
	role = models.CharField(max_length=20, null=True)
	group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)

# 实验报告
class Report(models.Model):
	id = models.CharField(max_length=20, primary_key=True)
	# ex_name = models.CharField(max_length=255)
	system_score = models.IntegerField(default=-1)
	teacher_score = models.IntegerField(default=-1)
	url = models.CharField(max_length=255, blank=True, null=True)
	create_time = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey('Group', on_delete=models.CASCADE)
	experiment = models.ForeignKey('experiment', on_delete=models.CASCADE, null=True)

# 团队互评
class TeamEvaluation(models.Model):
	Rater_ID = models.CharField(max_length=20) # 评分人
	Ratee_ID = models.CharField(max_length=20) # 被评分人
	score = models.IntegerField(default=-1)

# 编队
class Formation(models.Model):
	owner = models.ForeignKey('Group', on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	plane_cnt = models.IntegerField(default=0)

# 飞机
class Plane(models.Model):
	formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
	x = models.IntegerField(default=0)
	y = models.IntegerField(default=0)
	z = models.IntegerField(default=0)

# 路线（从一个编队到另一个编队）
class FormationPath(models.Model):
	# owner = models.ForeignKey('Group', on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=255)
	start_formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="start_formation",null=True)
	end_formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="end_formation", null=True)
	time_tot = models.IntegerField(default=5) # 用时
	direction = models.CharField(max_length=255, null=True) # 方向
	speed = models.FloatField(default=0) # 速度

# 灯光方案
class LightScheme(models.Model):
	name = models.CharField(max_length=255)
	formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
	# owner = models.ForeignKey('Group', on_delete=models.CASCADE)

# 灯光序列
class LightList(models.Model):
	name = models.CharField(max_length=255)
	# color1 = models.ForeignKey('Light', on_delete=models.CASCADE, related_name="color1")
	# color2 = models.ForeignKey('Light', on_delete=models.CASCADE, related_name="color2")
	# color3 = models.ForeignKey('Light', on_delete=models.CASCADE, related_name="color3")
	# color4 = models.ForeignKey('Light', on_delete=models.CASCADE, related_name="color4")
	time = models.IntegerField(default=1) # 亮灯时间
	# owner = models.ForeignKey('Group', on_delete=models.CASCADE)
	lightScheme = models.ForeignKey('LightScheme', on_delete=models.CASCADE)

# 灯光
class Light(models.Model):
	name = models.CharField(max_length=20)
	RGB = models.CharField(max_length=20)

# 灯光序列和灯光对应表
class LightListLight(models.Model):
	lightList = models.ForeignKey('LightList', on_delete=models.CASCADE)
	light = models.ForeignKey('Light', on_delete=models.CASCADE)

# 实验三
# 设备
class Equipment(models.Model):
	id = models.CharField(max_length=20, primary_key=True) # 卡口编号
	equipmentType = models.CharField(max_length=1) # 卡口类型
	place = models.CharField(max_length=255) # 坐标
	direction = models.CharField(max_length=255, null=True) # 路段方向

# 车辆
class Car(models.Model):
	license_plate_number = models.CharField(max_length=20, primary_key=True) # 车牌号
	url = models.CharField(max_length=255, blank=True, null=True) # 车辆图片

# 车辆经过设备记录表
class CarEquipment(models.Model):
	equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
	car = models.ForeignKey('Car', on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True) # 车辆经过设备的时间

# 公告
class Notice(models.Model):
	title = models.CharField(max_length=31) # 标题
	message = models.CharField(max_length=511) # 公告内容
	time = models.DateTimeField(auto_now_add=True) # 发布时间
	top = models.IntegerField(default=0) # 是否置顶（0：不置顶；1：置顶）
	user = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True) # 发布人

# 是否为未读公告（教师）
class TeacherNewNotice(models.Model):
	notice = models.ForeignKey(Notice, on_delete=models.CASCADE,null=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True)
	new = models.IntegerField(default=1) # 是否未读（0：已读；1：未读）

# 是否为未读公告（学生）
class StudentNewNotice(models.Model):
	notice = models.ForeignKey(Notice, on_delete=models.CASCADE,null=True)
	student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
	new = models.IntegerField(default=1) # 是否未读（0：已读；1：未读）

# 私信
class PrivateLetter(models.Model):
	message = models.CharField(max_length=511) # 私信内容
	senderStu = models.ForeignKey(Student, on_delete=models.CASCADE,related_name = 'senderStu_id',null=True)
	senderTea = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name = 'senderTea_id',null=True)
	receiverStu = models.ForeignKey(Student, on_delete=models.CASCADE,related_name = 'receiverStu_id',null=True)
	receiverTea = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name = 'receiverTea_id',null=True)
	time = models.DateTimeField(auto_now_add=True) # 发送时间
	new = models.IntegerField(default=1) # 是否未读（0：已读；1：未读）

# 私信（与别人的聊天框是否打开）
class ChatBoxIsOpen(models.Model):
	senderStu = models.ForeignKey(Student, on_delete=models.CASCADE,related_name = 'senderStuIsOpen_id',null=True)
	senderTea = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name = 'senderTeaIsOpen_id',null=True)
	receiverStu = models.ForeignKey(Student, on_delete=models.CASCADE,related_name = 'receiverStuIsOpen_id',null=True)
	receiverTea = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name = 'receiverTeaIsOpen_id',null=True)
	isOpen = models.IntegerField(default=1) # 聊天框是否打开（0：不打开；1：打开）

# 帖子
class Post(models.Model):
	userStu = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
	userTea = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True)
	title = models.CharField(max_length=31) # 标题
	message = models.CharField(max_length=511) # 帖子内容
	time = models.DateTimeField(auto_now_add=True) # 发布时间

# 评论
class Comment(models.Model):
	userStu = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
	userTea = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
	message = models.CharField(max_length=511) # 评论内容
	time = models.DateTimeField(auto_now_add=True) # 发布时间

# 点赞
class ThumbsUp(models.Model):
	userStu = models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
	userTea = models.ForeignKey(Teacher, on_delete=models.CASCADE,null=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)

# 实验
class experiment(models.Model):
	name = models.CharField(max_length=21) # 实验名称
	url = models.CharField(max_length=255, blank=True, null=True) #实验所在位置
	introduction = models.CharField(max_length=2047, blank=True, null=True) #实验简介
	introductionUrl = models.CharField(max_length=255, blank=True, null=True) #实验简介地址

# 班级
class Classes(models.Model):
	name = models.CharField(max_length=21, null=True) # 班级名称
	college = models.CharField(max_length=20, null=True) # 学院

# 实验数据
class experimentData(models.Model):
	experiment = models.ForeignKey(experiment, on_delete=models.CASCADE,null=True) # 实验
	group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True) # 团队
	report = models.ForeignKey(Report, on_delete=models.CASCADE,null=True) # 实验报告
	exPurpose = models.CharField(max_length=512, null=True) # 实验目的
	systemScore = models.IntegerField(default=-1) # 系统得分
	time = models.DateTimeField(auto_now_add=True) # 实验报告提交时间
	exSteps = models.CharField(max_length=512, null=True) # 实验主要步骤
	exResult = models.CharField(max_length=512, null=True) # 实验结果
	exExperience = models.CharField(max_length=512, null=True) # 实验心得
	exTime = models.CharField(max_length=512, null=True) # 实验时间

# 登录记录
class loginRecord(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True) # 用户ID
	time = models.DateTimeField(auto_now_add=True) # 登录时间

# 图灵测试论坛
# 帖子
class TLPost(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
	title = models.CharField(max_length=31) # 标题
	message = models.CharField(max_length=511) # 帖子内容
	time = models.DateTimeField(auto_now_add=True) # 发布时间

# 评论
class TLComment(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True)
	tlPost = models.ForeignKey(TLPost, on_delete=models.CASCADE,null=True)
	message = models.CharField(max_length=511) # 评论内容
	time = models.DateTimeField(auto_now_add=True) # 发布时间

# 投票活动
class TLVote(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True) # 发起团队
	time = models.DateTimeField(auto_now_add=True) # 发起时间
	tlComment = models.ForeignKey(TLComment, on_delete=models.CASCADE,null=True) # 被投票的评论
	endTime = models.DateTimeField(null=True) # 活动结束时间

# 用户投票
class TLGroupVote(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True) # 投票团队
	tlVote = models.ForeignKey(TLVote, on_delete=models.CASCADE,null=True) # 投票活动
	result = models.IntegerField(null=True) # 投票结果；0：人；1：ai
