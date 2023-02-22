# JSRPC 
远程调用JS,实时调用JS,免去补环境的烦恼！

JSRPC已经合并在[RPCServer](https://github.com/71n9/RPCServer)

RPCServer 同时支持JavaScript Android远程调用，聚合接口统一管理，基于socket服务 只要有网络即可调用 解除内网限制。

## 使用方法
### 一. 配置环境
  - 1.Python3环境
  - 2.一键安装所需库 pip install -r requirements.txt
  
### 二. 启动使用
  - 1.启动Python脚本main.py文件:启动地址端口默认是【127.0.0.1:5123】 可自行修改
  ![image](https://user-images.githubusercontent.com/44369205/173170154-c408b9b3-5dfe-4ed2-a81d-709b049559e7.png)

  #### 2.绑定浏览器+调用JS 
    
   - 浏览器先执行rpc.js文件进行绑定浏览器,默认注册两个函数getCookie和getHostName 使用register方法可自行注册其他方法
   - 绑定浏览器方法
```js
new RPC("浏览器A","127.0.0.1",5123);
```
   - 注册函数方法 register(getHostName) 传入需要调用的函数即可
   
   - 调用JS http://127.0.0.1:5123/get?browser=【绑定浏览器时传入的名称】&fun=【需要调用执行的函数】&arg=【传入的参数以数组形式】
   - 例:http://127.0.0.1:5123/get?browser=浏览器A&fun=getHostName&arg=[300,2]
   
  ![image](https://user-images.githubusercontent.com/44369205/173170791-4f55b1da-23e9-45f8-acac-31176868ebe3.png)


