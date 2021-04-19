<template>
    <div class="systemNotificationContainer">
        <div class="systemNotificationTop">
            <el-tag effect="plain" type="success" class="systemNotificationTag">讨论区评论</el-tag>
        </div>
        <el-divider></el-divider>
        <el-scrollbar style="width:866px;height:100%;margin-left:20px;">
            <li v-for="item in replyLists">
                <!-- <el-card class="msgCard" shadow="hover">
                    <div slot="header" class="clearfix">
                        <el-tag type="success" v-if="item.new==1">new</el-tag>
                        <el-tag type="danger" v-if="item.top==1">置顶</el-tag>
                        <span class="msgCardHeader">{{ item.title }}</span>
                        <span class="publishUser">发布人：{{item.user_id}}</span>
                        <span class="publishTime">发布时间：{{item.time}}</span>
                    </div>
                    <div class="msgText">
                        <p>{{ item.message }}</p>
                    </div>
                </el-card> -->
                <div class="replyCon">
                    <div class="replyAll">
                        <div class="replyTop">
                            <span class="replyUser">{{ item.user_id }}</span>
                            <span class="replyUser2">评论了我的贴子</span>
                            <el-button type="primary" size="mini" class="replySee" @click="replySee(item)">查看帖子</el-button>
                        </div>
                        <div class="msgText">
                            <p>{{ item.message }}</p>
                        </div>
                        <div class="replyBottom">
                            <span>{{ item.time }}</span>
                        </div>
                    </div>
                </div>
            </li>
        </el-scrollbar>

        <el-drawer
        :title="drawerPost.title"
        :visible.sync="drawer"
        :direction="direction"
        :append-to-body="true"
        :size="drawerSize"
        class="postDrawer">
            <el-scrollbar style="width:100%;height:670px;" ref="myScrollbar2">

                <el-row :gutter="0">
                    <el-col :span="2">
                        <el-avatar class="PostUser"> {{drawerPost.user_id}} </el-avatar>
                    </el-col>
                    <el-col :span="22">
                        <p class="PostUserID">{{drawerPost.user_id}}</p>
                        <p class="PostPublishTime">{{drawerPost.time}}</p>
                    </el-col>
                </el-row>

                <div class="postDrawerMsg">
                    <p class="postDrawerMsgP">{{drawerPost.message}}</p>
                </div>

                <el-button type="primary" plain style="margin-left: 77px;margin-top: 23px;" size="mini" @click="commentClick()">评论</el-button>
                <el-button icon="el-icon-chat-line-round" style="margin-left: 31px;margin-top: 23px;" circle size="mini" plain></el-button>
                <span>{{drawerPost.commentNum}}</span>
                <!-- <el-button type="success" icon="el-icon-caret-top" style="margin-left: 27px;margin-top: 23px;" circle size="mini" plain></el-button>
                <span>3</span> -->
                <el-button class="thumbsUp" v-if="drawerPost.thumbsUp==0" @click="thumbsUp(drawerPost)" type="success" icon="el-icon-caret-top" style="margin-left: 27px" circle size="mini" plain></el-button>
                <el-button class="thumbsUpActive" v-if="drawerPost.thumbsUp==1" @click="thumbsDown(drawerPost)" type="success" icon="el-icon-caret-top" style="margin-left: 27px" circle size="mini" plain></el-button>
                <span>{{ drawerPost.thumbsUpNum }}</span>

                <el-divider></el-divider>

                <h2 class="postDrawerTitleTip">评论</h2>

                <p v-if="numTotal2==0" style="margin-left: 315px;margin-top: 103px;">暂无评论</p>

                <li v-for="item in commentLists">
                    <div class="postDrawerComment">
                        <el-row :gutter="0">
                            <el-col :span="2">
                                <el-avatar class="PostCommenttUser"> {{item.user_id}} </el-avatar>
                            </el-col>
                            <el-col :span="18">
                                <p class="PostCommentUserID">{{item.user_id}}</p>
                                <p class="PostCommentPublishTime">{{item.time}}</p>
                            </el-col>
                            <el-col :span="2">
                                <el-popconfirm title="是否删除？" @confirm="deleteComment(item.id)">
                                    <el-button slot="reference" style="float: right" type="danger" icon="el-icon-delete" circle size="mini"></el-button>
                                </el-popconfirm>
                            </el-col>
                        </el-row>
                        <div class="postCommentMsg">
                            <p class="postCommentMsgP">{{item.message}}</p>
                        </div>
                        <el-divider></el-divider>
                    </div>
                </li>

                <nav aria-label="page_navigation" class="page-bar">
                    <el-pagination background layout="prev, pager, next" :total="numTotal2" :page-size="pageSize2"
                    @prev-click="pre_page2()"
                    @next-click="next_page2()"
                    @current-change="curPage2"
                    :hide-on-single-page="numTotal2<=pageSize2"></el-pagination>
                </nav>
            </el-scrollbar>
            
        </el-drawer>

        <el-dialog customClass="commentDialog" title="评论" :visible.sync="commentFormVisible"  @closed="commenthandleClose" :append-to-body="true">
            <el-form :model="commentform" :rules="commentrules" ref="commentruleForm">
                <el-form-item label="" prop="message" class="releaseMsg">
                    <el-input type="textarea" :rows="2" maxlength="500" show-word-limit v-model="commentform.message" autocomplete="off" class="releaseTextArea"></el-input>
                </el-form-item>
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="commentFormVisible = false">取消</el-button>
                <el-button type="primary" @click="commenthandleSave">确定</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    import axios from 'axios'
    export function get_replyLists() {
        return axios({
            method: 'get',
            url: "/api/posts/replyLists",
            headers: {'Authorization': window.localStorage['tea_Authorization']}
        })
    }
    export function post_commentPost(id, message) {
        return axios({
            method: 'post',
            url: "/api/posts/commentPost",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {id: id, message: message}
        })
    }
    export function get_commentMsg(id, st, ed) {
        return axios({
            method: 'get',
            url: "/api/posts/commentMsg",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            params: {id: id, st: st, ed: ed}
        })
    }
    export function post_deleteComment(id) {
        return axios({
            method: 'post',
            url: "/api/posts/deleteComment",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {id: id}
        })
    }
    export function post_thumbsUp(id) {
        return axios({
            method: 'post',
            url: "/api/posts/thumbsUp",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {id: id}
        })
    }
    export function post_thumbsDown(id) {
        return axios({
            method: 'post',
            url: "/api/posts/thumbsDown",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {id: id}
        })
    }
    export function get_replyPost(id) {
        return axios({
            method: 'get',
            url: "/api/posts/replyPost",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            params: {id: id}
        })
    }
    export default {
        data() {
            return {
                replyLists: [],
                drawer: false,
                direction: 'rtl',
                drawerSize: '700px',
                drawerPost: {},

                commentLists: [],
                numTotal2:0, // 信息总数
                pageNo2:1, // 现在在第几页
                pageSize2:5, // 每一页的信息数

                commentFormVisible: false,
                commentform: {
                    message: ''
                },
                commentrules: {
                    message: [
                        { required: true,  message: '请输入内容', trigger: 'blur' },
                        { min: 1, max: 500, message: '长度应小于 500 个字符', trigger: 'blur' }
                    ],
                },
                formLabelWidth: '120px',

            }
        },
        created() {
            this.getReplyLists();
        },
        methods:{
            scrollUp2() {
                this.$refs['myScrollbar2'].wrap.scrollTop = 0;
            },
            getReplyLists(){
                get_replyLists().then(res => {
                    if(res.data.status == 200){
                        // console.log(res.data.data);
                        this.replyLists = res.data.data
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                    else{
                        console.log(res.data.err);
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            replySee(post){
                this.commentLists = [];
                this.numTotal2 = 0;
                this.pageNo2 = 1;
                this.pageSize2 = 5;
                // console.log(post);
                get_replyPost(post.post_id).then(res => {
                    console.log(res.data.err);
                    if(res.data.status == 200){
                        this.drawerPost = res.data.data;
                        // console.log(this.drawerPost);
                        this.getCommentLists(this.drawerPost.id, (this.pageNo2 - 1) * this.pageSize2 + 1, this.pageNo2 * this.pageSize2);
                        this.drawer = true;
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            getCommentLists(id, st, ed){
                get_commentMsg(id, st, ed).then(res => {
                    // console.log(res.data.status);
                    if(res.data.status == 200){
                        // console.log(res.data.data);
                        this.commentLists = res.data.data.data;
                        this.numTotal2 = res.data.data.numTotal;
                        // console.log(this.commentLists);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            getlist2(index = -1){
                if(index != -1){
                    this.pageNo2 = index;
                }
                this.getCommentLists(this.drawerPost.id, (this.pageNo2 - 1) * this.pageSize2 + 1, this.pageNo2 * this.pageSize2);
                this.scrollUp2();
            },
            pre_page2(){
                if(this.pageNo2 > 1){
                    this.pageNo2--;
                    this.getlist2(this.pageNo2);
                }
            },
            next_page2(){
                // if(this.pageNo2 < this.pageTotal2){
                    this.pageNo2++;
                    this.getlist2(this.pageNo2);
                // }
            },
            curPage2(index){
                this.pageNo2 = index;
                this.getlist2(index);
            },
            deleteComment(id){
                post_deleteComment(id).then(res => {
                    if(res.data.status == 200){
                        if(this.numTotal2 == 1){///////
                            this.commentLists = [];
                        }
                        this.$message.success("删除成功");
                        this.numTotal2--;
                        if(this.numTotal2 % this.pageSize2 == 0 && this.pageNo2 * this.pageSize2 > this.numTotal2){
                            if(this.pageNo2 > 1){
                                this.pageNo2--;
                            }
                        }
                        // this.getPostLists((this.pageNo - 1) * this.pageSize + 1, this.pageNo * this.pageSize, true);
                        this.getCommentLists(this.drawerPost.id, (this.pageNo2 - 1) * this.pageSize2 + 1, this.pageNo2 * this.pageSize2);
                        this.drawerPost.commentNum--;

                        // console.log(this.commentLists,this.numTotal2,this.pageNo2);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                    else{
                        this.$message.error("删除失败");
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            // 点赞
            thumbsUp(post){
                post_thumbsUp(post.id).then(res => {
                    if(res.data.status == 200){
                        // this.getPostLists((this.pageNo - 1) * this.pageSize + 1, this.pageNo * this.pageSize, true);
                        if(this.drawer){
                            this.drawerPost.thumbsUp = 1;
                            this.drawerPost.thumbsUpNum++;
                        }
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            // 取消赞
            thumbsDown(post){
                post_thumbsDown(post.id).then(res => {
                    if(res.data.status == 200){
                        // this.getPostLists((this.pageNo - 1) * this.pageSize + 1, this.pageNo * this.pageSize, true);
                        if(this.drawer){
                            this.drawerPost.thumbsUp = 0;
                            this.drawerPost.thumbsUpNum--;
                        }
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error');
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            commentClick(){
                // console.log(Post.id);
                this.commentFormVisible = true;
            },
            commenthandleClose () {
                this.$refs.commentruleForm.resetFields();
                this.commentform.message = '';
            },
            commenthandleSave () {
                this.$refs.commentruleForm.validate((valid) => {
                    if (valid) {
                        // this.$message.success("发布成功");
                        // console.log(this.form.title, this.form.message);
                        post_commentPost(this.drawerPost.id, this.commentform.message).then(res => {
                            if(res.data.status == 200){
                                this.$message.success("评论成功");
                                this.commentFormVisible = false;
                                this.numTotal2++;
                                // this.getPostLists((this.pageNo - 1) * this.pageSize + 1, this.pageNo * this.pageSize, true);
                                this.getCommentLists(this.drawerPost.id, (this.pageNo2 - 1) * this.pageSize2 + 1, this.pageNo2 * this.pageSize2);
                                this.drawerPost.commentNum++;
                                this.commenthandleClose();
                            }
                            else if(res.data.status == 403){
                                this.$router.replace('/tea_error');
                            }
                            else{
                                this.$message.error("评论失败");
                            }
                        }).catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("评论失败");
                    }
                })
            },
        },
    }
</script>

<style scoped>
    
    .systemNotificationContainer{
        height: 520px;
        /* margin-left: 20px; */
    }
    .systemNotificationTop{
        height: 18px;
    }
    .systemNotificationTag{
        margin-top: 5px;
        margin-left: 20px;
    }
    .msgCard{
        width: 850px;
        margin-top: 5px;
        /* margin-bottom: 10px; */
    }
    .msgCardHeader{
        font-size: 18px;
        font-weight: 800;
    }
    .clearfix:before,
    .clearfix:after {
        display: table;
        content: "";
    }
    .clearfix:after {
        clear: both
    }

    /* 滚动条位置 */
    /deep/.__bar-is-vertical {
        right: -1px !important;
    }
    /* 隐藏横向滚动条 */
    /deep/.__bar-is-horizontal {
        display: none !important;
    }

    .publishUser{
        margin-left: 10px;
        font-size: 10px;
    }
    .publishTime{
        margin-left: 10px;
        font-size: 10px;
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

    .publishUser{
        margin-left: 10px;
        font-size: 10px;
    }
    .publishTime{
        margin-left: 10px;
        font-size: 10px;
    }
    .postContainer>>>.el-scrollbar__wrap{
        overflow-x: hidden;
    }
    .pageBarCon{

    }
    .page-bar{
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .postDrawerMsg{
        width: 90%;  
        height: auto;  
        word-wrap:break-word;  
        word-break:break-all;  
        overflow: hidden;  
        font-size: 20px;
        color: #323232;
        margin-left: 5%;
        margin-top: 10px;
        /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); */
    }
    .postDrawerMsgP{
        /* margin: 23px; */
        margin-left: 40px;
    }
    .postDrawerTitleTip{
        margin-left: 35px;
        margin-bottom: 30px;
    }
    .postDrawer>>>.el-scrollbar__wrap{
        overflow-x: hidden;
    }
    .postDrawerComment>>>.el-divider{
        /* display:inline-block; */
        width:83.5%;
        /* height:100%;		 */
        /* margin:0 8px; */
        /* vertical-align:middle; */
        /* position:relative; */
        margin-left: 8.3%;
    }
    .postDrawerComment{
        margin-left: 7%;
        margin-top: 2%;
    }
    .PostCommenttUser{
        margin-left: 0px;
    }
    .PostCommentPublishTime{
        /* margin-bottom: 15px; */
        font-size: 12px;
        color:gray;
        margin-left: 0px;
    }
    .PostCommentUserID{
        font-size: 18px;
        /* color:gray; */
        margin-left: 0px;
        font-weight: 700;
    }

    .PostUser{
        margin-left: 20px;
    }
    .PostPublishTime{
        /* margin-bottom: 15px; */
        font-size: 12px;
        color:gray;
        margin-left: 15px;
    }
    .PostUserID{
        font-size: 18px;
        /* color:gray; */
        margin-left: 15px;
        font-weight: 700;
    }
    .postCommentMsg{
        width: 90%;  
        height: auto;  
        word-wrap:break-word;  
        word-break:break-all;  
        overflow: hidden;  
        font-size: 18px;
        color: #323232;
        margin-left: 2.1%;
        margin-top: 10px;
        /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); */
    }
    .postCommentMsgP{
        /* margin: 23px; */
        margin-left: 40px;
    }

    /* 更改element-UI按钮样式 */
    .thumbsUp.el-button--success {
        color: rgb(75, 181, 75);
        background-color: rgb(232, 247, 232);
        border-color: rgb(174, 231, 174);
    }
    .thumbsUp.el-button--success:hover{
        color: rgb(75, 181, 75);
        background-color: rgb(232, 247, 232);
        border-color: rgb(174, 231, 174);
    }
    .thumbsUp.el-button--success:focus{
        color: rgb(75, 181, 75);
        background-color: rgb(232, 247, 232);
        border-color: rgb(174, 231, 174);
    }
    .thumbsUpActive.el-button--success {
        color: white;
        background-color: rgb(98, 208, 98);
        border-color: rgb(98, 208, 98);
    }
    .thumbsUpActive.el-button--success:hover{
        color: white;
        background-color: rgb(98, 208, 98);
        border-color: rgb(98, 208, 98);
    }
    .thumbsUpActive.el-button--success:focus{
        color: white;
        background-color: rgb(98, 208, 98);
        border-color: rgb(98, 208, 98);
    }

    .releaseMsg>>>.el-textarea__inner {
        /* border: 0; */
        resize: none;/* 这个是去掉 textarea 下面拉伸的那个标志，如下图 */
        height: 300px;
        overflow-y: auto;
    }
</style>
