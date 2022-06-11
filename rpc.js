
class RPC extends WebSocket{
    constructor(name,host,prot){
        let url = `ws://${host}:${prot}/ws`;
        super(url);

        this.name = name;
        this.funDic = {};
        this.onopen = function() {this.send(JSON.stringify({"msg":"register","browser":this.name}))}

        this.onmessage = function(msgEvent){
            console.log(msgEvent.data) ;
            var response = {"msg":"result","success":false}
            var data = {};
            if (msgEvent.data.match("exec"))
                data = JSON.parse(msgEvent.data);

           // {"exec": fun, "arg": arg, "resultId": resultId}

            if (data["exec"]){

                let fun = this.funDic[data["exec"]]
                // 直接eval 要是接口对外开放可能存在风险
                if (!fun){
                    this.send(JSON.stringify(response));
                    return
                }
                let ret = fun.apply(fun,eval(data["arg"]));
                response["result"] = ret;
                response["resultId"] = data["resultId"];
                response["success"] = true;

                this.send(JSON.stringify(response));}

            }
        }

        register(f){this.funDic[f.name] = f;}
}


function getCookie(){

    return document.cookie
}


function getHostName(a,b){

    return `hostname:${window.location.hostname} a:${a} b:${b} a+b=${a+b}`
}

window.__rpc = new RPC("浏览器A","127.0.0.1",5000)

window.__rpc.register(getHostName)
window.__rpc.register(getCookie)