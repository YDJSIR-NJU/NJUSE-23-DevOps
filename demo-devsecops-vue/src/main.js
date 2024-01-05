import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import ECharts from "vue-echarts";
import VueHighlightJS from "vue-highlightjs";
import JsonViewer from "vue-json-viewer";

Vue.config.productionTip = false;

// Vue.use(Button)
// Vue.use(Select)
// Vue.use(Radio)
// Vue.use(Container)
// Vue.use(Header)
// Vue.use(Aside)
// Vue.use(Main)
// Vue.use(Menu)

Vue.use(ElementUI);
Vue.use(VueHighlightJS);
Vue.use(JsonViewer);
Vue.component("v-chart", ECharts);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
