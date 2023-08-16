"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[4449],{224:(e,n,t)=>{t.d(n,{Zo:()=>c,kt:()=>f});var r=t(2374);function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);n&&(r=r.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,r)}return t}function p(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){a(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function l(e,n){if(null==e)return{};var t,r,a=function(e,n){if(null==e)return{};var t,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||(a[t]=e[t]);return a}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)t=o[r],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(a[t]=e[t])}return a}var i=r.createContext({}),s=function(e){var n=r.useContext(i),t=n;return e&&(t="function"==typeof e?e(n):p(p({},n),e)),t},c=function(e){var n=s(e.components);return r.createElement(i.Provider,{value:n},e.children)},d="mdxType",u={inlineCode:"code",wrapper:function(e){var n=e.children;return r.createElement(r.Fragment,{},n)}},m=r.forwardRef((function(e,n){var t=e.components,a=e.mdxType,o=e.originalType,i=e.parentName,c=l(e,["components","mdxType","originalType","parentName"]),d=s(t),m=a,f=d["".concat(i,".").concat(m)]||d[m]||u[m]||o;return t?r.createElement(f,p(p({ref:n},c),{},{components:t})):r.createElement(f,p({ref:n},c))}));function f(e,n){var t=arguments,a=n&&n.mdxType;if("string"==typeof e||a){var o=t.length,p=new Array(o);p[0]=m;var l={};for(var i in n)hasOwnProperty.call(n,i)&&(l[i]=n[i]);l.originalType=e,l[d]="string"==typeof e?e:a,p[1]=l;for(var s=2;s<o;s++)p[s]=t[s];return r.createElement.apply(null,p)}return r.createElement.apply(null,t)}m.displayName="MDXCreateElement"},7029:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>i,contentTitle:()=>p,default:()=>u,frontMatter:()=>o,metadata:()=>l,toc:()=>s});var r=t(3085),a=(t(2374),t(224));const o={title:"\u6d4b\u8bd5"},p=void 0,l={unversionedId:"tutorial/advance/test",id:"tutorial/advance/test",title:"\u6d4b\u8bd5",description:"\u5f97\u76ca\u4e8ePepperBot\u7cbe\u7b80\u7684\u67b6\u6784\u8bbe\u8ba1(event => route => handler => api)\uff0c\u6d4b\u8bd5\u4e1a\u52a1\u903b\u8f91\u975e\u5e38\u8f7b\u677e\uff0c\u751a\u81f3\u4e0d\u9700\u8981\u63d0\u4f9b\u4e13\u95e8\u7684\u6d4b\u8bd5\u6846\u67b6",source:"@site/docs/tutorial/advance/test.md",sourceDirName:"tutorial/advance",slug:"/tutorial/advance/test",permalink:"/PepperBot/docs/tutorial/advance/test",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/tutorial/advance/test.md",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1692176874,formattedLastUpdatedAt:"2023\u5e748\u670816\u65e5",frontMatter:{title:"\u6d4b\u8bd5"},sidebar:"\u6559\u7a0b",previous:{title:"\u90e8\u7f72",permalink:"/PepperBot/docs/tutorial/advance/deploy"},next:{title:"\u5de5\u5177\u51fd\u6570",permalink:"/PepperBot/docs/tutorial/advance/utils"}},i={},s=[{value:"\u6ce8\u518c\u8def\u7531",id:"\u6ce8\u518c\u8def\u7531",level:2},{value:"\u6a21\u62df\u4e8b\u4ef6",id:"\u6a21\u62df\u4e8b\u4ef6",level:2},{value:"\u83b7\u53d6API\u8c03\u7528\u7ed3\u679c",id:"\u83b7\u53d6api\u8c03\u7528\u7ed3\u679c",level:2}],c={toc:s},d="wrapper";function u(e){let{components:n,...t}=e;return(0,a.kt)(d,(0,r.Z)({},c,t,{components:n,mdxType:"MDXLayout"}),(0,a.kt)("p",null,"\u5f97\u76ca\u4e8ePepperBot\u7cbe\u7b80\u7684\u67b6\u6784\u8bbe\u8ba1(event => route => handler => api)\uff0c\u6d4b\u8bd5\u4e1a\u52a1\u903b\u8f91\u975e\u5e38\u8f7b\u677e\uff0c\u751a\u81f3\u4e0d\u9700\u8981\u63d0\u4f9b\u4e13\u95e8\u7684\u6d4b\u8bd5\u6846\u67b6"),(0,a.kt)("p",null,"\u8be6\u7ec6\u7684\u6d4b\u8bd5\u65b9\u5f0f\uff0c\u53ef\u4ee5\u53c2\u8003",(0,a.kt)("inlineCode",{parentName:"p"},"PepperBot"),"\u7684\u6d4b\u8bd5\u4ee3\u7801(\u4ed3\u5e93\u6839\u76ee\u5f55",(0,a.kt)("inlineCode",{parentName:"p"},"tests"),"\u6587\u4ef6\u5939)\uff0c\u8fd9\u91cc\u53ea\u662f\u4ecb\u7ecd\u4e00\u4e0b\u5b9e\u73b0\u601d\u8def"),(0,a.kt)("h2",{id:"\u6ce8\u518c\u8def\u7531"},"\u6ce8\u518c\u8def\u7531"),(0,a.kt)("p",null,"\u8def\u7531\u6b63\u5e38\u6ce8\u518c\u5373\u53ef"),(0,a.kt)("h2",{id:"\u6a21\u62df\u4e8b\u4ef6"},"\u6a21\u62df\u4e8b\u4ef6"),(0,a.kt)("p",null,"\u56e0\u4e3a",(0,a.kt)("inlineCode",{parentName:"p"},"PepperBot"),"\u672c\u8eab\u5c31\u662f\u4e00\u4e2a\u4e8b\u4ef6\u9a71\u52a8\u7684\u6846\u67b6\uff0c\u6240\u4ee5\u6211\u4eec\u53ef\u4ee5\u76f4\u63a5\u6a21\u62df\u4e8b\u4ef6\uff0c\u6765\u6d4b\u8bd5\u4e1a\u52a1\u903b\u8f91\u662f\u5426\u6b63\u5e38\u6267\u884c"),(0,a.kt)("p",null,(0,a.kt)("inlineCode",{parentName:"p"},"PepperBot"),"\u5904\u7406\u4e8b\u4ef6\u7684\u6700\u4e0a\u5c42\u62bd\u8c61\uff0c\u662f",(0,a.kt)("inlineCode",{parentName:"p"},"handle_event"),"\u51fd\u6570\uff0c\u6240\u4ee5\u6211\u4eec\u53ef\u4ee5\u76f4\u63a5\u8c03\u7528\u8fd9\u4e2a\u51fd\u6570\uff0c\u6765\u6a21\u62df\u4e8b\u4ef6"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-py"},'from pepperbot.core.event.handle import handle_event\n\nawait handle_event(\n    "onebot",\n    {\n        "time": 1651692010,\n        "self_id": 123456789,\n        "post_type": "message",\n        "message_type": "group",\n        "sub_type": "normal",\n        "message_id": 1234,\n        "user_id": 987654321,\n        "message": message,\n        "raw_message": "Hello, World!",\n        "font": 123,\n        ...\n        "group_id": 1041902989,\n    }\n)\n')),(0,a.kt)("h2",{id:"\u83b7\u53d6api\u8c03\u7528\u7ed3\u679c"},"\u83b7\u53d6API\u8c03\u7528\u7ed3\u679c"),(0,a.kt)("p",null,"\u4e00\u822c\u6765\u8bf4\uff0c\u6211\u4eec\u60f3\u8981\u77e5\u9053\u4e1a\u52a1\u903b\u8f91\u662f\u5426\u6b63\u5e38\u6267\u884c\uff0c\u53ea\u9700\u8981\u68c0\u6d4b\u5bf9\u5e94\u7684API\u662f\u5426\u88ab\u8c03\u7528\u5373\u53ef"),(0,a.kt)("p",null,"\u8fd9\u91cc\u7528QQ\u4e3e\u4f8b\uff0c",(0,a.kt)("inlineCode",{parentName:"p"},"PepperBot"),"\u4e2d\uff0c\u5411",(0,a.kt)("inlineCode",{parentName:"p"},"go-cqhttp"),"\u53d1\u9001\u6d88\u606f\u7684\u6700\u5e95\u5c42API\u662f",(0,a.kt)("inlineCode",{parentName:"p"},"to_onebot"),"\uff0c\u6240\u4ee5\u6211\u4eec\u8fd9\u91cc\u76f4\u63a5mock\u5373\u53ef"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-py"},'api_results = []\n\n\ndef new_caller(self, action: str, kwargs: dict[str, Any]):\n    if action == "get_login_info":\n        return {"user_id": "123456789", "nickname": "\u6d4b\u8bd5\u673a\u5668\u4eba"}\n\n    else:\n        api_results.append((action, kwargs))\n\n\n@pytest.fixture(scope="class")\ndef patch_api_caller():\n    with patch(\n        "pepperbot.core.api.api_caller.ApiCaller.to_onebot",\n        new=new_caller,\n    ) as patched:\n        yield patched\n')),(0,a.kt)("p",null,"\u6211\u4eec\u5c06\u8c03\u7528\u60c5\u51b5\uff0c\u6536\u5f55\u5230",(0,a.kt)("inlineCode",{parentName:"p"},"api_results"),"\u4e2d\uff0c\u7136\u540e\u5728\u6d4b\u8bd5\u7528\u4f8b\u4e2d\uff0c\u65ad\u8a00",(0,a.kt)("inlineCode",{parentName:"p"},"api_results"),"\u662f\u5426\u7b26\u5408\u9884\u671f\u5373\u53ef"),(0,a.kt)("p",null,"\u6bd4\u5982\uff0c\u6211\u5148\u6ce8\u518c\u4e00\u4e2a",(0,a.kt)("inlineCode",{parentName:"p"},"command"),"\uff0c\u5982\u679c\u6ee1\u8db3\u4e00\u5b9a\u6761\u4ef6\uff0c\u5c31\u53d1\u9001",(0,a.kt)("inlineCode",{parentName:"p"},"hello world"),"\uff0c\u90a3\u4e48\uff0c\u6211\u5c31\u53ef\u4ee5\u8fd9\u6837\u5224\u65ad"),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-py"},'bot = PepperBot()\n\nbot.register_adapter(\n    bot_protocol="onebot",\n    receive_protocol="http",\n    backend_protocol="http",\n    backend_host="127.0.0.1",\n    backend_port=5700,\n)\n\n@as_command(\n    need_prefix=True,\n    prefixes=["/"],\n    aliases=["command"],\n)\nclass TestCommand:\n    async def initial(self, sender: CommandSender):\n        await sender.send("Hello, World!")\n\n\nbot.apply_routes(\n    [\n        BotRoute(\n            commands=[TestCommand],\n            groups="*",\n        )\n    ]\n)\n\n# \u4e0d\u9700\u8981run\uff0c\u6211\u4eec\u76f4\u63a5\u8c03\u7528handle_event\u6765\u6a21\u62df\u4e8b\u4ef6\nawait handle_event(\n    "onebot",\n    {\n        "time": 1651692010,\n        "self_id": 123456789,\n        "post_type": "message",\n        "message_type": "group",\n        "sub_type": "normal",\n        "message_id": 1234,\n        "user_id": 987654321,\n        "message": message,\n        "raw_message": "/command",\n        "font": 123,\n        ...\n        "group_id": 1041902989,\n    }\n)\n\n# \u8fd9\u91cc\u4e0d\u4e00\u5b9a\u548c\u5b9e\u9645\u7684\u53c2\u6570\u4e00\u81f4\uff0c\u7406\u89e3\u601d\u8def\u5373\u53ef\nassert api_results == [\n    ("send_group_msg", {"message": "Hello, World!", "group_id": 1041902989}) \n]\n')))}u.isMDXComponent=!0}}]);