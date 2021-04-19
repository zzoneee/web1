<template>
    <div class="setting_container">

        <div class="setting_info">

            <el-row :gutter="0">
            
                <el-col :span="5" class="setting_left">
                    <!-- <el-row :gutter="0"> -->
                        <!-- <el-col :span="3" :offset="2"> -->
                            <!-- <button class="tea_info_btn" :class="{'color_click':exNo==1}" type="input" @click="ex1_click">班级信息</button> -->
                            <div @click="setting_ex1_click" class="setting_left_btn">
                                <div class="ex_name" :class="{'color_click':setting_exNo==1}">信息修改</div>
                            </div>
                        <!-- </el-col> -->
                        <!-- <el-col :span="3"> -->
                            <!-- <button class="tea_info_btn" :class="{'color_click':exNo==2}" type="input" @click="ex2_click">实验报告</button> -->
                            <div @click="setting_ex2_click" class="setting_left_btn">
                                <div class="ex_name" :class="{'color_click':setting_exNo==2}">密码修改</div>
                            </div>
                        <!-- </el-col> -->
                        <!-- <el-col :span="3"> -->
                            <!-- <button class="tea_info_btn" :class="{'color_click':exNo==3}" type="input" @click="ex3_click">设置</button> -->
                            <div @click="setting_ex3_click" class="setting_left_btn">
                                <div class="ex_name" :class="{'color_click':setting_exNo==3}">添加新教师</div>
                            </div>
                        <!-- </el-col> -->
                    <!-- </el-row> -->
                </el-col>

                <el-col :span="19" class="setting_right">
                    <step1 v-if="setting_exNo==1"></step1>
                    <step2 v-if="setting_exNo==2"></step2>
                    <step3 v-if="setting_exNo==3"></step3>
                </el-col>
            
            </el-row>
        </div>

    </div>
</template>

<script>
    import tea_teacherMessageModificationTab from "./tea_teacherMessageModificationTab";
    import tea_passwordModificationTab from "./tea_passwordModificationTab";
    import tea_addTeacherTab from "./tea_addTeacherTab";
    export default {
        // name: "tea_setting",
        components:{
            "step1":tea_teacherMessageModificationTab,
            "step2":tea_passwordModificationTab,
            "step3":tea_addTeacherTab
        },
        data() {
            return {
                setting_exNo:1
            }
        },
        methods:{
            setting_ex1_click(){
                this.setting_exNo=1;
                // console.log(this.setting_exNo);
            },
            setting_ex2_click(){
                this.setting_exNo=2;
                // console.log(this.setting_exNo);
            },
            setting_ex3_click(){
                this.setting_exNo=3;
                // console.log(this.setting_exNo);
            }
        }
    }

</script>

<style scoped>

    .setting_container{
        margin-left: 5%;
    }
    .setting_left_btn{
        color:#428599;
        width: 140px;
        height:50px;
        font-size: 18px;
        outline: none;
        /* background-color: #c2e6f1; */
        /* border:1px solid rgb(22, 51, 81); */
        
        /* border-radius: 25px; */
        font-size: 25px;
        margin-top: 10%;
    }
    .color_click{
        color: #296b80;
        font-weight:bold;
        /* background-color: #61b3cc; */
        /* border-left: 1px solid rgb(22, 51, 81); */
        /* background-color: #c2e6f1; */
    }
    /* .setting_right{
        margin-left: ;
    } */

</style>
