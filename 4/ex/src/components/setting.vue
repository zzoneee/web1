<template>
    <div class="container">

        <div class="header">
            <el-row :gutter="0">
                <el-col>
                    <button type="button" class="btn_setting"></button>
                    <button type="button" class="btn_backManu" @click="toMenu"></button>
                </el-col>
            </el-row>
        </div>

        <div>
            <el-row :gutter="0">
                <el-col :span="5" class="left_area">
                    <img src="static/deco1.png" style="padding-left: 12px;margin-bottom: 6px">
                    <div class="list_ex lst1">
                        <div @click="ex1_click">
                            <el-row :gutter="0">
                                <el-col :span="14">
                                    <div class="ex_name" :class="{'color_click':exNo==1 || exNo==3}">团队信息</div>
                                </el-col>
                            </el-row>
                        </div>
                        <div @click="ex4_click">
                            <el-row :gutter="0">
                                <el-col :span="14">
                                    <div class="ex_name" :class="{'color_click':exNo==4}">个人信息</div>
                                </el-col>
                            </el-row>
                        </div>
                        <div @click="ex2_click">
                            <el-row :gutter="0">
                                <el-col :span="14">
                                    <div class="ex_name" :class="{'color_click':exNo==2}">密码修改</div>
                                </el-col>
                            </el-row>
                        </div>
                    </div>
                    <div style="margin-top: 100px">
                        <el-row :gutter="0">
                            <el-col :span="11" :offset="1">
                                <img src="static/line1.png">
                            </el-col>
                            <el-col :span="11">
                                <img src="static/line2.png">
                            </el-col>
                        </el-row>
                    </div>
                    <div class="deco_line"></div>
                </el-col>
                <el-col :span="19" class="right_area">
                    <step1 v-if="exNo==1"></step1>
                    <step2 v-if="exNo==2"></step2>
                    <step3 v-if="exNo==3"></step3>
                    <step4 v-if="exNo==4"></step4>
                </el-col>
            </el-row>
        </div>

    </div>
</template>

<script>
    import groupInfoTab from "./TabComponents/groupInfoTab";
    import passwordModificationTab from "./TabComponents/passwordModificationTab";
    import noGroupInfoTab from "./TabComponents/noGroupInfoTab";
    import stuMsgModificationTab from "./TabComponents/stuMsgModificationTab";
    import axios from 'axios'
    export function get_isStuHasGroup() {
        return axios({
            method: 'get',
            url: "/api/user/isStuHasGroup",
            headers: {'Authorization': window.localStorage['Authorization']}
        })
    }
    export default {
        components:{
            "step1":groupInfoTab,
            "step2":passwordModificationTab,
            "step3":noGroupInfoTab,
            "step4":stuMsgModificationTab,
        },
        data(){
            return{
                exNo: 0
            };
        },
        created() {
            this.isStuHasGroup();
        },
        methods:{
            ex1_click(){
                this.isStuHasGroup();
            },
            ex2_click(){
                this.exNo = 2;
            },
            ex4_click(){
                this.exNo = 4;
            },
            toMenu(){
                this.$router.push('/menu');
            },
            isStuHasGroup(){
                get_isStuHasGroup().then(res => {
                    if(res.data.status == 200){
                        if(res.data.data.hasGroup){
                            this.exNo = 1;
                        }
                        else{
                            this.exNo = 3;
                        }
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/stu_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
        }
    }
</script>

<style scoped>
    /* 导航栏 */
    .container{
        /* width: 1515px; */
        /* height: 100vh;
        min-height: 700px; */
        /* background: #060E21; */
        /* margin:0 auto;
        opacity: 1; */
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
    .header{
        /* background: url('../assets/header.jpg'); */
        height:80px;
        /* width:1508px; */
    }
    .btn_setting{
        background-image: url("../assets/btn_setting2.jpg");
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

    /* 左侧导航栏（团队信息、密码修改） */
    .left_area{
        /* width:880px; */
        height:730px;
        margin-top: 20px;
    }
    .lst_img_click{
        background:url("../assets/ex_img.png");
        background-repeat: no-repeat
    }
    .lst_img_noclick{
        background:url("../assets/lst_ex1.png");
        background-repeat: no-repeat
    }
    .lst_img_normal{
        width: 126px;
        height: 70px;
        font-size: 20px;
        font-family: Arial Rounded MT;
        font-weight: bold;
        line-height: 23px;
        color: #87D2FC;
        opacity: 1;
        margin-top: 20px;
        padding-top: 27px;
        text-align: center;
    }
    .ex_name{
        font-size: 23px;
        font-family: Microsoft YaHei;
        font-weight: 400px;
        line-height: 24px;
        color: #000;
        opacity: 1;
        margin-left: 55px;
        margin-top: 45px;
    }
    .dif{
        margin-top: 12px;
        width: 7px;
        height: 17px;
        background: #87D2FC;
        opacity: 0.8;
        border-radius: 3px;
        transform:rotate(10deg);
        -ms-transform:rotate(10deg); 	/* IE 9 */
        -moz-transform:rotate(10deg); 	/* Firefox */
        -webkit-transform:rotate(10deg); /* Safari 和 Chrome */
        -o-transform:rotate(10deg); 	/* Opera */
    }
    .dif_click{
        background-color: #6CFCE8;
    }
    .diff_font{
        margin-left: 15px;
        margin-top: 9px;
        font-size: 16px;
        font-family: Microsoft YaHei;
        font-weight: 400;
        line-height: 21px;
        opacity: 0.8;
        color: #87D2FC;
    }
    .color_normal{
        color: #87D2FC;
    }
    .color_click{
        color: #87D2FC;
        font-weight: bolder;
    }
    .deco_line{
        width: 0px;
        height: 240px;
        border: 1px solid #2C4C79;
        opacity: 1;
        position: absolute;
        left: 400px;
        top:70px;
    }
    .bigBtn{
        margin-top: 10px;
        width: 168px;
        height: 59px;
        background-color: transparent;
        border-style: none;
        outline:none;
    }
    /* .btn_restart{
        margin-left: 30px;
        background-image: url("../assets/restart.png");
    }
    .btn_close{
        margin-left: 20px;
        background-image: url("../assets/close.png");
    } */
    .system_settings{
        width: 388px;
        height: 230px;
        background: #1A2B47;
        opacity: 1;
        margin-left: 13px;
        margin-top: 20px;
    }
    .deco1{
        position: relative;
        float: left;
        margin-left: 13px;
        width: 307px;
        height: 0px;
        border: 1px solid #87D2FC;
        opacity: 1;
    }
    .deco2{
        position: relative;
        float: right;
        width: 38px;
        height: 0px;
        border-bottom: #87D2FC 2px dashed;
        opacity: 1;
        margin-right: 20px;
    }
    .setting_font{
        font-size: 16px;
        font-family: Microsoft YaHei;
        font-weight: 400;
        line-height: 19px;
        color: #87D2FC;
        opacity: 1;
    }
    .para{
        width: 43px;
        height: 28px;
        background: #2C4C79;
        opacity: 1;
        padding-bottom: 10px;
    }
    .para p{
        color: #87D2FC;
        text-align: center;
    }

    /* 右侧信息 */
    .right_area{
        padding-left: 20px;
        width:60%;
        margin-left: 100px;
    }

</style>