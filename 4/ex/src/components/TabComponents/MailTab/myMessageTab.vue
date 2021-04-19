<template>
    <div class="myMessageContainer">
        <div class="myMessageTop">
            <el-tag effect="plain" type="success" class="myMessageTag">我的消息</el-tag>
            <el-button type="primary" size="small" class="recentContacts" @click="openDrawer">最近联系人</el-button>
            <el-button type="success" size="small" class="findContact" @click="searchContacts">查找联系人</el-button>
        </div>
        <el-divider></el-divider>
        <el-tabs v-model="editableTabsValue" type="card" closable @tab-remove="removeTab" @tab-click="clickTab">
            <el-tab-pane
                v-for="(item, index) in editableTabs"
                :key="item.name"
                :label="item.receiver"
                :name="item.name">
                <!-- {{item.content}} -->
                <!-- <vue-scroll :ops="ops" style="width:866px;height:360px;margin-left:20px;" class="chatBox-content-demo"> -->
                <el-scrollbar :ops="ops" style="width:866px;height:360px;margin-left:20px;" class="myScrollbar" ref="myScrollbar">
                    <li v-for="(item2, index2) in item.msgList">
                        <div class="liMsg">
                            <div v-if="item2.Ienter==2" class="msgall">
                                <el-row :gutter="0">
                                    <el-col :span="2" :offset="0">
                                        <el-avatar> {{item.receiver}} </el-avatar>
                                    </el-col>
                                    <el-col :span="17">
                                        <div class="msgContainer">
                                            <p class="myMessageMsg">{{item2.message}}</p>
                                        </div>
                                    </el-col>
                                </el-row>
                            </div>

                            <div v-if="item2.Ienter==1" class="msgall2">
                                <el-row :gutter="0">
                                    <el-col :span="2" :offset="0" push="22">
                                        <el-avatar> {{userID}} </el-avatar>
                                    </el-col>
                                    <el-col :span="17" push="2">
                                        <div class="msgContainer2">
                                            <p class="myMessageMsg">{{item2.message}}</p>
                                        </div>
                                    </el-col>
                                </el-row>
                            </div>
                        </div>
                        
                        <!-- <div v-if="item2.Ienter==1" class="msgall2">
                            <el-row :gutter="0">
                                <el-col :span="10" :offset="3">
                                    <div class="msgContainer2">
                                        <p class="myMessageMsg2">{{item2.message}}</p>
                                    </div>
                                </el-col>
                                <el-col :span="2">
                                    <el-avatar class="myMessageavatar2"> {{userID}} </el-avatar>
                                </el-col>
                            </el-row>
                        </div> -->
                        <!-- </div> -->
                    </li>
                </el-scrollbar>
                <div class="enterMsg">
                    <el-input type="textarea" :rows="2" maxlength="500" show-word-limit placeholder="请输入内容" v-model="enterMsgs" class="textareaMsg"></el-input>
                    <el-button type="primary" class="enterMsgBtn" size="small" @click="enterMsgClick(item.identity)">发送</el-button>
                </div>
            </el-tab-pane>
        </el-tabs>

        <el-drawer
        title="最近联系人"
        :visible.sync="drawer"
        :direction="direction" :append-to-body="true">
            <!-- <span>最多显示最近十位联系人</span> -->
            <div class="recentContactsList">
                <el-scrollbar style="width:100%;height:600px">
                    <!-- <li v-for="item in recentContactsLists">
                        {{item.receiver}}
                    </li> -->
                    <li v-for="item in recentContactsLists">
                        <div class="recentContactLi">
                            <el-tag type="success" v-if="item.identity==0" style="margin-top: 9px; margin-left:11px;">教师</el-tag>
                            <el-tag type="primary" v-if="item.identity==1" style="margin-top: 9px; margin-left:11px;">学生</el-tag>
                            {{item.receiver}}
                            <el-popconfirm title="是否发送消息？" @confirm="sendMsg(item.receiver, item.identity)">
                                <el-button slot="reference" style="float: right; margin-right: 10px; margin-top: 11px;" icon="el-icon-chat-dot-square" type="primary" circle size="mini"></el-button>
                            </el-popconfirm>
                        </div>
                    </li>
                </el-scrollbar>
            </div>
        </el-drawer>

        <el-dialog customClass="searchContactDiag" title="查找联系人" :visible.sync="dialogFormVisible"  @closed="handleClose" :append-to-body="true">
            <el-form :model="form" :rules="rules" ref="ruleForm">

                <!-- <el-form-item label="标题" :label-width="formLabelWidth" prop="title">
                    <el-input v-model="form.title" autocomplete="off" class="releaseInput"></el-input>
                </el-form-item>
                <el-form-item label="公告内容" :label-width="formLabelWidth" prop="message" class="releaseMsg">
                    <el-input type="textarea" :rows="2" maxlength="500" show-word-limit v-model="form.message" autocomplete="off" class="releaseTextArea"></el-input>
                </el-form-item>
                <el-form-item label="置顶" :label-width="formLabelWidth" prop="top">
                    <el-switch v-model="form.top"></el-switch>
                </el-form-item> -->

                <el-form-item label="" :label-width="formLabelWidth" prop="receiver">
                    <el-input v-model="form.receiver" autocomplete="off" class="searchContactInput" placeholder="请输入账号"></el-input>
                    <el-button type="primary" icon="el-icon-search" @click="searchContact(form.receiver, form.identity)">搜索</el-button>
                </el-form-item>

                <el-form-item label="" :label-width="formLabelWidth" prop="identity">
                    <el-radio-group v-model="form.identity">
                        <el-radio :label=0>教师</el-radio>
                        <el-radio :label=1>学生</el-radio>
                    </el-radio-group>
                </el-form-item>
                
            </el-form>

            <div class="recentContactSearch" v-if="searchContactForm.identity!=2&&searchContactForm.identity!=4">
                <el-tag type="success" v-if="searchContactForm.identity==0||searchContactForm.identity==3" style="margin-top: 9px; margin-left:11px;">教师</el-tag>
                <el-tag type="primary" v-if="searchContactForm.identity==1" style="margin-top: 9px; margin-left:11px;">学生</el-tag>
                {{searchContactForm.receiver}}
                <el-popconfirm title="是否发送消息？" @confirm="sendMsg(searchContactForm.receiver, searchContactForm.identity)">
                    <el-button v-if="searchContactForm.identity!=3" slot="reference" style="float: right; margin-right: 10px; margin-top: 11px;" icon="el-icon-chat-dot-square" type="primary" circle size="mini"></el-button>
                </el-popconfirm>
                <!-- <el-tooltip content="Bottom center" placement="bottom" effect="light"> -->
                    <el-button disabled v-if="searchContactForm.identity==3" style="float: right; margin-right: 10px; margin-top: 11px;" icon="el-icon-chat-dot-square" type="primary" circle size="mini"></el-button>
                <!-- </el-tooltip> -->
            </div>

            <div class="noRecentContactSearch" v-if="searchContactForm.identity==4">
                没有这个用户
            </div>

            <!-- <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleSave">确定</el-button>
            </div> -->
        </el-dialog>

    </div>
</template>

<script>
    import axios from 'axios'
    export function get_privateLetter() {
        return axios({
            method: 'get',
            url: "/api/privateLetter/getPrivateLetterLists",
            headers: {'Authorization': window.localStorage['tea_Authorization']}
        })
    }
    export function post_enterPrivateLetter(receiver, message, identity) {
        return axios({
            method: 'post',
            url: "/api/privateLetter/enterPrivateLetter",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data:{receiver: receiver, message: message, identity: identity}
        })
    }
    export function get_recentContacts() {
        return axios({
            method: 'get',
            url: "/api/privateLetter/getRecentContacts",
            headers: {'Authorization': window.localStorage['tea_Authorization']}
        })
    }
    export function post_closeChatBox(receiver, iden) {
        return axios({
            method: 'post',
            url: "/api/privateLetter/closeChatBox",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data:{receiver: receiver, iden: iden}
        })
    }
    export function post_openChatBox(receiver, identity) {
        return axios({
            method: 'post',
            url: "/api/privateLetter/openChatBox",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data:{receiver: receiver, identity: identity}
        })
    }
    export function get_searchContact(receiver, identity) {
        return axios({
            method: 'get',
            url: "/api/privateLetter/searchContact",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            params:{receiver: receiver, identity: identity}
        })
    }
    export default {
        data() {
            return {
                userID: window.localStorage['tea_userId'],
                editableTabsValue: '',
                editableTabs: [],
                tabIndex: 0,

                drawer: false,
                direction: 'ltr',

                ops: {
                    vuescroll: {},
                    scrollPanel: {},
                    rail: {
                        keepShow: true
                    },
                    bar: {
                        hoverStyle: true,
                        onlyShowBarOnScroll: false, //是否只有滚动的时候才显示滚动条
                        background: "#000",//滚动条颜色
                        opacity: 0.2,//滚动条透明度
                        "overflow-x": "hidden"
                    }
                },
                enterMsgs: '',
                firstEnter: true,
                recentContactsLists: [],
                dialogFormVisible: false,
                form: {
                    receiver: '',
                    identity: 0
                },
                rules: {
                    // title: [
                    //     { required: true, message: '请输入标题', trigger: 'blur' },
                    //     { min: 1, max: 30, message: '长度应小于 30 个字符', trigger: 'blur' }
                    // ],
                    // message: [
                    //     { required: true,  message: '请输入公告内容', trigger: 'blur' },
                    //     { min: 1, max: 500, message: '长度应小于 500 个字符', trigger: 'blur' }
                    // ],
                },
                formLabelWidth: '120px',
                searchContactForm: {
                    identity: 2, //0：教师，1：学生，2：还未搜索，3：自己，4：用户不存在
                    receiver: ''
                },
            }
        },
        created() {
            this.initGetMsg();
        },
        updated: function() {
            this.scrollDown();
        },
        methods:{
            scrollDown() {
                // console.log(this.$refs['myScrollbar'][0].wrap.scrollHeight);
                // console.log(this.tabIndex);
                for(let i = 0;i < this.tabIndex;i++){
                    this.$refs['myScrollbar'][i].wrap.scrollTop = this.$refs['myScrollbar'][i].wrap.scrollHeight;
                }
            },
            initGetMsg(){
                get_privateLetter().then(res => {
                    // console.log(res.data.status);
                    if(res.data.status == 200){
                        // console.log(res.data.data[0]['receiver']);
                        // this.noticeLists = res.data.data
                        if(this.firstEnter){
                            this.editableTabsValue = res.data.data[0]['name'];
                            this.firstEnter = false;
                        }
                        this.tabIndex = res.data.data.length
                        this.editableTabs = res.data.data;
                        // console.log(this.editableTabs[1].msgList);
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
            // addTab(targetName) {
            //     let newTabName = ++this.tabIndex + '';
            //     this.editableTabs.push({
            //         receiver: 'New Tab',
            //         name: newTabName,
            //         msgList: []
            //     });
            //     this.editableTabsValue = newTabName;
            // },
            removeTab(targetName) {
                let tabs = this.editableTabs;
                let activeName = this.editableTabsValue;
                if (activeName === targetName) {
                    tabs.forEach((tab, index) => {
                        if (tab.name === targetName) {
                        let nextTab = tabs[index + 1] || tabs[index - 1];
                        if (nextTab) {
                            activeName = nextTab.name;
                        }
                        }
                    });
                }
                this.editableTabsValue = activeName;
                this.editableTabs = tabs.filter(tab => tab.name !== targetName);

                // this.enterMsgs = '';
                this.tabIndex--;

                let lenTargetName = targetName.length;
                let iden = 0;
                let receiver = "";
                for(let i = 0;i < lenTargetName - 1;i++){
                    receiver += targetName[i];
                }
                if(targetName[lenTargetName - 1] == '0'){
                    iden = 0;
                }
                else{
                    iden = 1;
                }
                // console.log(receiver + " " + iden);
                post_closeChatBox(receiver, iden).then(res => {
                    console.log(res.data.status);
                    if(res.data.status == 200){
                        // console.log(res.data.data);
                        // this.noticeLists = res.data.data
                        // this.initGetMsg();// 刷新信息
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
            clickTab(targetName){
                // this.enterMsgs = '';
            },
            enterMsgClick(identity){
                if(this.enterMsgs != ''){
                    // console.log(this.enterMsgs,this.editableTabsValue,identity);
                    let lenTargetName = this.editableTabsValue.length;
                    let receiver = "";
                    for(let i = 0;i < lenTargetName - 1;i++){
                        receiver += this.editableTabsValue[i];
                    }
                    post_enterPrivateLetter(receiver, this.enterMsgs, identity).then(res => {
                        // console.log(res.data.status);
                        if(res.data.status == 200){
                            // console.log(res.data.data);
                            // this.noticeLists = res.data.data
                            this.initGetMsg();// 刷新信息
                            this.enterMsgs = '';
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
                }
            },
            openDrawer(){
                this.drawer = true;
                get_recentContacts().then(res => {
                    // console.log(res.data.status);
                    if(res.data.status == 200){
                        // console.log(res.data.data);
                        this.recentContactsLists = res.data.data;
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
            // 选择用户打开聊天框
            sendMsg(receiver, identity){
                // console.log(receiver + " " + identity);
                post_openChatBox(receiver, identity).then(res => {
                    // console.log(res.data.status);
                    if(res.data.status == 200){
                        // console.log(res.data.data);
                        this.initGetMsg();// 刷新信息
                        // console.length(receiver + String(identity));
                        if(identity == 0){
                            this.editableTabsValue = receiver + '0';
                        }
                        else{
                            this.editableTabsValue = receiver + '1';
                        }

                        // this.editableTabsValue = receiver + String(identity);
                        this.drawer = false; // 用于最近联系人
                        this.dialogFormVisible = false; // 用于查找联系人
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
            // 点击“查找联系人”按钮
            searchContacts(){
                // console.log(589);
                this.dialogFormVisible = true;
            },
            handleClose () {
                this.searchContactForm.identity=2;
                this.$refs.ruleForm.resetFields();
                // this.form.title = '';
                // this.form.message = '';
                // this.editRoleForm.role = '';
            },
            searchContact(receiver, identity){
                if(receiver != '' && receiver != null){
                    // console.log(receiver + " " + identity);
                    get_searchContact(receiver, identity).then(res => {
                        // console.log(res.data.status);
                        if(res.data.status == 200){
                            // console.log(res.data.data);
                            this.searchContactForm = res.data.data;
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
                }
            },
        },
    }
</script>

<style scoped>
    
    .myMessageContainer{
        height: 520px;
        /* margin-left: 20px; */
    }
    .myMessageTop{
        height: 18px;
    }
    .myMessageTag{
        margin-top: 5px;
        margin-left: 20px;
    }
    .recentContacts{
        float: right;
        margin-right: 15px;
        margin-top: 5px;
    }
    .findContact{
        float: right;
        margin-right: 15px;
        margin-top: 5px;
    }
    .msgall{
        margin-top: 20px;
    }
    .msgContainer{
        width: auto;  
        display:inline-block !important; display:inline; 
        height: auto;  
        word-wrap:break-word;  
        word-break:break-all;  
        overflow: hidden;  
        font-size: 18px;
        font-weight: 500;
        color: #323232;
        background: rgb(223, 233, 241);
        /* border-top-left-radius:2em; */
        border-top-right-radius:1em;
        border-bottom-right-radius:1em;
        border-bottom-left-radius:1em;
    }
    .myMessageMsg{
        margin: 15px;
    }
    .msgall2{
        margin-top: 20px;
        /* float: right; */
        /* margin-left: 235px; */
        /* width: 450px; */
    }
    .liMsg{
        width: 100%;
    }
    .msgContainer2{
        width: auto;  
        display:inline-block !important; display:inline; 
        height: auto;  
        word-wrap:break-word;  
        word-break:break-all;  
        overflow: hidden;  
        font-size: 18px;
        font-weight: 500;
        color: #323232;
        background: rgb(214, 248, 221);
        border-top-left-radius:1em;
        /* border-top-right-radius:1em; */
        border-bottom-right-radius:1em;
        border-bottom-left-radius:1em;
        /* margin-right: 30px; */
        float: right;
    }
    .myMessageavatar2{
        /* display:inline-block !important; display:inline;  */
        /* float: right; */
    }
    .myMessageMsg2{
        margin: 15px;
    }
    .textareaMsg{
        
    }
    .enterMsg{
        height: 118px;
        background: #fff;
        border-top: 0.5px solid rgb(231, 229, 229);
    }
    .enterMsg>>>.el-textarea__inner {
        border: 0;
        resize: none;/* 这个是去掉 textarea 下面拉伸的那个标志，如下图 */
        height: 80px;
        overflow-y: auto;
    }
    .enterMsgBtn{
        float: right;
        margin-right: 20px;
    }

    .myMessageContainer>>>.el-scrollbar__wrap{
        overflow-x: hidden;
    }

    .recentContactsList{
        width: 400px;
        height: 600px;
        margin-left: 30px;
        margin-top: 20px;
    }

    .recentContactsList>>>.el-scrollbar__wrap{
        overflow-x: hidden;
    }
    .recentContactLi{
        width: 320px;
        height: 50px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
        margin-top: 30px;
        margin-left: 40px;
        margin-bottom: 5px;
        /* background-color: rgb(182, 129, 129); */
    }
    .recentContactLi2{
        margin-top: 10px;
    }
    .searchContactInput{
        width: 200px;
    }
    .recentContactSearch{
        width: 320px;
        height: 50px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
        margin-top: 30px;
        margin-left: 115px;
        margin-bottom: 5px;
        /* background-color: rgb(182, 129, 129); */
    }
    .noRecentContactSearch{
        margin-left: 230px;
    }

</style>

<style>
    .searchContactDiag{
        width:600px;
    }
</style>
