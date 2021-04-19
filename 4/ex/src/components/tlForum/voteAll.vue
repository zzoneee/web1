<template>
    <div class="systemNotificationContainer">
        <el-scrollbar style="width:866px;height:99%;margin-left:20px;">
            <li v-for="item in voteLists">
                <div class="replyCon">
                    <div class="replyAll">
                        <div class="vtoptag">
                            <el-button v-if="item.isOver==1" type="danger" size='mini'>已结束</el-button>
                            <el-button v-if="item.isOver==0" type="success" size='mini'>进行中</el-button>
                            <el-button v-if="item.answer==0&&item.isOver==1" type="info" size='mini'>人</el-button>
                            <el-button v-if="item.answer==1&&item.isOver==1" type="warning" size='mini'>AI</el-button>
                            <!-- <el-button v-if="item.isVote!=-1&&item.isOver==1" type="success" size='mini' style="float:right">提交实验数据</el-button> -->
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
                            <el-button v-if="item.isVote==-1&&item.isOver==0&&item.group_id==group_id" type="primary" size='mini' @click="toVote(item.id)">投票</el-button>
                            <el-button v-if="item.isVote==0" type="primary" size='mini'>已投票：人</el-button>
                            <el-button v-if="item.isVote==1" type="primary" size='mini'>已投票：AI</el-button>
                            <el-button v-if="item.isVote==-1&&item.isOver==1&&item.group_id==group_id" type="primary" size='mini'>未投票</el-button>
                            <el-button v-if="item.isVote==-1&&item.isOver==0&&item.group_id!=group_id" type="primary" size='mini' @click="toVote(item.id)">参与投票</el-button>
                            <el-button v-if="item.isVote==-1&&item.isOver==1&&item.group_id!=group_id" type="primary" size='mini'>已结束</el-button>
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

    </div>
</template>

<script>
    import axios from 'axios'
    export function get_voteLists(group_id) {
        return axios({
            method: 'get',
            url: "/api/TLForum/voteLists",
            headers: {'Authorization': window.localStorage['Authorization']},
            params: {group_id: group_id}
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
    export default {
        data() {
            return {
                group_id: this.$route.query.group,
                voteLists: [],
                voteFormVisible: false,

                toVoteFormVisible: false,
                toVoteRadio: 0, // 0：人；1：AI
                tlVote_id: 0,
            }
        },
        created() {
            this.getVoteLists();
        },
        mounted () {
            // this.drawLine();
        },
        methods:{
            getVoteLists(){
                get_voteLists(this.group_id).then(res => {
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
                    // console.log(res.data.status);
                    if(res.data.status == 200){
                        this.getVoteLists();
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
</style>

<style>
    .toVoteDialog{
        width: 450px;
    }
</style>
