<template>
  <el-menu
    :default-active="activeIndex"
    active-text-color="#ffd04b"
    background-color="#1E90FF"
    class="el-menu-demo"
    mode="horizontal"
    style="margin: 0 auto; width: 100%"
    text-color="#fff"
  >
    <el-menu-item
      v-for="item in menu"
      :key="item.path"
      :index="item.path"
      @click="clickMenu(item)"
    >
      <span slot="title">{{ item.label }}</span>
    </el-menu-item>
  </el-menu>
</template>
<script>
export default {
  data() {
    return {
      activeIndex: "1",
      menu: [
        {
          path: "/index",
          name: "index",
          label: "数据获取",
        },
      ],
    };
  },
  methods: {
    clickMenu(item) {
      this.$router.push({ name: item.name });
    },
  },
};
</script>
