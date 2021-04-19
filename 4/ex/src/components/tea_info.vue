<template>
    <div class="container">

        <el-menu
            :default-active="activeIndex"
            class="el-menu"
            mode="horizontal"
            @select="handleSelect"
            text-color="#000"
            active-text-color="#4099b4">
            <el-menu-item index="6" class="stuMsg" :class="{'active_index':activeIndex=='6'}">实验</el-menu-item>
            <el-menu-item index="1" :class="{'active_index':activeIndex=='1'}">学生信息</el-menu-item>
            <el-menu-item index="2" :class="{'active_index':activeIndex=='2'}">实验报告</el-menu-item>
            <!-- <el-menu-item index="3" :class="{'active_index':activeIndex=='3'}">添加新教师</el-menu-item> -->
            <el-menu-item index="5" :class="{'active_index':activeIndex=='4'}">讨论区</el-menu-item>
            
            <el-submenu index="4" class="userInfo">
                <template slot="title"><el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar> {{ userID }}</template>
                <el-menu-item index="4-1" :class="{'active_index':activeIndex=='4-1'}">信息修改</el-menu-item>
                <el-menu-item index="4-2" :class="{'active_index':activeIndex=='4-2'}">密码修改</el-menu-item>
                <el-menu-item index="3" :class="{'active_index':activeIndex=='3'}">添加新教师</el-menu-item>
                <el-menu-item index="4-3" :class="{'active_index':activeIndex=='4-3'}">退出登录</el-menu-item>
            </el-submenu>
            
            <!-- <el-badge :value="7" class="e-mail"> -->
                <!-- <el-button type="primary" icon="el-icon-message" class="e-mailBtn"></el-button> -->
                <el-button class="e-mail" type="info" icon="el-icon-message" circle @click="toE_mail"></el-button>
            <!-- </el-badge> -->
        </el-menu>

        <div class="info">

            <!-- <div class="header">
                <el-row :gutter="0">
                    <el-col :span="3" :offset="2">
                        <button class="tea_info_btn" :class="{'color_click':exNo==1}" type="input" @click="ex1_click">学生信息</button>
                    </el-col>
                    <el-col :span="3">
                        <button class="tea_info_btn" :class="{'color_click':exNo==2}" type="input" @click="ex2_click">实验报告</button>
                    </el-col>
                    <el-col :span="3">
                        <button class="tea_info_btn" :class="{'color_click':exNo==3}" type="input" @click="ex3_click">设置</button>
                    </el-col>
                </el-row>
            </div> -->

            <div class="message">
                <step1 v-if="exNo==1"></step1>
                <step2 v-if="exNo==2"></step2>
                <step3 v-if="exNo==3"></step3>
                <step4 v-if="exNo==4"></step4>
                <step5 v-if="exNo==5"></step5>
                <step6 v-if="exNo==6"></step6>
                <step7 v-if="exNo==7"></step7>
                <step8 v-if="exNo==8"></step8>
            </div>
        </div>

    </div>
</template>

<script>
    const tea_classInfo = () => import('./TabComponents/tea_classInfo');
    const tea_experiment = () => import('./TabComponents/tea_experiment');

    // import tea_classMessageTab from "./TabComponents/tea_classMessageTab";
    import tea_report from "./TabComponents/teaReport/tea_report";
    import tea_addTeacherTab from "./TabComponents/tea_addTeacherTab";
    import tea_teacherMessageModificationTab from "./TabComponents/tea_teacherMessageModificationTab";
    import tea_passwordModificationTab from "./TabComponents/tea_passwordModificationTab";
    import tea_mail from "./TabComponents/tea_mail";
    import forum from "./TabComponents/forum/forum";
    export default {
        components:{
            "step1":tea_classInfo,
            "step2":tea_report,
            "step3":tea_addTeacherTab,
            "step4":tea_teacherMessageModificationTab,
            "step5":tea_passwordModificationTab,
            "step6":tea_mail,
            "step7":forum,
            "step8":tea_experiment,
        },
        data() {
            return {
                exNo:8,
                activeIndex: '6',
                userID: window.localStorage['tea_userId']
            }
        },
        methods:{
            handleSelect(key, keyPath) {
                this.activeIndex = key;
                // console.log(key, keyPath, this.activeIndex[0]);
                if(this.activeIndex == "1"){
                    this.exNo = 1;
                }
                else if(this.activeIndex == "2"){
                    this.exNo = 2;
                }
                else if(this.activeIndex == "3"){
                    this.exNo = 3;
                }
                else if(this.activeIndex == "4-1"){
                    this.exNo = 4;
                }
                else if(this.activeIndex == "4-2"){
                    this.exNo = 5;
                }
                else if(this.activeIndex == "5"){
                    this.exNo = 7;
                }
                else if(this.activeIndex == "4-3"){
                    window.localStorage.removeItem('tea_Authorization');
                    window.localStorage.removeItem('tea_userId');
                    this.$router.push('/tea_login');
                }
                else if(this.activeIndex == "6"){
                    this.exNo = 8;
                }
            },
            toE_mail(){
                this.exNo = 6;
                this.activeIndex = 999;
            },
        }
    }

</script>

<style scoped>
    .container{
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
    .info{
        margin-top: 3%;
    }
    .message{
        margin-top: 2%;
    }
    .tea_info_btn{
        color:#000;
        width: 140px;
        height:50px;
        font-size: 18px;
        outline: none;
        background-color: #c2e6f1;
        border:1px solid rgb(22, 51, 81);
        border-radius: 25px;
    }
    .color_click{
        color: #c2e6f1;
        background-color: #61b3cc;
    }
    .stuMsg{
        margin-left: 100px;
    }
    .userInfo{
        float:right;
    }
    .el-menu-item{
        font-size: 16px;
    }
    .active_index{
        font-weight: 600;
    }
    .e-mail{
        float:right;
        margin-top: 15px;
        margin-right: 50px;
    }
    @keyframes myMove {
        0% {
            top: 0;
        }
        50% {
            top: 4vh;
        }
        100% {
            top: 0;
        }
    } 
</style>
