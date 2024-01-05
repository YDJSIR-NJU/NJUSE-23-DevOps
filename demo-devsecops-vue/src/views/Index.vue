<template>
  <div class="home" style="height: 100%">
    <el-header>
      <header-layout></header-layout>
    </el-header>
    <el-container style="height: 100%">
      <el-main style="text-align: center">
        <h1 style="margin-bottom: 1rem">获取与更新消息</h1>
        <el-row>
          <el-col :span="12">
            <el-card header="远端消息内容">
              <el-input v-model="remoteMessage" style="width: 80%" disabled>
              </el-input>
              <el-button type="primary" @click="getRemoteMessage()">
                获取消息
              </el-button>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card header="更新远端消息">
              <el-input v-model="localMessage" style="width: 80%"> </el-input>
              <el-button type="success" @click="postLocalMessage()">
                提交更新
              </el-button>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import HeaderLayout from "../components/HeaderLayout.vue";
import { getMessage, postMessage } from "@/api/query";

export default {
  name: "home",
  components: {
    HeaderLayout,
  },
  data() {
    return {
      localMessage: "",
      remoteMessage: "",
    };
  },
  methods: {
    getRemoteMessage() {
      const that = this;
      getMessage().then(function (res) {
        console.log(res.data);
        that.remoteMessage = res.data;
        that.$message.success(
          "远端消息获取成功，消息内容为" + that.remoteMessage
        );
      });
    },
    postLocalMessage() {
      const that = this;
      if (this.localMessage === "") {
        this.$message.error("消息内容不能为空");
        return;
      }
      postMessage(this.localMessage).then(function (res) {
        console.log(res.data);
        if (res.data === "OK") {
          that.$message.success("远端消息更新成功");
        } else {
          that.$message.error("远端消息更新失败");
        }
      });
    },
  },
  mounted() {
    const that = this;
  },
};
</script>

<style>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  text-align: center;
  line-height: 60px;
  margin-top: 0%;
  padding: 0;
  width: 100%;
}

.el-aside {
  background-color: #d3dce6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #e9eef3;
  color: #333;
  text-align: center;
}

body > .el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
</style>
