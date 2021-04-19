<template>
    <div class="systemNotificationContainer">
        <el-scrollbar style="width:866px;height:99%;margin-left:20px;">
            <li v-for="item in voteLists">
                <div class="replyCon">
                    <div class="replyAll">
                        <div class="vtoptag">
                            <el-button v-if="item.isOver==1" type="danger" size='mini'>已截止</el-button>
                            <el-button v-if="item.isOver==0" type="success" size='mini'>进行中</el-button>
                            <el-button v-if="item.answer==0&&item.isOver==1" type="info" size='mini'>人</el-button>
                            <el-button v-if="item.answer==1&&item.isOver==1" type="warning" size='mini'>AI</el-button>
                            <el-button v-if="item.isVote!=-1&&item.isOver==1" type="success" size='mini' style="float:right" @click="submitReport(item.id,item.isVote,item.answer,item.result0,item.result1,item.time,item.endTime,item.diff,item.title,item.tlPost_idMessage,item.tlComment_idMessage)">提交实验报告</el-button>
                        </div>
                        <el-divider></el-divider>
                        <div>
                            <el-tag class="vtitle1" plain>帖子标题</el-tag>
                            <!-- <span class="vtitle1">帖子标题</span> -->
                            <span class="vtitle2">{{ item.title }}</span>
                        </div>
                        <div class="vtop">
                            <el-tag class="vtitle1" plain>帖子内容</el-tag>
                            <!-- <span class="vtitle1">帖子内容</span> -->
                            <span class="vtitle2">{{ item.tlPost_idMessage }}</span>
                        </div>
                        <div class="vtop">
                            <el-tag class="vtitle1" plain>评论内容</el-tag>
                            <!-- <span class="vtitle1">评论内容</span> -->
                            <span class="vtitle2">{{ item.tlComment_idMessage }}</span>
                        </div>
                        <el-divider></el-divider>
                        <div>
                            <span>投票人数：{{ item.num }}</span>
                            <el-button type="success" style="margin-left: 15px" size='mini' @click="voteDetail(item.id)">投票详情</el-button>
                            <el-button v-if="item.isVote==-1&&item.isOver==0" type="primary" size='mini' @click="toVote(item.id)">投票</el-button>
                            <el-button v-if="item.isVote==0" type="primary" size='mini'>已投票：人</el-button>
                            <el-button v-if="item.isVote==1" type="primary" size='mini'>已投票：AI</el-button>
                            <el-button v-if="item.isVote==-1&&item.isOver==1" type="primary" size='mini'>未投票</el-button>
                            <!-- <el-tag type="warning" style="float: right">标签四</el-tag> -->
                        </div>
                        <div class="vbottomCon">
                            <span class="vbottom">发起人：{{ item.group_name }}</span>
                            <span class="vbottom" style="margin-left: 15px">投票开始时间：{{ item.time }}</span>
                            <span class="vbottom" style="margin-left: 15px">投票结束时间：{{ item.endTime }}</span>
                        </div>
                    </div>
                </div>
            </li>
        </el-scrollbar>

        <el-dialog customClass="releaseDialog" title="投票详情" :visible.sync="voteFormVisible"  @closed="votehandleClose" :append-to-body="true">
            <div id="myChart" :style="{width: '300px', height: '200px'}"></div>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="votehandleSave">确定</el-button>
            </div>
        </el-dialog>
        
        <el-dialog customClass="toVoteDialog" title="投票" :visible.sync="toVoteFormVisible"  @closed="toVotehandleClose" :append-to-body="true">
            <!-- <div id="myChart" :style="{width: '300px', height: '200px'}"></div> -->
            <el-radio-group v-model="toVoteRadio" class="toVoteDialogRadio">
                <el-radio :label="0">人</el-radio>
                <el-radio :label="1">AI</el-radio>
            </el-radio-group>
            <div slot="footer" class="dialog-footer">
                <el-button @click="toVoteFormVisible = false">取消</el-button>
                <el-button type="primary" @click="toVotehandleSave">确定</el-button>
            </div>
        </el-dialog>

        <el-dialog customClass="createGroupDialog" title="提交实验报告" :visible.sync="dialogFormVisible"  @closed="handleClose" :append-to-body="true">
            <el-form :model="form" :rules="rules" ref="ruleForm">
                
                <el-form-item label="实验名称" :label-width="formLabelWidth" prop="exName">
                    <el-input :disabled="true" v-model="form.exName" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="团队名称" :label-width="formLabelWidth" prop="groupName">
                    <el-input :disabled="true" v-model="form.groupName" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="团队成员信息" :label-width="formLabelWidth" prop="groupNumberMsg">
                    <!-- <el-input :disabled="true" v-model="form.groupNumberMsg" autocomplete="off"></el-input> -->
                    <el-input type="textarea" :disabled="true" :rows="2" maxlength="500" show-word-limit v-model="form.groupNumberMsg" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                <el-form-item label="实验目的" :label-width="formLabelWidth" prop="exPurpose">
                    <!-- <el-input :disabled="true" v-model="form.exPurpose" autocomplete="off"></el-input> -->
                    <el-input type="textarea" :disabled="true" :rows="2" maxlength="500" show-word-limit v-model="form.exPurpose" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                <el-form-item label="实验主要步骤" :label-width="formLabelWidth" prop="exSteps">
                    <!-- <el-input :disabled="true" v-model="form.exSteps" autocomplete="off"></el-input> -->
                    <el-input type="textarea" :disabled="true" :rows="2" maxlength="500" show-word-limit v-model="form.exSteps" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                <el-form-item label="实验结果" :label-width="formLabelWidth" prop="exResult" class="exMsg2">
                    <!-- <el-input v-model="form.exResult" autocomplete="off" class="createGroupDiagInput"></el-input> -->
                    <el-input type="textarea" :disabled="true" :rows="2" maxlength="500" show-word-limit v-model="form.exResult" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                <el-form-item label="系统评分" :label-width="formLabelWidth" prop="systemScore">
                    <el-input :disabled="true" v-model="form.systemScore" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="实验心得" :label-width="formLabelWidth" prop="exExperience" class="exMsg2">
                    <!-- <el-input v-model="form.exExperience" autocomplete="off" class="createGroupDiagInput"></el-input> -->
                    <el-input type="textarea" :rows="2" maxlength="500" show-word-limit v-model="form.exExperience" autocomplete="off" class="createGroupDiagInput"></el-input>
                </el-form-item>
                <el-form-item label="实验日期" :label-width="formLabelWidth" prop="exDate">
                    <el-input :disabled="true" v-model="form.exDate" autocomplete="off"></el-input>
                </el-form-item>
                
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleSave">提交</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    import axios from 'axios'
    export function get_voteLists() {
        return axios({
            method: 'get',
            url: "/api/TLForum/voteLists",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export function get_myVoteLists(group_id) {
        return axios({
            method: 'get',
            url: "/api/TLForum/myVoteLists",
            headers: {'Authorization': window.localStorage['Authorization']},
            params: {group_id: group_id}
        })
    }
    export function post_toVote(group_id, result, tlVote_id) {
        return axios({
            method: 'post',
            url: "/api/TLForum/toVote",
            headers: {'Authorization': window.localStorage['Authorization']},
            data: {group_id: group_id, result: result, tlVote_id: tlVote_id}
        })
    }
    export function get_voteDetail(tlVote_id) {
        return axios({
            method: 'get',
            url: "/api/TLForum/voteDetail",
            headers: {'Authorization': window.localStorage['Authorization']},
            params: {tlVote_id: tlVote_id}
        })
    }
    export function get_exName(ex_id) {
        return axios({
            method: 'get',
            url: "/api/experiment/getExName",
            headers: {'Authorization': window.localStorage['Authorization']},
            params: {ex_id: ex_id}
        })
    }
    export function get_getGroupName(group_id) {
        return axios({
            method: 'get',
            url: "/api/user/getGroupName",
            headers: {'Authorization': window.localStorage['Authorization']},
            params: {group_id: group_id}
        })
    }
    export function get_getGroupNumbersMsg(group_id) {
        return axios({
            method: 'get',
            url: "/api/user/getGroupNumbersMsg",
            headers: {'Authorization': window.localStorage['Authorization']},
            params: {group_id: group_id}
        })
    }
    export function post_createReport(form) {
        return axios({
            method: 'post',
            url: "/api/report/createReport",
            headers: {'Authorization': window.localStorage['Authorization']},
            data:{form: form}
        })
    }
    export default {
        data() {
            return {
                group_id: this.$route.query.group,
                ex_id: this.$route.query.ex,
                voteLists: [],
                voteFormVisible: false,

                toVoteFormVisible: false,
                toVoteRadio: 0, // 0：人；1：AI
                tlVote_id: 0,

                dialogFormVisible: false,
                form: {
                    exName: '',
                    groupName: '',
                    groupNumberMsg: '张三/计算机171/2020003/项目统筹\n王五/计算机174/2020012/算法研究',
                    exPurpose: '根据某一用户的评论，判断这个用户是人还是AI。',
                    // exSteps: '1.可以在论坛上寻找一个帖子中的一条回复并发起投票，也可以在投票活动中寻找别人发起的投票。\n2.',
                    exSteps: '',
                    exResult: '',
                    systemScore: '',
                    exExperience: '',
                    exDate: '',

                    time: '',
                    experiment_id: this.$route.query.ex,
                    group_id: this.$route.query.group,
                },
                rules: {
                    // exResult: [
                    //     { message: '请输入实验结果', required: true, trigger: 'blur' },
                    //     { min: 0, max: 500, message: '长度应小于 500 个字符', trigger: 'blur' }
                    // ],
                    exExperience: [
                        { message: '请输入实验心得', required: true, trigger: 'blur' },
                        { min: 0, max: 500, message: '长度应小于 500 个字符', trigger: 'blur' }
                    ],
                },
                formLabelWidth: '120px',
            }
        },
        created() {
            this.getMyVoteLists();
            this.getExName(this.ex_id);
            this.getGroupName();
            this.getGroupNumbersMsg();
        },
        mounted () {
            // this.drawLine();
        },
        methods:{
            getGroupNumbersMsg(){
                get_getGroupNumbersMsg(this.group_id).then(res => {
                    // console.log(res.data.data);
                    if(res.data.status == 200){
                        // this.form.groupName = res.data.data;
                        // 张三/计算机171/2020003/项目统筹
                        // console.log(res.data.data);

                        this.form.groupNumberMsg = '';
                        let cnt = 1
                        res.data.data.forEach(item=>{
                            if(cnt != 1){
                                this.form.groupNumberMsg += '\n';
                            }
                            this.form.groupNumberMsg += '队员' + String(cnt) + '：' + '姓名：' + item.name + '   学院：' + item.college + '   班级：' + item.class_name + '   学号：' + item.stu_num + '   承担角色：' + item.role;
                            cnt++;
                        });
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            getGroupName(){
                get_getGroupName(this.group_id).then(res => {
                    // console.log(res.data.data);
                    if(res.data.status == 200){
                        this.form.groupName = res.data.data;
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            getExName(ex_id){
                get_exName(ex_id).then(res => {
                    // console.log(res.data.data);
                    if(res.data.status == 200){
                        this.form.exName = res.data.data;
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                    else{
                        console.log(res.data.err);
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            getMyVoteLists(){
                get_myVoteLists(this.group_id).then(res => {
                    // console.log(res.data.data);
                    if(res.data.status == 200){
                        this.voteLists = res.data.data;
                        // console.log(this.voteLists);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                    else{
                        console.log(res.data.err);
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            // 绘图
            drawLine(data){
                // 新建一个promise对象
                let newPromise = new Promise((resolve) => {
                    resolve()
                })
                //然后异步执行echarts的初始化函数
                newPromise.then(() => {
                    //	此dom为echarts图标展示dom
                    // echarts.init(DOm)
                

                // 基于准备好的dom，初始化echarts实例
                let myChart = this.$echarts.init(document.getElementById('myChart'));
                // 绘制图表
                myChart.setOption({
                    title: {
                        text: '投票结果',
                        // subtext: '纯属虚构',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                    },
                    series: [
                        {
                            name: '投票人数',
                            type: 'pie',
                            radius: '50%',
                            data: [
                                {value: data.result0, name: '人'},
                                {value: data.result1, name: 'AI'},
                            ],
                            emphasis: {
                                itemStyle: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }
                    ]
                });

                })
            },
            voteDetail(id){
                // this.drawLine();
                get_voteDetail(id).then(res => {
                    // console.log(res.data.data);
                    if(res.data.status == 200){
                        this.voteFormVisible = true;
                        this.drawLine(res.data.data);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                    else{
                        console.log(res.data.err);
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            votehandleClose () {
                this.voteFormVisible = false;
            },
            votehandleSave () {
                this.voteFormVisible = false;
            },
            toVote(id){
                this.tlVote_id = id;
                this.toVoteFormVisible = true;
            },
            toVotehandleClose () {
                // this.$refs.commentruleForm.resetFields();
                this.toVoteRadio = 0;
            },
            toVotehandleSave () {
                post_toVote(this.group_id, this.toVoteRadio, this.tlVote_id).then(res => {
                    if(res.data.status == 200){
                        this.getMyVoteLists();
                        this.toVoteFormVisible = false;
                        this.$message.success("投票成功");
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error');
                    }
                    else{
                        console.log(res.data.err);
                        this.$message.error("投票失败，" + res.data.msg);
                    }
                }).catch( error =>{
                    console.log(error);
                    this.$message.error("投票失败");
                });
            },
            handleClose () {
                this.$refs.ruleForm.resetFields();
                this.form.exResult = '';
                this.form.exExperience = '';
            },
            handleSave () {
                this.$refs.ruleForm.validate((valid) => {
                    if (valid) {
                        this.createReport(this.form);
                    } else {
                        this.$message.error("提交失败");
                    }
                })
            },
            submitReport(id,isVote,answer,result0,result1,time,endTime,diff,title,tlPost_idMessage,tlComment_idMessage){
                this.getExSteps(isVote,answer,result0,result1,time,endTime,diff,title,tlPost_idMessage,tlComment_idMessage);
                this.getExResult(isVote,answer,result0,result1,time,endTime,diff,title,tlPost_idMessage,tlComment_idMessage);
                this.getSystemScore(isVote,answer,result0,result1,time,endTime,diff,title,tlPost_idMessage,tlComment_idMessage);
                this.getExDate(endTime);
                this.dialogFormVisible = true;
            },
            createReport(form){
                post_createReport(form).then(res => {
                    // console.log(res.data.err);
                    if(res.data.status == 200){
                        this.dialogFormVisible = false;
                        this.$message.success("提交成功");
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                    else{
                        this.$message.error("提交失败");
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            // 实验步骤
            getExSteps(isVote,answer,result0,result1,time,endTime,diff,title,tlPost_idMessage,tlComment_idMessage){
                // 1.可以在论坛上寻找一个帖子中的一条回复并发起投票，也可以在投票活动中寻找别人发起的投票。\n2.
                this.form.exSteps = '';
                // this.form.exSteps += '1.可以在论坛上寻找一个帖子中的一条评论并发起投票，也可以在投票活动中寻找别人发起的投票。\n';
                this.form.exSteps += '1.发起或参与一次投票。\n';
                this.form.exSteps += '2.根据已知信息，推测评论者的身份，并投票。\n';
                this.form.exSteps += 'a.该实验步骤考察点：考察用户能不能根据帖子内容和用户的评论内容，推测发表该评论的用户是‘人’还是‘AI’。\n';
                this.form.exSteps += '本团队本次实验的投票信息如下：\n帖子标题：' + title + '\n帖子内容：' + tlPost_idMessage + '\n评论内容：' + tlComment_idMessage + '\n';
                this.form.exSteps += 'b.该实验步骤开始时间：' + time + '，结束时间：' + endTime + '，实验用时：' + diff + '分钟，合理用时：60分钟以内；\n';
                this.form.exSteps += 'c.该实验步骤次数：1次；\n';
                this.form.exSteps += 'd.该实验步骤评价：有' + result0 + '人投票给了‘人’，有' + result1 + '人投票给了‘AI’，本团队投票给了';
                if(isVote == 0){
                    this.form.exSteps += '‘人’';
                }
                else{
                    this.form.exSteps += '‘AI’';
                }
                this.form.exSteps += '，正确答案为';
                if(answer == 0){
                    this.form.exSteps += '‘人’';
                }
                else{
                    this.form.exSteps += '‘AI’';
                }
                this.form.exSteps += '，本团队推测';
                if(answer == isVote){
                    this.form.exSteps += '成功；\n';
                }
                else{
                    this.form.exSteps += '失败；\n';
                }
                this.form.exSteps += 'e.该实验步骤满分：100，本团队得分：';
                if(answer == isVote){
                    this.form.exSteps += '100。';
                }
                else{
                    let score = 80;
                    if(answer == 0){
                        score = Math.trunc(result1 / (result0 + result1) * 80);
                    }
                    else{
                        score = Math.trunc(result0 / (result0 + result1) * 80);
                    }
                    this.form.exSteps += score + '。';
                }
            },
            // 实验结果
            getExResult(isVote,answer,result0,result1,time,endTime,diff,title,tlPost_idMessage,tlComment_idMessage){
                this.form.exResult = '';
                this.form.exResult += '在本次实验中，有' + result0 + '人投票给了‘人’，有' + result1 + '人投票给了‘AI’';
                this.form.exResult += '，正确答案为';
                if(answer == 0){
                    this.form.exResult += '‘人’';
                }
                else{
                    this.form.exResult += '‘AI’';
                }
                this.form.exResult += '，本次投票的正确率为'
                if(answer == 0){
                    this.form.exResult += Math.trunc(result0 / (result0 + result1) * 100);
                }
                else{
                    this.form.exResult += Math.trunc(result1 / (result0 + result1) * 100);
                }
                this.form.exResult += '%，本团队投票给了'
                if(isVote == 0){
                    this.form.exResult += '‘人’';
                }
                else{
                    this.form.exResult += '‘AI’';
                }
                this.form.exResult += '，本团队推测';
                if(answer == isVote){
                    this.form.exResult += '成功。\n';
                }
                else{
                    this.form.exResult += '失败。\n';
                }
            },
            // 系统评分
            getSystemScore(isVote,answer,result0,result1,time,endTime,diff,title,tlPost_idMessage,tlComment_idMessage){
                if(answer == isVote){
                    this.form.systemScore = 100;
                }
                else{
                    let score = 80;
                    if(answer == 0){
                        score = Math.trunc(result1 / (result0 + result1) * 80);
                    }
                    else{
                        score = Math.trunc(result0 / (result0 + result1) * 80);
                    }
                    this.form.systemScore = score;
                }
            },
            // 实验日期
            getExDate(endTime){
                this.form.exDate = '';
                let len = endTime.length;
                for(let i = 0;i < len;i++){
                    if(endTime[i] == ' '){
                        break;
                    }
                    this.form.exDate += endTime[i];
                }

                this.form.time = endTime;
            },
        },
    }
</script>

<style scoped>
    
    .systemNotificationContainer{
        height: 635px;
        /* margin-left: 20px; */
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    }
    /* 滚动条位置 */
    /deep/.__bar-is-vertical {
        right: -1px !important;
    }
    /* 隐藏横向滚动条 */
    /deep/.__bar-is-horizontal {
        display: none !important;
    }

    .systemNotificationContainer>>>.el-scrollbar__wrap{
        overflow-x: hidden;
    }

    .replyCon{
        width: 850px;
        height: auto;
        margin-top: 5px;
        border:1px solid rgb(241, 240, 240);
        /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); */
        background-color: #fff;
    }
    .replyAll{
        margin: 20px;
    }
    .replyUser{
        font-size: 20px;
        font-weight: 700;
    }
    .replyUser2{
        font-size: 14px;
        color: rgb(103, 102, 102);
    }
    .replySee{
        float: right;;
    }
    .msgText{
        width: 100%;  
        height: auto;  
        word-wrap:break-word;  
        word-break:break-all;  
        overflow: hidden;  
        font-size: 15px;
        color: #323232;
        margin: 0;
        /* font-family: "微软雅黑"; */
        margin-top: 20px;
    }
    .replyBottom{
        margin-top: 20px;
        font-size: 11px;
        color: gray;
    }
    .vtitle1{
        font-size: 14px;
        /* font-weight: 900; */
    }
    .vtitle2{
        font-size: 18px;
        margin-left: 15px;
    }
    .vbottomCon{
        margin-top: 19px;
    }
    .vbottom{
        font-size: 11px;
        color: gray;
    }
    .vtop{
        margin-top: 15px;
    }
    .toVoteDialogRadio{
        /* text-align: center; */
        margin-left: 135px;
    }
    #myChart{
        margin-left: 215px;
        margin-top: 15px;
    }
    /* .vtoptag{
        margin-bottom: 20px;
    } */

    .createGroupDiagInput>>>.el-textarea__inner {
        /* border: 0; */
        resize: none;/* 这个是去掉 textarea 下面拉伸的那个标志，如下图 */
        height: 150px;
        overflow-y: auto;
    }
</style>

<style>
    .toVoteDialog{
        width: 450px;
    }
    .createGroupDialog{
        width: 900px;
    }
</style>
