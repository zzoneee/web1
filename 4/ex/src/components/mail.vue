<template>
    <div class="mailContainer">
        <div class="header">
            <el-row :gutter="0">
                <el-col>
                    <button type="button" class="btn_setting"></button>
                    <button type="button" class="btn_backManu" @click="toMenu"></button>
                </el-col>
            </el-row>
        </div>

        <div class="mailCon2">
            <el-row :gutter="0">
                <el-col :span="3" :offset="2">
                    <div class="mailLeft">
                        <button class="mailbtn" :class="{'active_mailbtn':mailNum=='1'}" type="input" @click="clickMailbtn1()">公告</button>
                        <button class="mailbtn" :class="{'active_mailbtn':mailNum=='2'}" type="input" @click="clickMailbtn2()">我的消息</button>
                        <button class="mailbtn" :class="{'active_mailbtn':mailNum=='3'}" type="input" @click="clickMailbtn3()">讨论区评论</button>
                    </div>
                </el-col>

                <el-col :span="3">
                    <div class="mailRight">
                        <step1 v-if="mailNum==1"></step1>
                        <step2 v-if="mailNum==2"></step2>
                        <step3 v-if="mailNum==3"></step3>
                    </div>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
    import tea_classMessageTab from "./TabComponents/MailTab/StuSystemNotificationTab";
    import myMessageTab from "./TabComponents/MailTab/StuMyMessageTab";
    import forumReply from "./TabComponents/MailTab/StuForumReply";
    export default {
        components:{
            "step1": tea_classMessageTab,
            "step2": myMessageTab,
            "step3": forumReply,
        },
        data() {
            return {
                mailNum: 1
            }
        },
        created() {
        },
        methods:{
            clickMailbtn1(){
                this.mailNum = 1;
            },
            clickMailbtn2(){
                this.mailNum = 2;
            },
            clickMailbtn3(){
                this.mailNum = 3;
            },
            toMenu(){
                this.$router.push('/menu');
            },
        },
    }
</script>

<style scoped>
    .mailContainer{
        margin:0 auto;
        position:fixed;
        top:0;
        left:0;
        width: 100%;
        height:100%;
        min-width: 1000px;
        zoom:1;

        background: url('../assets/bg.png');
        background-repeat: no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
        background-position: center 0;
    }
    .mailCon2{
        margin-left: 130px;
        margin-top: 27px;
    }
    .mailLeft{
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        height: 600px;
        width: 150px;
        /* margin-left: 100px; */
    }
    .mailRight{
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        height: 600px;
        width: 890px;
        /* margin-left: 100px; */
    }
    .mailbtn{
        color:#6b757b;
        width: 150px;
        height:40px;
        font-size: 15px;
        font-weight: 700;
        outline: none;
        /* background-color: #b0cad9; */
        background-color:transparent;
        border-style:none;
        /* border:1px solid rgb(22, 51, 81); */
        /* border-radius: 20px; */
        margin-top: 30px;
    }
    .mailbtn:hover{
        color: #2faee3;
    }
    .active_mailbtn{
        color: #2faee3;
    }

    .header{
        /* background: url('../assets/header.jpg'); */
        height:80px;
        /* width:1508px; */
    }
    .btn_setting{
        background-image: url("../assets/btn_mail.jpg");
        float:left;
        margin-left: 155px;
        width: 145px;
        height: 38px;
        background-color: transparent;
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
    }
    .btn_backManu{
        background-image: url("../assets/btn_backManu2.jpg");
        float:right;
        margin-right: 30px;
        /* margin-left: 1055px; */
        width: 145px;
        height: 38px;
        background-color: transparent;
        border-style: none;
        outline:none;
        margin-top: 22px;
        margin-left: 20px;
    }
</style>
