<template>
    <div class="mailContainer">
        
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
</template>

<script>
    import tea_classMessageTab from "./MailTab/systemNotificationTab";
    import myMessageTab from "./MailTab/myMessageTab";
    import forumReply from "./MailTab/forumReply";
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
        },
    }
</script>

<style scoped>
    .mailContainer{
        margin-left: 140px;
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
</style>
