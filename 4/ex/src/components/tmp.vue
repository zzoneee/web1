<template>
    <div>
        <!-- <div>
            <span>实验</span>
            <el-input type="textarea" v-model="z1" class="zz"></el-input>
            <span>团队</span>
            <el-input type="textarea" v-model="z2" class="zz"></el-input>
            <span>实验目的</span>
            <el-input type="textarea" v-model="z3" class="zz"></el-input>
            <span>系统得分</span>
            <el-input type="textarea" v-model="z4" class="zz"></el-input>
            <el-button type="primary" @click="submitForm()">提交</el-button>
        </div> -->
        <div id="myChart" :style="{width: '300px', height: '200px'}"></div>
        <el-button type="primary" @click="submitForm()">提交</el-button>
    </div>
</template>

<script>
    export default {
        
        data() {
            return {
                z1: '',
                z2: '',
                z3: '',
                z4: '',
                zzz: 1,
            }
        },
        mounted () {
            this.drawLine();
        },
        created() {
            
        },
        methods:{
            submitForm(){
                // console.log(this.codeList);
                this.zzz++;
                this.drawLine();
            },
            // 绘制柱状图
            drawLine(){
                // 基于准备好的dom，初始化echarts实例
                let myChart = this.$echarts.init(document.getElementById('myChart'))
                // 绘制图表
                myChart.setOption({
                    title: {
                        text: '投票结果',
                        // subtext: '纯属虚构',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                    },
                    series: [
                        {
                            name: '投票人数',
                            type: 'pie',
                            radius: '50%',
                            data: [
                                {value: this.zzz, name: '人'},
                                {value: 5, name: 'AI'},
                            ],
                            emphasis: {
                                itemStyle: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }
                    ]
                });
            },
        },
    }
</script>

<style scoped>

</style>
