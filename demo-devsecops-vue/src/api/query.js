import axios from "axios";
import { API_VERSION } from "@/api/_prefix";

export const postMessage = (message) => {
  // console.log(`POST ${API_VERSION}/message`)
  return axios
    .post(`${API_VERSION}/message`, message, {
      headers: {
        "Content-Type": "text/plain",
      },
    })
    .then((res) => {
      return res;
    });
};

export const getMessage = () => {
  // console.log(`GET ${API_VERSION}/message`)
  return axios
    .get(`${API_VERSION}/message`, {
      "Content-Type": "text/plain",
    })
    .then((res) => {
      return res; // 纯文本！
    })
    .catch(function (error) {
      console.log(error);
    });
};
