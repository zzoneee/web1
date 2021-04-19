<template>
    <div class="systemNotificationContainer">
        <div class="systemNotificationTop">
            <el-tag effect="plain" type="success" class="systemNotificationTag">公告</el-tag>
            <!-- <el-button type="primary" size="small" round class="releaseNotification" @click="releaseNotification">发布公告</el-button> -->
        </div>
        <el-divider></el-divider>
        <el-scrollbar style="width:866px;height:100%;margin-left:20px;">
            <!-- <ul> -->
                <li v-for="item in noticeLists">
                    <!-- <el-badge value="置顶"> -->
                        <el-card class="msgCard" shadow="hover">
                            <div slot="header" class="clearfix">
                                <el-tag type="success" v-if="item.new==1">new</el-tag>
                                <el-tag type="danger" v-if="item.top==1">置顶</el-tag>
                                <span class="msgCardHeader">{{ item.title }}</span>
                                <span class="publishUser">发布人：{{item.user_id}}</span>
                                <span class="publishTime">发布时间：{{item.time}}</span>

                                <!-- <el-popconfirm title="是否删除？" @confirm="deleteNotice(item.id)">
                                    <el-button slot="reference" style="float: right" type="danger" icon="el-icon-delete" circle size="mini"></el-button>
                                </el-popconfirm>
                                
                                <el-popconfirm title="是否置顶？" @confirm="topNotice(item.id)" v-if="item.top==0">
                                    <el-button slot="reference" style="float: right; margin-right: 10px" icon="el-icon-top" type="primary" circle size="mini"></el-button>
                                </el-popconfirm>

                                <el-popconfirm title="是否取消置顶？" @confirm="noTopNotice(item.id)" v-if="item.top==1">
                                    <el-button slot="reference" style="float: right; margin-right: 10px" icon="el-icon-bottom" type="warning" circle size="mini"></el-button>
                                </el-popconfirm>

                                <el-popconfirm title="是否编辑？" @confirm="editNotice(item.id, item.title, item.message)">
                                    <el-button slot="reference" style="float: right; margin-right: 10px" icon="el-icon-edit" type="success" circle size="mini"></el-button>
                                </el-popconfirm> -->
                            </div>
                            <div class="msgText">
                                <p>{{ item.message }}</p>
                            </div>
                        </el-card>
                    <!-- </el-badge> -->
                </li>
            <!-- </ul> -->
        </el-scrollbar>

        <!-- <el-dialog customClass="releaseDialog" title="发布公告" :visible.sync="dialogFormVisible"  @closed="handleClose" :append-to-body="true">
            <el-form :model="form" :rules="rules" ref="ruleForm">

                <el-form-item label="标题" :label-width="formLabelWidth" prop="title">
                    <el-input v-model="form.title" autocomplete="off" class="releaseInput"></el-input>
                </el-form-item>
                <el-form-item label="公告内容" :label-width="formLabelWidth" prop="message" class="releaseMsg">
                    <el-input type="textarea" :rows="2" maxlength="500" show-word-limit v-model="form.message" autocomplete="off" class="releaseTextArea"></el-input>
                </el-form-item>
                <el-form-item label="置顶" :label-width="formLabelWidth" prop="top">
                    <el-switch v-model="form.top"></el-switch>
                </el-form-item>
                
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleSave">确定</el-button>
            </div>
        </el-dialog>

        <el-dialog customClass="editDialog" title="编辑公告" :visible.sync="editVisible"  @closed="editClose" :append-to-body="true">
            <el-form :model="editForm" :rules="editRules" ref="editRuleForm">

                <el-form-item label="标题" :label-width="formLabelWidth" prop="title">
                    <el-input v-model="editForm.title" autocomplete="off" class="releaseInput"></el-input>
                </el-form-item>
                <el-form-item label="公告内容" :label-width="formLabelWidth" prop="message" class="releaseMsg">
                    <el-input type="textarea" :rows="2" maxlength="500" show-word-limit v-model="editForm.message" autocomplete="off" class="releaseTextArea"></el-input>
                </el-form-item>
                
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取消</el-button>
                <el-button type="primary" @click="editSave">确定</el-button>
            </div>
        </el-dialog> -->

    </div>
</template>

<script>
    import axios from 'axios'
    export function get_stuNoticeLists() {
        return axios({
            method: 'get',
            url: "/api/notice/stuNoticeLists",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export default {
        data() {
            return {
                noticeLists: [],
            }
        },
        created() {
            this.getNoticeLists();
        },
        methods:{
            getNoticeLists(){
                get_stuNoticeLists().then(res => {
                    // console.log(res.data.data);
                    if(res.data.status == 200){
                        // console.log(res.data.data);
                        this.noticeLists = res.data.data;
                        console.log(this.noticeLists);
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
    .releaseNotification{
        float: right;
        margin-right: 15px;
        margin-top: 5px;
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
    .msgText{
        width: 100%;  
        height: auto;  
        word-wrap:break-word;  
        word-break:break-all;  
        overflow: hidden;  
        font-size: 14px;
        color: #323232;
        /* font-family: "微软雅黑"; */
    }
    /* 滚动条位置 */
    /deep/.__bar-is-vertical {
        right: -1px !important;
    }
    /* 隐藏横向滚动条 */
    /deep/.__bar-is-horizontal {
        display: none !important;
    }

    .releaseMsg>>>.el-textarea__inner {
        /* border: 0; */
        resize: none;/* 这个是去掉 textarea 下面拉伸的那个标志，如下图 */
        height: 300px;
        overflow-y: auto;
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
</style>
