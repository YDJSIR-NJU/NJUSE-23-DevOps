# demo-devsecops-vue

<center>2023秋南京大学软件学院《DevOps》课程第2次实践作业 网页端示例项目</center>

## 运行环境

Node 14.18.3

## 快速开始

以该项目为模板，为自己选定的流水线项目建立具有一定 DevSecOps 特性的网页端项目。

本项目设计在部署时使用 Nginx 容器部署，在部署到自己的环境时请注意反向代理指向的位置。

```yaml
location ^~ /api/ {
proxy_pass http://${APP_SERVER_IP}:8080/api/;
}
```

如使用其他部署方案，请自行做对应修改。
