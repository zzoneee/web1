<template>
    <div class="reportContainer">
        <div>
            <el-row :gutter="0">
                <el-col :span="5" class="left_area">
                    <img src="../../../../static/deco1.png" style="padding-left: 12px;margin-bottom: 6px">
                    <div class="list_ex lst1">
                        <div @click="ex1_click">
                            <el-row :gutter="0">
                                <el-col :span="14">
                                    <div class="ex_name" :class="{'color_click':exNo==1}">按团队查看</div>
                                </el-col>
                            </el-row>
                        </div>
                        <div @click="ex2_click">
                            <el-row :gutter="0">
                                <el-col :span="14">
                                    <div class="ex_name" :class="{'color_click':exNo==2}">按班级查看</div>
                                </el-col>
                            </el-row>
                        </div>
                    </div>
                    <div style="margin-top: 100px">
                        <el-row :gutter="0">
                            <el-col :span="11" :offset="1">
                                <img src="../../../../static/line1.png">
                            </el-col>
                            <el-col :span="11">
                                <img src="../../../../static/line2.png">
                            </el-col>
                        </el-row>
                    </div>
                    <div class="deco_line"></div>
                </el-col>
                <el-col :span="19" class="right_area">
                    <step1 v-if="exNo==1"></step1>
                    <step2 v-if="exNo==2"></step2>
                </el-col>
            </el-row>
        </div>

    </div>
</template>

<script>
    const report_group = () => import('./tea_report_group');
    const report_class = () => import('./tea_report_class');
    // import report_group from "./tea_report_group";
    // import report_class from "./tea_report_class";
    export default {
        components:{
            "step1":report_group,
            "step2":report_class,
        },
        data(){
            return{
                exNo:1
            };
        },
        created() {
        },
        methods:{
            ex1_click(){
                this.exNo=1;
            },
            ex2_click(){
                this.exNo=2;
            },
        }
    }
</script>

<style scoped>
    /* 左侧导航栏 */
    .left_area{
        height:730px;
        margin-top: 20px;
    }
    .ex_name{
        font-size: 23px;
        font-family: Microsoft YaHei;
        font-weight: 400;
        line-height: 24px;
        color: #000;
        opacity: 1;
        margin-left: 55px;
        margin-top: 45px;
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
    .deco1{
        position: relative;
        float: left;
        margin-left: 13px;
        width: 307px;
        height: 0px;
        border: 1px solid #87D2FC;
        opacity: 1;
    }
    
    /* 右侧信息 */
    .right_area{
        padding-left: 20px;
        width:60%;
        margin-left: 100px;
    }
</style>
