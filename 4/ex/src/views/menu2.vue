<template>
    <div class="menu">
        <el-row>
            <el-col :span="17">
                <div class="menuBtnList">
                    <div class="menuBtnListCon">
                        <ul>
                            <li v-for="(list,index) in cur_exLists">
                                <el-button type="primary" class="menuBtnListBtn" @click="goToEx(list.url, list.id)" plain>进入实验</el-button>
                                <el-button type="primary" class="menuBtnListBtn" @click="seeIntroduction(list.introduction, list.introductionUrl)" plain>查看简介</el-button>
                                <!-- <div class="menuBtnListTop"> -->
                                    <span class="menuBtnListP">{{ list.name }}</span>
                                <!-- </div> -->
                                
                                <div class="menuBtnListTop">
                                    <el-steps :active="list.active" finish-status="success">
                                        <el-step title="完成实验并提交实验报告"></el-step>
                                        <!-- <el-step title="提交实验报告"></el-step> -->
                                        <el-step title="教师评分"></el-step>
                                    </el-steps>
                                </div>
                                <!-- <el-divider v-if="index+1!=pageSize"></el-divider> -->
                            </li>
                        </ul>

                        <nav aria-label="page_navigation" class="page-bar">
                            <el-pagination background layout="prev, pager, next" :total="numTotal" :page-size="pageSize"
                            @prev-click="pre_page()"
                            @next-click="next_page()"
                            @current-change="curPage"
                            :hide-on-single-page="numTotal<=pageSize"></el-pagination>
                        </nav>
                        <!-- <el-row :gutter="0">
                            <el-col :span="6" :offset="0">
                                <button type="button" class="btn_ex1" @click="to_ex1"></button>
                                <p class="menuBtnListP">实验一</p>
                            </el-col>
                            <el-col :span="6">
                                <button type="button" class="btn_ex2" @click="to_ex2"></button>
                                <p class="menuBtnListP">实验二</p>
                            </el-col>
                            <el-col :span="6">
                                <button type="button" class="btn_ex3" @click="to_ex3"></button>
                                <p class="menuBtnListP">实验三</p>
                            </el-col>
                            <el-col :span="6" :offset="0">
                                <button type="button" class="btn_report" @click="to_report"></button>
                                <p class="menuBtnListP">实验报告</p>
                            </el-col>
                        </el-row>

                        <el-row :gutter="0">
                            <el-col :span="6">
                                <button type="button" class="btn_setting" @click="to_setting"></button>
                                <p class="menuBtnListP">设置</p>
                            </el-col>
                            <el-col :span="6">
                                <button type="button" class="btn_mail" @click="to_mail"></button>
                                <p class="menuBtnListP">信息</p>
                            </el-col>
                            <el-col :span="6">
                                <button type="button" class="btn_forum" @click="to_forum"></button>
                                <p class="menuBtnListP">讨论区</p>
                            </el-col>
                            <el-col :span="6">
                                <button type="button" class="btn_exit" @click="exit_to_login"></button>
                                <p class="menuBtnListP">退出登录</p>
                            </el-col>
                        </el-row> -->
                    </div>
                </div>
            </el-col>
            <el-col :span="7">
                <div class="menuBtnListRight">
                    <div class="menuBtnListRightLists">
                        <!-- <el-button type="primary" class="ex_name" @click="to_ex1" plain>实验报告</el-button>
                        <el-button type="primary" class="ex_name" @click="to_ex1" plain>设置</el-button>
                        <el-button type="primary" class="ex_name" @click="to_ex1" plain>信息</el-button>
                        <el-button type="primary" class="ex_name" @click="to_ex1" plain>讨论区</el-button>
                        <el-button type="primary" class="ex_name" @click="to_ex1" plain>退出登录</el-button> -->
                        <el-divider></el-divider>
                        <div @click="to_report">
                            <div class="ex_name"><i class="el-icon-document"></i>实验报告</div>
                        </div>
                        <div @click="to_setting">
                            <div class="ex_name"><i class="el-icon-setting"></i>设置</div>
                        </div>
                        <div @click="to_mail">
                            <div class="ex_name"><i class="el-icon-chat-dot-round"></i>信息中心</div>
                        </div>
                        <div @click="to_forum">
                            <div class="ex_name"><i class="el-icon-user"></i>讨论区</div>
                        </div>
                        <!-- <div @click="exit_to_login">
                            <div class="ex_name_exit">退出登录</div>
                        </div> -->
                        <el-button type="danger" class="ex_name_exit" @click="exit_to_login" plain>退出登录</el-button>
                    </div>
                </div>
            </el-col>
        </el-row>

        <el-dialog customClass="releaseDialog" title="实验简介" :visible.sync="exiVisible"  @closed="exihandleClose" :append-to-body="true">
            <p v-if="introduction!=null&&introduction!=''">{{ introduction }}</p>
            <!-- <a href=introductionUrl></a> -->
            <el-link v-if="introductionUrl!=null&&introductionUrl!=''" :href="introductionUrl" target="_blank" type="primary">实验简介链接</el-link>
            <p style="margin-left: 43%;" v-if="(introduction==null||introduction=='')&&(introductionUrl==null||introductionUrl=='')">无实验说明</p>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="exihandleSave">确定</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    import axios from 'axios'
    export function get_isStuHasGroup() {
        return axios({
            method: 'get',
            url: "/api/user/isStuHasGroup",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export function get_exLists() {
        return axios({
            method: 'get',
            url: "/api/experiment/exLists",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export function get_groupNameByStu_name(stu_num) {
        return axios({
            method: 'get',
            url: "/api/user/groupNameByStu_name",
            headers: {'Authorization': window.localStorage['Authorization']},
            params: {stu_num: stu_num}
        })
    }
    export default {
        data() {
            return {
                exLists:[
                    // {exName: "实验一", steps: "0"},
                    // {exName: "实验二", steps: "3"},
                    // {exName: "实验三", steps: "1"},
                ],
                cur_exLists:[],
                // pageTotal:3,
                // rows:1,
                numTotal:0,
                pageNo:1,
                pageSize:3,

                exiVisible: false,
                introduction: '',
                introductionUrl: '',

            }
        },
        created() {
            // 判断是否已登录
            get_isStuHasGroup().then(res => {
                if(res.data.status == 200){
                }
                else if(res.data.status == 403){
                    this.$router.replace('/stu_error')
                }
            }).catch( error =>{
                console.log(error);
            });
            // 获取实验列表
            get_exLists().then(res => {
                // console.log(res.data.data);
                if(res.data.status == 200){
                    this.exLists = res.data.data;
                    this.numTotal = this.exLists.length;
                    this.pageNo = 1;
                    this.getlist(this.pageNo);
                }
                else if(res.data.status == 403){
                    this.$router.replace('/stu_error')
                }
            }).catch( error =>{
                console.log(error);
            });
        },
        methods:{
            to_ex1(){
                this.noGroup(1);
            },
            to_ex2(){
                this.noGroup(2);
            },
            to_ex3(){
                this.noGroup(3);
            },
            to_setting(){
                this.$router.push('/setting');
            },
            to_report(){
                this.noGroup(4);
            },
            to_mail(){
                this.$router.push('/mail');
            },
            to_forum(){
                this.$router.push('/forum');
            },
            exit_to_login(){
                window.localStorage.removeItem('Authorization');
                window.localStorage.removeItem('userId');
                this.$router.push('/');
            },
            noGroup(num){
                get_isStuHasGroup().then(res => {
                    // console.log(res.data.status + " " + res.data.data.hasGroup);
                    if(res.data.status == 200){
                        if(res.data.data.hasGroup){
                            if(num == 1){
                                console.log("toex1");
                            }
                            else if(num == 2){
                                console.log("toex2");
                            }
                            else if(num == 3){
                                console.log("toex3");
                            }
                            else if(num == 4){
                                this.$router.push('/report');
                            }
                        }
                        else{
                            this.noGroupToSetting();
                        }
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            noGroupToSetting(){
                const h = this.$createElement;
                this.$notify.error({
                    title: '请先前往设置加入团队',
                    message: h('p', null, [
                        // h('span', null, '内容可以是 '),
                        h('el-button', {
                            on: {
                                click:this.to_setting
                            },
                            // type: 'primary'
                        }, "点击前往设置")
                    ]),
                    position: 'bottom-right'
                    // duration: 0
                });
            },
            getlist(index = -1){
                if(index != -1){
                    this.pageNo = index;
                }
                // console.log(index + "   " + this.pageNo);
                this.cur_exLists = [];
                for(var a in this.exLists){
                    if(a >= (this.pageNo - 1) * this.pageSize && a < this.pageNo * this.pageSize){
                        this.cur_exLists.push(this.exLists[a]);
                    }
                }
            },
            pre_page(){
                if(this.pageNo > 1){
                    this.pageNo--;
                    this.getlist(this.pageNo);
                }
            },
            next_page(){
                if(this.pageNo < this.pageTotal){
                    this.pageNo++;
                    this.getlist(this.pageNo);
                }
            },
            curPage(index){
                this.pageNo = index;
                this.getlist(index);
            },
            goToEx(url, id){
                get_groupNameByStu_name( window.localStorage['userId']).then(res => {
                    if(res.data.status == 200){
                        console.log(res.data.data);
                        window.open(url + "?group=" + res.data.data + "&ex=" + id);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            seeIntroduction(introduction, introductionUrl){
                this.introduction = introduction;
                this.introductionUrl = introductionUrl;
                this.exiVisible = true;
            },
            exihandleClose () {
                this.exiVisible = false;
            },
            exihandleSave () {
                this.exiVisible = false;
            },
        }
    }
</script>

<style scoped>
    .menu{
        margin:0 auto;
        position:fixed;
        top:0;
        left:0;
        width: 100%;
        height:100%;
        min-width: 1000px;
        zoom:1;
        background: url('../assets/tea/tea_info_bkg.jpg');
        background-repeat: no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
        background-position: center 0;
    }
    .menuBtnList{
        margin-left: 270px;
        margin-top: 5%;
        box-shadow: 0 2px 12px 0 rgba(43, 34, 34, 0.1);
        background-color: #fff;
        opacity: 0.91;
        height: 600px;
        width: 800px;
    }
    .btn_menu{
        margin-top: 30px;
        margin-left: 53px;
        width: 150px;
    }
    .btn_menu1{
        color:#000;
        width: 150px;
        height: 150px;
        font-size: 23px;
        outline: none;
        background-color: #f4f9fa;
        border:1px solid rgb(22, 51, 81);
        border-radius: 15px;

        /* margin-left: 100px; */
    }
    .btn_menu1:hover{
        color:#000;
        background-color: #d7eef3;
        border:1px solid rgb(22, 51, 81);
        font-weight: 900;
    }
    .btn_menu1:active{
        background-color: #cbe9f0;
    }
    .btn_ex1{
        background-image: url("../assets/menu/ex1.jpg");
        /* float:left; */
        /* margin-left: 155px; */
        width: 83px;
        height: 83px;
        border-radius:15px;
        background-color: transparent;
        /* background-color: blue; */
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
        border:2px solid rgb(22, 51, 81);
    }
    .btn_ex2{
        background-image: url("../assets/menu/ex2.jpg");
        /* float:left; */
        /* margin-left: 155px; */
        width: 83px;
        height: 83px;
        border-radius:15px;
        background-color: transparent;
        /* background-color: blue; */
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
        border:2px solid rgb(22, 51, 81);
    }
    .btn_ex3{
        background-image: url("../assets/menu/ex3.jpg");
        /* float:left; */
        /* margin-left: 155px; */
        width: 83px;
        height: 83px;
        border-radius:15px;
        background-color: transparent;
        /* background-color: blue; */
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
        border:2px solid rgb(22, 51, 81);
    }
    .btn_setting{
        background-image: url("../assets/menu/setting.jpg");
        /* float:left; */
        /* margin-left: 155px; */
        width: 83px;
        height: 83px;
        border-radius:15px;
        background-color: transparent;
        /* background-color: blue; */
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
        border:2px solid rgb(22, 51, 81);
    }
    .btn_report{
        background-image: url("../assets/menu/report.jpg");
        /* float:left; */
        /* margin-left: 155px; */
        width: 83px;
        height: 83px;
        border-radius:15px;
        background-color: transparent;
        /* background-color: blue; */
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
        border:2px solid rgb(22, 51, 81);
    }
    .btn_mail{
        background-image: url("../assets/menu/mail.jpg");
        /* float:left; */
        /* margin-left: 155px; */
        width: 83px;
        height: 83px;
        border-radius:15px;
        background-color: transparent;
        /* background-color: blue; */
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
        border:2px solid rgb(22, 51, 81);
    }
    .btn_forum{
        background-image: url("../assets/menu/forum.jpg");
        /* float:left; */
        /* margin-left: 155px; */
        width: 83px;
        height: 83px;
        border-radius:15px;
        background-color: transparent;
        /* background-color: blue; */
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
        border:2px solid rgb(22, 51, 81);
    }
    .btn_exit{
        background-image: url("../assets/menu/exit.jpg");
        /* float:left; */
        /* margin-left: 155px; */
        width: 83px;
        height: 83px;
        border-radius:15px;
        background-color: transparent;
        /* background-color: blue; */
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
        border:2px solid rgb(22, 51, 81);
    }
    .menuBtnListCon{
        /* margin-left: 23px; */
        margin-top: 50px;
        margin: 50px;
    }
    .menuBtnListTop{
        width: 700px;
        /* height: 110px; */
    }
    .menuBtnListP{
        /* font-size: 20px;
        font-weight: 600;
        text-align:center;
        margin-right: 20px;
        color: rgb(69, 74, 73); */
        font-size: 20px;
        font-weight: 600;
        /* margin-top: 50px; */
        /* margin-bottom: 20px; */
    }
    .menuBtnListBtn{
        /* float: right; */
        /* margin-right: 200px; */
        /* margin-left: 320px; */
        margin-top: 50px;
        margin-bottom: 20px;
    }
    .page-bar{
        margin-top: 43px;
    }

    .menuBtnListRight{
        margin-left: 100px;
        margin-top: 55px;
        box-shadow: 0 2px 12px 0 rgba(43, 34, 34, 0.1);
        background-color: #fff;
        opacity: 0.91;
        height: 600px;
        width: 200px;
    }
    .ex_name{
        font-size: 23px;
        font-weight: 600;
        /* text-align: center; */
        margin-top: 71px;
        color: #87D2FC;
        margin-left: 40px;
    }
    .ex_name_exit{
        font-size: 23px;
        font-weight: 600;
        /* text-align: center; */
        margin-top: 71px;
        /* color: rgb(255, 146, 146); */
        margin-left: 33px;
    }
    /* .menuBtnListRightLists{
        margin-top: 100px;
        height: 600px;
        width: 300px;
    } */
</style>
