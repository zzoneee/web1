<template>
    <div id="classInfoRc">
        <div class="classInfo_table" v-if="curPosition==0">
            <el-table
                    :data="classInfoTableData"
                    height="550"
                    border
                    id="tb"
                    ref="multipleTable"
                    @selection-change="handleSelectionChange"
                    style="width: 100%">
                <el-table-column
                                type="selection"
                                width="39">
                </el-table-column>
                <el-table-column align='center'
                                 prop="class_name"
                                 label="班级"
                                 width="300">
                </el-table-column>
                <el-table-column align='center'
                                 prop="college"
                                 label="学院"
                                 width="400">
                </el-table-column>
                <el-table-column align='center'
                                 prop="class_amount"
                                 label="人数"
                                 width="200">
                </el-table-column>
                <el-table-column align='center'
                                 prop="details"
                                 label="详情">
                    <template slot-scope="scope">
                        <el-button size="mini" class="classDetail" @click="toSeeDetialClassMsg(scope.$index, classInfoTableData)" type="primary">查看详情</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <el-button type="danger" style="margin-top: 31px;" @click="deleteClassBtn()">删除班级</el-button>
            <el-button type="primary" style="margin-top: 31px;" @click="addClassBtn()">添加班级</el-button>
        </div>

        <div class="classInfo_table" v-show="curPosition==1">
            <!-- <el-page-header @back="goBack" :content=curClass_name class="position2PageHeader"></el-page-header> -->
            <div class="goBackTop">
                <div class="goBackTop2">
                    <span @click="goBack()" class="goBack"><i class="el-icon-back"></i>返回</span>
                    <el-divider direction="vertical"></el-divider>
                    <span>{{ curClass_name }}</span>
                </div>
            </div>

            <div class="plane_table">
                <el-input class="search_stu_msg" placeholder="请输入要查找的内容" v-model="search_stu_msg"></el-input>
                <el-button class="search_stu_btn" icon="el-icon-search" @click="searchStu">搜索</el-button>
                <!-- 导入导出 -->
                <!-- 操作按钮 -->
                <input type="file" @change="importExcel(this)" id="importExcel" style="display: none" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel" />
                <a id="exportExcel"></a>
                <el-button class="btnExport" type="success" @click="btnExportClick(tableData)">导出Excel</el-button>
                <el-button class="btnImport" type="primary" @click="btnImportClick">导入Excel</el-button>
                <!-- 错误提示 -->
                <el-dialog title="提示" v-model="errorDialog">
                    <span>{{errorMsg}}</span>
                    <span slot="footer" class="dialog-footer">
                        <el-button type="primary" @click="errorDialog=false">确认</el-button>
                    </span>
                </el-dialog>

                <el-table
                        v-loading="loading"
                        :data="tableData"
                        height="490"
                        border
                        id="tb"
                        style="width: 100%">
                    <el-table-column align='center'
                                    prop="college"
                                    label="学院"
                                    width="150">
                    </el-table-column>
                    <el-table-column align='center'
                                    prop="class_name"
                                    label="班级"
                                    width="120">
                    </el-table-column>
                    <el-table-column align='center'
                                    prop="stu_num"
                                    label="学号"
                                    width="150">
                    </el-table-column>
                    <el-table-column align='center'
                                    prop="name"
                                    label="姓名"
                                    width="120">
                    </el-table-column>
                    <el-table-column align='center'
                                    prop="phone"
                                    label="电话号码"
                                    width="150">
                    </el-table-column>
                    <el-table-column align='center'
                                    prop="group"
                                    label="团队"
                                    width="140">
                    </el-table-column>
                    <el-table-column align='center'
                                    prop="role"
                                    label="承担角色"
                                    width="100">
                    </el-table-column>
                    <el-table-column align='center'
                                    prop="details"
                                    label="操作">
                        <template slot-scope="scope">
                            <el-button size="mini" class="download" @click="updateStuMsg(scope.$index, tableData);updateStuMsgVisible = true">修改信息</el-button>
                            <el-button size="mini" type="warning" @click="resetPassword(scope.$index, tableData)">重置密码</el-button>
                            <el-button size="mini" type="danger" @click="deleteStu(scope.$index, tableData)">删除</el-button>
                        </template>
                    </el-table-column>

                </el-table>
                <el-button class="addStuBtn" type="input" @click="dialogFormVisible = true">添加学生</el-button>
            </div>
        </div>

        <!-- page1 -->
        <el-dialog customClass="addClassDialog" title="添加班级" :visible.sync="addClassDialogFormVisible"  @closed="addClassHandleClose" :append-to-body="true">
            <el-form :model="addClassForm" :rules="addClassRules" ref="addClassRuleForm">
                <el-form-item label="班级名称" :label-width="formLabelWidth" prop="class_name">
                    <el-input v-model="addClassForm.class_name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="所属学院" :label-width="formLabelWidth" prop="college">
                    <el-input v-model="addClassForm.college" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="addClassDialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="addClassHandleSave">确定</el-button>
            </div>
        </el-dialog>

        <!-- page2 -->
        <el-dialog customClass="stuMsgDialog" title="修改学生信息" :visible.sync="updateStuMsgVisible"  @closed="handleClose" :append-to-body="true">
            <el-form :model="form" :rules="rules" ref="ruleForm">
                <el-form-item label="学号" :label-width="formLabelWidth" prop="stu_num">
                    <el-input :disabled="true" v-model="form.stu_num" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="姓名" :label-width="formLabelWidth" prop="name">
                    <el-input v-model="form.name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="学院" :label-width="formLabelWidth" prop="college">
                    <!-- <el-input v-model="form.college" autocomplete="off"></el-input> -->
                    <el-input :disabled="true" v-model="curCollege" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="班级" :label-width="formLabelWidth" prop="class_name">
                    <!-- <el-input v-model="form.class_name" autocomplete="off"></el-input> -->
                    <el-input :disabled="true" v-model="curClass_name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="电话号码" :label-width="formLabelWidth" prop="phone">
                    <el-input v-model="form.phone" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="团队" :label-width="formLabelWidth" prop="groupName">
                    <el-select v-model="form.groupName" placeholder="请选择要加入的团队" @change="current">
                        <el-option label="" value=""></el-option>
                        <el-option v-for="(item,index) in form.groups" :label="item.name" :key="index" :value="item.name"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item v-if="ifChooseGroup==1" label="承担角色" :label-width="formLabelWidth" prop="role">
                    <el-input v-model="form.role" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="updateStuMsgVisible = false">取消</el-button>
                <el-button type="primary" @click="updateStuMsgSave">保存</el-button>
            </div>
        </el-dialog>

        <!-- <el-button class="addStuBtn" type="input" @click="dialogFormVisible = true">添加学生</el-button> -->
        <el-dialog customClass="stuMsgDialog2" title="添加学生" :visible.sync="dialogFormVisible"  @closed="handleClose" :append-to-body="true">
            <el-form :model="form" :rules="rules" ref="ruleForm">

                <el-form-item label="学号" :label-width="formLabelWidth" prop="stu_num">
                    <el-input v-model="form.stu_num" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="姓名" :label-width="formLabelWidth" prop="name">
                    <el-input v-model="form.name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" :label-width="formLabelWidth" prop="password">
                    <el-input v-model="form.password" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="学院" :label-width="formLabelWidth" prop="college">
                    <!-- <el-input :disabled="true" v-model="form.college" autocomplete="off"></el-input> -->
                    <el-input :disabled="true" v-model="curCollege" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="班级" :label-width="formLabelWidth" prop="class_name">
                    <!-- <el-input :disabled="true" v-model="form.class_name" autocomplete="off"></el-input> -->
                    <el-input :disabled="true" v-model="curClass_name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="电话号码" :label-width="formLabelWidth" prop="phone">
                    <el-input v-model="form.phone" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="团队" :label-width="formLabelWidth" prop="groupName">
                    <el-select v-model="form.groupName" placeholder="请选择要加入的团队" @change="current">
                        <el-option label="" value=""></el-option>
                        <el-option v-for="(item,index) in form.groups" :label="item.name" :key="index" :value="item.name"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item v-if="ifChooseGroup==1" label="承担角色" :label-width="formLabelWidth" prop="role">
                    <el-input v-model="form.role" autocomplete="off"></el-input>
                </el-form-item>
                
            </el-form>

            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取消</el-button>
                <el-button type="primary" @click="handleSave">确定</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
    import axios from 'axios'
    import XLSX from 'xlsx'
    export function get_classesInfo() {
        return axios({
            method: 'get',
            url: "/api/classes/classesInfo",
            headers: {'Authorization': window.localStorage['tea_Authorization']}
        })
    }
    export function get_classesExist(class_name) {
        return axios({
            method: 'get',
            url: "/api/classes/classesExist",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            params: {'class_name': class_name}
        })
    }
    export function post_addClass(class_name, college) {
        return axios({
            method: 'post',
            url: "/api/classes/addClass",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {'class_name': class_name, 'college': college}
        })
    }
    export function post_deleteClass(classMsg) {
        return axios({
            method: 'post',
            url: "/api/classes/deleteClass",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data: {'classMsg': classMsg}
        })
    }

    // page2
    export function get_classMessage() {
        return axios({
            method: 'get',
            url: "/api/teacher/classMessage",
            headers: {'Authorization': window.localStorage['tea_Authorization']}
        })
    }
    export function post_importExcel(insertData) {
        return axios({
            method: 'post',
            url: "/api/teacher/importExcel",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            data:{'insertData': insertData}
        })
    }
    export function get_stuNumExist(stuNum) {
        return axios({
            method: 'get',
            url: "/api/teacher/stuNumExist",
            headers: {'Authorization': window.localStorage['tea_Authorization']},
            params:{stuNum: stuNum}
        })
    }
    export default {
        data() {
            let validateClass_name = (rule, value, callback) => {
                if(value == ""){
                    callback(new Error('请输入班级名称'));
                }
                get_classesExist(value).then(res => {
                    // console.log(res.data.data);
                    if(res.data.status == 200){
                        if(res.data.data == '0'){
                            callback();
                        }
                        else{
                            callback(new Error('该班级已存在'));
                        }
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error')
                    }
                }).catch( error =>{
                    console.log(error);
                    callback(new Error(error));
                });
            };

            //page2
            let validateGroup = (rule, value, callback) => {
                if (value == '') {
                    this.ifChooseGroup = 0;
                    // callback(new Error('请输入学院'));
                } else {
                    this.ifChooseGroup = 1;
                }
                callback();
            };
            let validateStu_num = (rule, value, callback) => {
                if(value == ""){
                    callback(new Error('请输入学号'));
                }
                else if(this.updateStuMsgVisible == false){
                    // this.$axios({
                    //     method: 'get',
                    //     url: "/api/teacher/stuNumExist",
                    //     params:{stuNum: value}
                    // }).then((res) => {
                    //     if(res.data.status == 200){
                    //         callback();
                    //     }
                    //     else{
                    //         callback(new Error('该学号已存在'));
                    //     }
                    // }).catch( error =>{
                    //     console.log(error);
                    //     callback(new Error(error));
                    // });
                    get_stuNumExist(value).then(res => {
                        if(res.data.status == 200){
                            callback();
                        }
                        else if(res.data.status == 403){
                            this.$router.replace('/tea_error')
                        }
                        else{
                            callback(new Error('该学号已存在'));
                        }
                    }).catch( error =>{
                        console.log(error);
                        callback(new Error(error));
                    });
                }
                else{
                    callback();
                }
            };
            return {
                curPosition: 0, // 0: 班级列表；1：班级详细信息
                curClassID: '', // 当前班级
                curClass_name: '', // 当前班级
                curCollege: '', // 当前学院

                classInfoTableData: [],
                multipleSelection: [],

                addClassDialogFormVisible: false,
                addClassForm: {
                    class_name: '',
                    college: '',
                },
                formLabelWidth: '120px',
                addClassRules: {
                    class_name: [
                        { validator: validateClass_name, required: true, trigger: 'blur' },
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                    college: [
                        { message: '请输入所属学院', required: true, trigger: 'blur' },
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                },

                // page2
                editMsg:{},
                allTableData: [],
                tableData: [],
                dialogFormVisible: false,
                form: {
                    stu_num: '',
                    name: '',
                    college: '',
                    class_name: '',
                    phone: '',
                    role: '',
                    password: '',
                    groups: [],
                    groupName: ''
                },
                rules: {
                    groupName: [
                        { validator: validateGroup, trigger: ["blur",'change'] }
                    ],
                    stu_num: [
                        { validator: validateStu_num, required: true, trigger: 'blur' },
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                    name: [
                        { required: true, message: '请输入姓名', trigger: 'blur' },
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: '请输入密码', trigger: 'blur' },
                        { min: 6, max: 16, message: '长度在 6 到 16 个字符', trigger: 'blur' }
                    ],
                    // college: [
                    //     { required: true, message: '请输入学院', trigger: 'blur' },
                    //     { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    // ],
                    // class_name: [
                    //     { required: true, message: '请输入班级', trigger: 'blur' },
                    //     { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    // ],
                    phone: [
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                    role: [
                        { min: 0, max: 20, message: '长度应小于 20 个字符', trigger: 'blur' }
                    ],
                },
                ifChooseGroup: 0,
                updateStuMsgVisible: false,
                update_StuMsg:{},
                search_stu_msg: '',

                elImport: '', // 导入el
                elExport: '', // 导出el
                errorDialog: false, // 错误信息弹窗
                errorMsg: '', // 错误信息内容

                loading: false,
            }
        },
        created() {
            this.getClassesInfo();

            // 获取团队信息（列表）
            this.$axios({
                method: 'get',
                url: "/api/teacher/getGroupList"
            }).then(res=> {
                if(res.status == 200){
                    this.form.groups=res.data.data;
                }
                else{
                    console.log(res.data.msg);
                }
            }).catch( error =>{
                console.log(error);
            });
        },
        mounted () {
            this.elImport = document.getElementById('importExcel')
            this.elExport = document.getElementById('exportExcel')
        },
        methods:{
            // 复选框选项变动
            handleSelectionChange(val) {
                this.multipleSelection = val;
                // console.log(this.multipleSelection, val);
            },
            getClassesInfo(){
                get_classesInfo().then(res => {
                    // console.log(res.data.err);
                    if(res.data.status == 200){
                        this.classInfoTableData=res.data.data;
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            addClassBtn(){
                this.addClassDialogFormVisible = true;
            },
            addClassHandleClose () {
                this.$refs.addClassRuleForm.resetFields();
                this.addClassForm.class_name = '';
                this.addClassForm.college = '';
            },
            addClassHandleSave () {
                this.$refs.addClassRuleForm.validate((valid) => {
                    if (valid) {
                        post_addClass(this.addClassForm.class_name, this.addClassForm.college).then(res => {
                            // console.log(res.data.err);
                            if(res.data.status == 200){
                                this.$message.success("添加成功");
                                this.addClassDialogFormVisible = false;
                                this.getClassesInfo();
                                this.addClassHandleClose();
                            }
                            else if(res.data.status == 403){
                                this.$router.replace('/tea_error')
                            }
                            else{
                                this.$message.error("添加失败, "+res.data.msg);
                                return false;
                            }
                        }).catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("添加失败");
                    }
                })
            },
            // 删除班级
            deleteClassBtn(){
                // console.log(this.multipleSelection);
                if(this.multipleSelection.length == 0){
                    this.$message.error("请选择要删除的班级");
                }
                else{
                    post_deleteClass(this.multipleSelection).then(res => {
                        // console.log(res.data.err);
                        if(res.data.status == 200){
                            this.$message.success("删除成功");
                            this.getClassesInfo();
                        }
                        else if(res.data.status == 403){
                            this.$router.replace('/tea_error')
                        }
                        else{
                            this.$message.error("删除失败, "+res.data.msg);
                        }
                    }).catch( error =>{
                        console.log(error);
                    });
                }
            },
            // 查看班级详细信息
            toSeeDetialClassMsg(index, tableData){
                // console.log(tableData[index].id);
                this.curClassID = tableData[index].id;
                this.curClass_name = tableData[index].class_name;
                this.curPosition = 1;
                this.curCollege = tableData[index].college;
                // console.log(this.curCollege);

                // page2
                // 获取班级信息（表格）
                this.getClassMsg();
            },
            goBack(){
                // console.log(154);
                this.curPosition = 0;
                this.curClassID = '';
                this.curClass_name = '';

                // 更新班级列表
                this.getClassesInfo();
            },

            // page2
            // 获取班级信息（表格）
            getClassMsg(){
                get_classMessage().then(res => {
                    // console.log(res.data.err);
                    if(res.data.status == 200){
                        // this.tableData=res.data.data;
                        this.tableData = [];

                        // console.log("*******");
                        // console.log(res.data.data);

                        res.data.data.forEach(item=>{
                            if(item.class_name == this.curClass_name){
                                this.tableData.push(item);
                            }
                        })

                        this.allTableData=this.tableData;
                        this.password = res.data.password;
                        // console.log(this.tableData);
                    }
                    else if(res.data.status == 403){
                        this.$router.replace('/tea_error')
                    }
                }).catch( error =>{
                    console.log(error);
                });
            },
            updateStuMsg(index, row){
                // 显示对话框内的学生信息
                this.form.stu_num = row[index].stu_num;
                this.form.password = '******';
                this.form.name = row[index].name;
                this.form.college = row[index].college;
                this.form.phone = row[index].phone;
                this.form.class_name = row[index].class_name;
                this.form.groupName = row[index].group;
                if(this.form.groupName != ''){
                    this.ifChooseGroup = 1;
                }
                else{
                    this.ifChooseGroup = 0;
                }
                this.form.role = row[index].role;
            },
            updateStuMsgSave(){
                //更新学生信息
                this.$refs.ruleForm.validate((valid) => {
                    if (valid) {
                        this.update_StuMsg.stu_num = this.form.stu_num;
                        this.update_StuMsg.name = this.form.name;
                        this.update_StuMsg.college = this.form.college;
                        this.update_StuMsg.phone = this.form.phone;
                        this.update_StuMsg.role = this.form.role;
                        this.update_StuMsg.groupName = this.form.groupName;
                        // console.log("*** " + this.update_StuMsg.groupName);
                        this.update_StuMsg.class_name = this.form.class_name;
                        if(this.update_StuMsg.groupName == ''){
                            this.update_StuMsg.role = '';
                        }
                        // console.log(this.update_StuMsg);
                        this.$axios({
                            method: 'post',
                            url: "/api/teacher/updateStuMsg",
                            data: this.update_StuMsg
                        }).then(res=> {
                            if(res.data.status == 200){
                                this.$message.success("修改成功");
                                this.updateStuMsgVisible = false;
                                this.getClassMsg();
                                this.handleClose();
                            }else{
                                this.$message.error("修改失败, "+res.data.msg);
                                return false;
                            }
                        }) .catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("修改失败");
                    }
                })
            },
            resetPassword(index, row){
                // 重置密码
                this.$axios({
                    method: 'post',
                    url: "/api/teacher/resetPassword",
                    data: {stu_num: row[index].stu_num}
                }).then(res=> {
                    if(res.data.status == 200){
                        this.$message.success("重置密码成功，新密码为123456");
                        // this.getClassMsg();
                    }else{
                        this.$message.error("重置密码失败, "+res.data.msg);
                        return false;
                    }
                }) .catch( error =>{
                    console.log(error);
                });
            },
            deleteStu(index, row){
                this.$axios({
                    method: 'post',
                    url: "/api/teacher/deleteStu",
                    data: {stu_num: row[index].stu_num}
                }).then(res=> {
                    if(res.data.status == 200){
                        this.$message.success("删除成功");
                        this.getClassMsg();
                    }else{
                        this.$message.error("删除失败, "+res.data.msg);
                        return false;
                    }
                }) .catch( error =>{
                    console.log(error);
                });
            },
            handleClose () {
                this.$refs.ruleForm.resetFields();
                this.form.stu_num = '';
                this.form.name = '';
                this.form.college = '';
                this.form.phone = '';
                this.form.role = '';
                this.form.password = '';
                this.form.groupName = '';
                this.form.class_name = '';
            },
            handleSave () {
                this.$refs.ruleForm.validate((valid) => {
                    if (valid) {
                        this.editMsg.stu_num = this.form.stu_num;
                        this.editMsg.name = this.form.name;
                        // this.editMsg.college = this.form.college;
                        this.editMsg.college = this.curCollege;
                        this.editMsg.phone = this.form.phone;
                        this.editMsg.role = this.form.role;
                        this.editMsg.password = this.form.password;
                        this.editMsg.groupName = this.form.groupName;
                        // this.editMsg.class_name = this.form.class_name;
                        this.editMsg.class_name = this.curClass_name;

                        if(this.editMsg.groupName == ''){
                            this.editMsg.role = '';
                        }
                        this.$axios({
                            method: 'post',
                            url: "/api/teacher/addStudent",
                            data: this.editMsg
                        }).then(res=> {
                            if(res.data.status == 200){
                                this.$message.success("添加成功");
                                this.dialogFormVisible = false;
                                this.getClassMsg();
                                this.handleClose();
                            }else{
                                this.$message.error("添加失败, "+res.data.msg);
                                return false;
                            }
                        }) .catch( error =>{
                            console.log(error);
                        });
                    } else {
                        this.$message.error("添加失败");
                    }
                })
            },
            match_msg(str1, str2){
                if(str1 == '' || str1 == null || str2 == '' || str2 == null){
                    return false;
                }
                var str1len = str1.length;
                var str2len = str2.length;
                for(var i = 0;i < str1len;i++){
                    var flag = 1;
                    for(var j = 0;j < str2len;j++){
                        if(i + j >= str1len || str1[i + j] != str2[j]){
                            flag = 0;
                            break;
                        }
                    }
                    if(flag == 1){
                        return true;
                    }
                }
                return false;
            },
            searchStu(){
                // console.log(this.match_msg('杭州国际服务工程学院',this.search_stu_msg));
                if(this.search_stu_msg != ''){
                    this.tableData = [];
                    // console.log(this.allTableData);
                    this.allTableData.forEach(item=>{
                        // console.log(item);
                        if(this.match_msg(item.stu_num,this.search_stu_msg) || 
                        this.match_msg(item.name,this.search_stu_msg) || 
                        this.match_msg(item.college,this.search_stu_msg) || 
                        this.match_msg(item.class_name,this.search_stu_msg) || 
                        this.match_msg(item.phone,this.search_stu_msg) || 
                        this.match_msg(item.role,this.search_stu_msg) || 
                        this.match_msg(item.group,this.search_stu_msg)){
                            // console.log(item.stu_num);
                            this.tableData.push(item);
                        }
                        // console.log(item.stu_num);
                        
                    })
                    // console.log(this.search_stu_msg);
                }
            },
            // 点击导入按钮
            btnImportClick () {
                // console.log(54654);
                this.elImport.click();
            },
            // 点击导出按钮
            btnExportClick (rs) {
                if(rs.length == 0){
                    this.$message.error("无学生数据，导出失败");
                }
                else{
                    // 生成列名
                    // let tableHeader = ['学院', '班级', '学号', '姓名', '电话号码', '团队', '承担角色'];
                    let data = [{}]
                    for (let k in rs[0]) {
                        data[0][k] = k
                        // console.log(k);
                    }
                    // for (let i = 0;i < tableHeader.length;i++) {
                    //     let k = tableHeader[i];
                    //     data[0][k] = k;
                    //     console.log(k);
                    // }
                    data = data.concat(rs)
                    // console.table(data)
            
                    this.exportExcel(data, '学生数据')
                }
            },
            // 导入 Excel
            importExcel () {
                // console.log(54654);
                var f = this.elImport.files[0]
                var reader = new FileReader()
                let vm = this
                reader.onload = function (e) {
                    var data = e.target.result
            
                    if (vm.rABS) {
                        // 手动转化
                        vm.wb = XLSX.read(btoa(this.fixdata(data)), {
                        type: 'base64'
                    })
                    } else {
                        vm.wb = XLSX.read(data, {
                        type: 'binary'
                        })
                    }
            
                    let json = XLSX.utils.sheet_to_json(vm.wb.Sheets[vm.wb.SheetNames[0]])
                    vm.handleImportData(json)
                }
        
                if (this.rABS) {
                    reader.readAsArrayBuffer(f)
                } else {
                    reader.readAsBinaryString(f)
                }
            },
            // 处理导入的数据
            handleImportData (data) {
                // console.log(data)
                this.loading = true;
                this.elImport.value = ''
        
                if (data.length <= 0) {
                    this.errorDialog = true
                    this.errorMsg = '请导入正确信息'
                }
                else {
                    // 把导入的数据放入表格中
                    // this.tableData = data;
                    let insertData = [];
                    // console.log("***---***");
                    // console.log(data);
                    // console.log(data[0].role == null);
                    data.forEach(item=>{
                        if(item.stu_num != '' && item.stu_num != null
                        // && item.class_name != '' && item.class_name != null
                        // && item.college != '' && item.college != null
                        && item.name != '' && item.name != null){
                            item.class_name = this.curClass_name;
                            item.college = this.curCollege;
                            if(item.group == "" || item.group == null){
                                item.group = null;
                                item.role = null;
                            }
                            if(item.role == "" || item.role == null){
                                item.role = null;
                            }
                            if(item.phone == "" || item.phone == null){
                                item.phone = null;
                            }
                            // this.allTableData.forEach(item2=>{
                            //     if(item.stu_num == item2.stu_num){
                            //         flag = false;
                            //     }
                            // })

                            // 判断用户名是否重复
                            // get_stuNumExist(item.stu_num).then(res => {
                            //     if(res.data.status == 200){
                            //         console.log(item.stu_num);
                            //         insertData.push(item);
                            //     }
                            //     else if(res.data.status == 403){
                            //         this.$router.replace('/tea_error')
                            //     }
                            //     if(){

                            //     }
                            // }).catch( error =>{
                            //     console.log(error);
                            // });
                            insertData.push(item);//判断用户名是否重复放到后端了
                        }
                    })
                    // console.log("***---***999***");
                    // console.log(insertData);
                    if(insertData.length != 0){
                        // 更新数据库
                        post_importExcel(insertData).then(res => {
                            // console.log(res.data.err);
                            if(res.data.status == 200){
                                // 重新请求表格中的数据
                                this.getClassMsg();
                                this.$message.success("导入成功，这些用户的初始密码都为123456");
                                this.loading = false;
                            }
                            else if(res.data.status == 403){
                                this.$router.replace('/tea_error')
                            }
                            else{
                                this.$message.error("导入失败");
                            }
                        }).catch( error =>{
                            console.log(error);
                            this.$message.error("导入失败");
                        });
                    }
                }
            },
            // 导出 Excel
            exportExcel (json, downName, type) {
                // console.log(654654654);
                // 获取列名
                let keyMap = []
                for (let k in json[0]) {
                keyMap.push(k)
                }
        
                // 用来保存转换好的json
                let tmpdata = []
                json.map((v, i) => keyMap.map((k, j) => Object.assign({}, {
                v: v[k],
                position: (j > 25 ? this.getCharCol(j) : String.fromCharCode(65 + j)) + (i + 1)
                }))).reduce((prev, next) => prev.concat(next)).forEach(function (v) {
                tmpdata[v.position] = {
                    v: v.v
                }
                })
        
                let outputPos = Object.keys(tmpdata)  // 设置区域，比如表格从A1到D10
                let tmpWB = {
                SheetNames: ['mySheet'], // 保存的表标题
                Sheets: {
                    'mySheet': Object.assign({},
                    tmpdata, // 内容
                    {
                        '!ref': outputPos[0] + ':' + outputPos[outputPos.length - 1] // 设置填充区域
                    })
                }
                }
        
                // 创建二进制对象写入转换好的字节流
                let tmpDown = new Blob([this.s2ab(XLSX.write(tmpWB,
                { bookType: (type === undefined ? 'xlsx' : type), bookSST: false, type: 'binary' } // 这里的数据是用来定义导出的格式类型
                ))], {
                type: ''
                })
        
                this.elExport.download = downName + '.xlsx'  // 下载名称
                this.elExport.href = URL.createObjectURL(tmpDown)  // 绑定a标签到新创建对象超链接
                this.elExport.click()  // 模拟点击实现下载
        
                // 释放，用 URL.revokeObjectURL() 释放
                setTimeout(() => URL.revokeObjectURL(tmpDown), 100)
                this.$message.success("导出成功");
            },
            // 字符串转字符流
            s2ab (s) {
                var buf = new ArrayBuffer(s.length)
                var view = new Uint8Array(buf)
                for (var i = 0; i !== s.length; ++i) {
                view[i] = s.charCodeAt(i) & 0xFF
                }
                return buf
            },
            // 将指定的自然数转换为26进制表示。映射关系：[0-25] -> [A-Z]。
            getCharCol (n) {
                let s = ''
                let m = 0
                while (n > 0) {
                m = n % 26 + 1
                s = String.fromCharCode(m + 64) + s
                n = (n - m) / 26
                }
                return s
            },
            // 文件流转 BinaryString
            fixdata (data) {
                var o = ''
                var l = 0
                var w = 10240
                for (; l < data.byteLength / w; ++l) {
                o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w, l * w + w)))
                }
                o += String.fromCharCode.apply(null, new Uint8Array(data.slice(l * w)))
                return o
            },
            current(){

            },
        }
    }

</script>

<style scoped>
    #classInfoRc{
        width:1250px;
        margin:0 auto;
        /* margin-top: 10px; */
    }
    #tb{
        box-shadow:2px 2px 2px 2px rgba(0,0,0,0.16);
        font-weight: bolder;
        font-size: 17px;
        margin-top: 5px;
    }
    .el-table {
        background-color: transparent !important;
    }
    .classInfo_table /deep/ tr, .classInfo_table /deep/ th, .classInfo_table /deep/ td {
        background: #5692ca1c !important;
        color:#095b74;
        border-bottom: 0;
    }
    .classInfo_table /deep/  .el-table tbody tr:nth-child(odd) {
        background-color: #c9e5ec !important
    }

    /* .position2PageHeader{
        color: aquamarine;
    } */
    .goBack{
        cursor: pointer;
    }
    .goBackTop{
        font-size: 20px;
        font-weight: 600;
        color: #095b74;
        /* box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04); */
        /* height: 100px; */
        /* width: 200px; */
    }
    .goBackTop2{
        /* margin: 10px; */
    }

    /* page2 */
    .plane_table{
        margin-top: 5px;
    }
    .download{
        color: #FFF;
        background-color: #124856;
        border-color: #123456;
    }
    .download:active{
        background-color:#095b74;
    }
    .el-table {
        background-color: transparent !important;
    }
    .plane_table /deep/ tr, .plane_table /deep/ th, .plane_table /deep/ td {
        background: #5692ca1c !important;
        color:#095b74;
        border-bottom: 0;
    }
    .plane_table /deep/  .el-table tbody tr:nth-child(odd) {
        background-color: #c9e5ec !important
    }
    .addStuBtn{
        margin-top: 20px;
        /* margin-left: 800px; */
        color:#000;
        width: 140px;
        height:50px;
        font-size: 18px;
        outline: none;
        background-color: #b7e5ff;
        border:1px solid rgb(22, 51, 81);
        border-radius: 10px;
    }
    .addStuBtn:active{
        background-color: #accbdf;
    }
    .el-input{
        width: 300px;
    }
    .search_stu{

    }
    .search_stu_btn{
        color: #000;
        background-color: #c2e6f1;
        /* border:0.5px solid rgb(22, 51, 81); */
    }
    .search_stu_btn:active{
        color: #000;
        background-color: #accbdf;
    }
    .btnImport{
        float:right;
        margin-right: 15px;
    }
    .btnExport{
        float:right;
    }

</style>

<style>
    .addClassDialog{
        width:530px;
    }

    /* page2 */
    .stuMsgDialog{
        width:530px;
    }
    .stuMsgDialog2{
        width:530px;
    }
</style>
