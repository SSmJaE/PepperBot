"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[7840],{224:(e,t,n)=>{n.d(t,{Zo:()=>d,kt:()=>k});var a=n(2374);function r(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function l(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,a)}return n}function p(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?l(Object(n),!0).forEach((function(t){r(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):l(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function i(e,t){if(null==e)return{};var n,a,r=function(e,t){if(null==e)return{};var n,a,r={},l=Object.keys(e);for(a=0;a<l.length;a++)n=l[a],t.indexOf(n)>=0||(r[n]=e[n]);return r}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(a=0;a<l.length;a++)n=l[a],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(r[n]=e[n])}return r}var o=a.createContext({}),s=function(e){var t=a.useContext(o),n=t;return e&&(n="function"==typeof e?e(t):p(p({},t),e)),n},d=function(e){var t=s(e.components);return a.createElement(o.Provider,{value:t},e.children)},u="mdxType",m={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},c=a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,l=e.originalType,o=e.parentName,d=i(e,["components","mdxType","originalType","parentName"]),u=s(n),c=r,k=u["".concat(o,".").concat(c)]||u[c]||m[c]||l;return n?a.createElement(k,p(p({ref:t},d),{},{components:n})):a.createElement(k,p({ref:t},d))}));function k(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var l=n.length,p=new Array(l);p[0]=c;var i={};for(var o in t)hasOwnProperty.call(t,o)&&(i[o]=t[o]);i.originalType=e,i[u]="string"==typeof e?e:r,p[1]=i;for(var s=2;s<l;s++)p[s]=n[s];return a.createElement.apply(null,p)}return a.createElement.apply(null,n)}c.displayName="MDXCreateElement"},1372:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>o,contentTitle:()=>p,default:()=>m,frontMatter:()=>l,metadata:()=>i,toc:()=>s});var a=n(3085),r=(n(2374),n(224));const l={title:"\u6d88\u606f\u94fe"},p=void 0,i={unversionedId:"tutorial/event/message_chain",id:"tutorial/event/message_chain",title:"\u6d88\u606f\u94fe",description:"\u6700\u540e\u4e00\u6b65",source:"@site/docs/tutorial/event/message_chain.md",sourceDirName:"tutorial/event",slug:"/tutorial/event/message_chain",permalink:"/PepperBot/docs/tutorial/event/message_chain",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/tutorial/event/message_chain.md",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1684085113,formattedLastUpdatedAt:"2023\u5e745\u670814\u65e5",frontMatter:{title:"\u6d88\u606f\u94fe"},sidebar:"\u6559\u7a0b",previous:{title:"\u4e8b\u4ef6\u53c2\u6570",permalink:"/PepperBot/docs/tutorial/event/event_args"},next:{title:"\u6d88\u606f\u7247\u6bb5",permalink:"/PepperBot/docs/tutorial/event/message_segment"}},o={},s=[{value:"\u6700\u540e\u4e00\u6b65",id:"\u6700\u540e\u4e00\u6b65",level:2},{value:"\u4e3a\u4ec0\u4e48\u79f0\u4e3a\u94fe",id:"\u4e3a\u4ec0\u4e48\u79f0\u4e3a\u94fe",level:2},{value:"\u6d88\u606f\u94fe\u7684\u8de8\u5e73\u53f0",id:"\u6d88\u606f\u94fe\u7684\u8de8\u5e73\u53f0",level:2},{value:"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5",id:"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5",level:2},{value:"\u672a\u5b9e\u73b0\u7684\u6d88\u606f\u7247\u6bb5",id:"\u672a\u5b9e\u73b0\u7684\u6d88\u606f\u7247\u6bb5",level:2},{value:"\u63a5\u53d7\u5230\u7684\u6d88\u606f\u94fe",id:"\u63a5\u53d7\u5230\u7684\u6d88\u606f\u94fe",level:2},{value:"\u64cd\u4f5c\u6d88\u606f\u94fe",id:"\u64cd\u4f5c\u6d88\u606f\u94fe",level:2},{value:"\u5b57\u7b26\u4e32\u53ef\u4ee5\u76f4\u63a5 in",id:"\u5b57\u7b26\u4e32\u53ef\u4ee5\u76f4\u63a5-in",level:3},{value:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b",id:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b",level:3},{value:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b\u7684\u5b9e\u4f8b",id:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b\u7684\u5b9e\u4f8b",level:3},{value:"\u5feb\u6377\u65b9\u5f0f",id:"\u5feb\u6377\u65b9\u5f0f",level:3},{value:"\u83b7\u53d6\u6240\u6709\u6307\u5b9a\u7c7b\u578b\u5b9e\u4f8b",id:"\u83b7\u53d6\u6240\u6709\u6307\u5b9a\u7c7b\u578b\u5b9e\u4f8b",level:3},{value:"\u6309 index \u53d6 Segment",id:"\u6309-index-\u53d6-segment",level:3},{value:"\u53ef\u4ee5\u76f4\u63a5\u5224\u65ad\u5b9e\u4f8b",id:"\u53ef\u4ee5\u76f4\u63a5\u5224\u65ad\u5b9e\u4f8b",level:3},{value:"\u624b\u52a8\u6784\u9020\u6d88\u606f\u94fe",id:"\u624b\u52a8\u6784\u9020\u6d88\u606f\u94fe",level:2},{value:"\u76f4\u63a5\u4f20\u5165",id:"\u76f4\u63a5\u4f20\u5165",level:3},{value:"\u5217\u8868\u89e3\u6784",id:"\u5217\u8868\u89e3\u6784",level:3},{value:"\u51fd\u6570\u8fd4\u56de",id:"\u51fd\u6570\u8fd4\u56de",level:3},{value:"\u6d88\u606f\u94fe\u4e0a\u7ed1\u5b9a\u7684\u65b9\u6cd5",id:"\u6d88\u606f\u94fe\u4e0a\u7ed1\u5b9a\u7684\u65b9\u6cd5",level:2}],d={toc:s},u="wrapper";function m(e){let{components:t,...l}=e;return(0,r.kt)(u,(0,a.Z)({},d,l,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h2",{id:"\u6700\u540e\u4e00\u6b65"},"\u6700\u540e\u4e00\u6b65"),(0,r.kt)("p",null,"\u5728\u771f\u6b63\u5f00\u59cb\u52a8\u624b\u5b9a\u4e49\u4e8b\u4ef6\u54cd\u5e94\u4e4b\u524d\uff0c\u6211\u4eec\u6700\u540e\uff0c\u8fd8\u9700\u8981\u4e86\u89e3\u4e00\u4e0b",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe"),"\u7684\u6982\u5ff5"),(0,r.kt)("h2",{id:"\u4e3a\u4ec0\u4e48\u79f0\u4e3a\u94fe"},"\u4e3a\u4ec0\u4e48\u79f0\u4e3a\u94fe"),(0,r.kt)("p",null,(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe"),"\u5c31\u662f\u6211\u4eec\u5b9e\u9645\u4e0a\u63a5\u53d7\u5230\u7684\u6d88\u606f\uff0c\u901a\u5e38\u53c8\u6709\u8868\u60c5\uff0c\u53c8\u6709\u6587\u5b57\uff0c\u6216\u8005\u53c8\u6709\u6587\u5b57\uff0c\u53c8\u6709\u56fe\u7247"),(0,r.kt)("p",null,"\u7ec4\u6210\u6d88\u606f\u7684\u6bcf\u4e00\u4e2a\u5355\u5143\uff0c\u79f0\u4e3a\u4e00\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u7247\u6bb5")),(0,r.kt)("p",null,"\u6bd4\u5982\u8fd9\u6837\u4e00\u6761\u6d88\u606f"),(0,r.kt)("p",null,(0,r.kt)("img",{src:n(6877).Z,width:"144",height:"30"})),(0,r.kt)("p",null,"\u5b9e\u9645\u4e0a\u7531\u4e09\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u7247\u6bb5"),"\u7ec4\u6210\uff0c\u5206\u522b\u662f"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"\u6587\u5b57\u7247\u6bb5(Text)\u2014\u201412345"),(0,r.kt)("li",{parentName:"ul"},"\u8868\u60c5\u7247\u6bb5(Face)\u2014\u2014\u6ed1\u7a3d"),(0,r.kt)("li",{parentName:"ul"},"\u6587\u5b57\u7247\u6bb5(Text)\u2014\u201467890")),(0,r.kt)("h2",{id:"\u6d88\u606f\u94fe\u7684\u8de8\u5e73\u53f0"},"\u6d88\u606f\u94fe\u7684\u8de8\u5e73\u53f0"),(0,r.kt)("p",null,"\u663e\u800c\u6613\u89c1\u7684\u662f\uff0cQQ \u7684\u6d88\u606f\u7ed3\u6784\u548c\u5fae\u4fe1\u7684\u662f\u4e0d\u540c\u7684\uff0cQQ \u7684\u4e00\u6761\u6d88\u606f\uff0c\u53ef\u4ee5\u540c\u65f6\u5305\u542b\u6587\u5b57\u3001\u8868\u60c5\u3001\u56fe\u7247\uff0c\u800c\u5fae\u4fe1\u4e00\u6b21\u53ea\u80fd\u5305\u542b\u4e00\u79cd\u7c7b\u578b\uff0c\u8981\u4e48\u6587\u5b57\uff0c\u8981\u4e48\u56fe\u7247\uff0c\u8981\u4e48\u8868\u60c5"),(0,r.kt)("p",null,"\u4e3a\u4e86\u517c\u5bb9\u6027\u8003\u8651\uff0c\u4ee5 QQ \u7684",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe"),"\u6a21\u578b\u4e3a\u84dd\u672c\uff0c\u4e5f\u5c31\u662f\u8bf4\uff0c\u5fae\u4fe1\u6d88\u606f\u6240\u7ec4\u6210\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe"),"\uff0c\u6bcf\u6b21\u53ea\u6709\u4e00\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u7247\u6bb5")),(0,r.kt)("p",null,"\u5982\u679c\u4f60\u901a\u8fc7 API\uff0c\u5411\u5fae\u4fe1\u53d1\u9001\u4e86\u4e00\u4e2a\u6709\u591a\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u7247\u6bb5"),"\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe"),"\uff0cPepperBot \u4f1a\u5c06",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe"),"\u62c6\u5f00\uff0c\u6bcf\u6b21\u53ea\u53d1\u9001\u4e00\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u7247\u6bb5")),(0,r.kt)("h2",{id:"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5"},"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5"),(0,r.kt)("p",null,"PepperBot \u7684\u6d88\u606f\u7c7b\u578b\u57fa\u672c\u7b26\u5408 OneBot \u534f\u8bae\uff0c\u56e0\u4e3a\u4e3b\u8981\u540e\u7aef\u662f go-cqhttp\uff0c\u6240\u4ee5\u4ee5 go-cqhttp \u652f\u6301\u7684\u6709\u9650"),(0,r.kt)("p",null,"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5\u53ef\u4ee5\u53c2\u8003",(0,r.kt)("a",{parentName:"p",href:"/PepperBot/docs/tutorial/event/message_segment"},"\u6b64\u5904")),(0,r.kt)("p",null,"go-cqhttp \u5bf9\u6d88\u606f\u7247\u6bb5\u7684\u652f\u6301\uff0c\u53ef\u89c1",(0,r.kt)("a",{parentName:"p",href:"https://docs.go-cqhttp.org/cqcode/#qq-%E8%A1%A8%E6%83%85"},"\u6b64\u5904")),(0,r.kt)("admonition",{type:"info"},(0,r.kt)("p",{parentName:"admonition"},"\u53d1\u9001\u8bed\u97f3\u548c\u89c6\u9891\uff0c\u9700\u8981\u5c06 ffmpeg \u653e\u81f3 go-cqhttp.exe \u540c\u76ee\u5f55\u4e0b\uff0c\u6216\u8005\u5c06 ffmpeg \u7684\u53ef\u6267\u884c\u6587\u4ef6\u6dfb\u52a0\u81f3\u7cfb\u7edf\u53d8\u91cf")),(0,r.kt)("h2",{id:"\u672a\u5b9e\u73b0\u7684\u6d88\u606f\u7247\u6bb5"},"\u672a\u5b9e\u73b0\u7684\u6d88\u606f\u7247\u6bb5"),(0,r.kt)("p",null,"PepperBot\u5e76\u672a\u5b9e\u73b0\u6240\u6709QQ\u3001\u5fae\u4fe1\u652f\u6301\u7684\u6d88\u606f\u7247\u6bb5\uff0c\u5982\u679cPepperBot\u63a5\u53d7\u5230\u5c1a\u672a\u9002\u914d\u7684\u6d88\u606f\u7c7b\u578b\uff0c\u4f1a\u62a5\u9519"),(0,r.kt)("p",null,"TODO : \u6ce8\u610f\uff0c\u67d0\u4e9b\u6d88\u606f\u7247\u6bb5\uff0c\u5e76\u4e0d\u80fd\u8de8\u5e73\u53f0\uff0c\u6253\u7b97\u5b9e\u73b0\uff0c\u53ef\u4ee5\u901a\u8fc7\u914d\u7f6e\u63a7\u5236\uff0c\u9047\u5230\u4e0d\u80fd\u8de8\u5e73\u53f0\u7684\u6d88\u606f\u7247\u6bb5\uff0c\u662f\u76f4\u63a5\u62a5\u9519\uff0c\u8fd8\u662f\u5ffd\u7565"),(0,r.kt)("h2",{id:"\u63a5\u53d7\u5230\u7684\u6d88\u606f\u94fe"},"\u63a5\u53d7\u5230\u7684\u6d88\u606f\u94fe"),(0,r.kt)("p",null,"\u5728\u63a5\u53d7\u5230\u7fa4\u6d88\u606f\u4e4b\u540e\uff0cPepperBot \u4f1a\u81ea\u52a8\u5c06\u63a5\u6536\u5230\u7684\u6d88\u606f\uff0c\u8f6c\u6362\u6210\u7b26\u5408 PepperBot \u7684",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe"),"\uff0c\u5e76\u5728",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe"),"\u4e0a\u7ed1\u5b9a\u4e86\u4e00\u4e9b\u5c5e\u6027\u548c\u65b9\u6cd5\uff0c\u4fbf\u4e8e\u64cd\u4f5c",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe")),(0,r.kt)("p",null,"\u4e8b\u4ef6\u7684\u53c2\u6570\u4e2d\uff0c\u7c7b\u578b\u4e3a ",(0,r.kt)("inlineCode",{parentName:"p"},"MessageChain")," \u7684 ",(0,r.kt)("inlineCode",{parentName:"p"},"chain")," \u53c2\u6570\uff0c\u5373\u4e3a",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe")),(0,r.kt)("p",null,(0,r.kt)("inlineCode",{parentName:"p"},"chain"),"\u4e0a\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"segments"),"\u5c5e\u6027\uff0c\u5373 ",(0,r.kt)("inlineCode",{parentName:"p"},"chain.segments"),"\uff0c\u5c31\u662f\u6240\u6709\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u7247\u6bb5"),"\u4e86\uff0c\u4ed6\u662f\u4e00\u4e2a\u5217\u8868\uff0c\u5305\u542b\u6240\u6709\u6d88\u606f\u7247\u6bb5\uff0c\u53ef\u4ee5\u8fed\u4ee3"),(0,r.kt)("p",null,"\u5f53\u7136\uff0c\u4e5f\u53ef\u4ee5\u76f4\u63a5\u8fed\u4ee3\u6307\u5b9a\u7c7b\u578b\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u7247\u6bb5"),"\uff0c"),(0,r.kt)("p",null,"\u6bd4\u5982\u8fed\u4ee3\u6240\u6709\u56fe\u7247\uff0c\u53ef\u4ee5\u76f4\u63a5"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"for image in chain.images:\n    ...\n")),(0,r.kt)("p",null,"\u8fed\u4ee3\u6240\u6709\u8868\u60c5"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"for face in chain.faces:\n    ...\n")),(0,r.kt)("p",null,"\u8bf8\u5982\u6b64\u7c7b"),(0,r.kt)("p",null,"\u6587\u5b57\u6709\u6240\u4e0d\u540c\uff0c\u5e76\u6ca1\u6709\u63d0\u4f9b ",(0,r.kt)("inlineCode",{parentName:"p"},"chain.text")," \u8fd9\u6837\u4e00\u4e2a\u5c5e\u6027\uff0c\u800c\u662f\u63d0\u4f9b\u4e86 ",(0,r.kt)("inlineCode",{parentName:"p"},"chain.pure_text"),","),(0,r.kt)("p",null,"\u8fd8\u662f",(0,r.kt)("img",{src:n(6877).Z,width:"144",height:"30"}),"\u8fd9\u4e2a\u4f8b\u5b50"),(0,r.kt)("p",null,(0,r.kt)("inlineCode",{parentName:"p"},"chain.pure_text")," \u65e0\u89c6\u4e86\u4e24\u4e2a\u6587\u5b57\u7247\u6bb5\u4e2d\u95f4\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"\u8868\u60c5\u7c7b\u578b\u7247\u6bb5"),'\uff0c\u6700\u540e\u7ec4\u5408\u6210\u4e86\u4e00\u4e2a\u5b57\u7b26\u4e32\uff0c\u5b57\u7b26\u4e32\u7684\u503c\u4e3a"1234567890"'),(0,r.kt)("p",null,"\u5176\u5b83\u6d88\u606f\u7c7b\u578b\uff0c\u6bd4\u5982\u6587\u5b57+\u56fe\u7247+\u6587\u5b57\uff0c\u4e5f\u4f1a\u5ffd\u7565",(0,r.kt)("inlineCode",{parentName:"p"},"\u6587\u5b57\u7247\u6bb5"),"\u4e4b\u95f4\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"\u56fe\u7247\u7247\u6bb5"),"\uff0c\u53ea\u62fc\u63a5",(0,r.kt)("inlineCode",{parentName:"p"},"\u6587\u5b57\u7247\u6bb5")),(0,r.kt)("p",null,(0,r.kt)("inlineCode",{parentName:"p"},"pure_text")," \u5728\u5224\u65ad\u6d88\u606f\u7684\u6587\u5b57\u5185\u5bb9\u65f6\u6bd4\u8f83\u6709\u7528"),(0,r.kt)("h2",{id:"\u64cd\u4f5c\u6d88\u606f\u94fe"},"\u64cd\u4f5c\u6d88\u606f\u94fe"),(0,r.kt)("h3",{id:"\u5b57\u7b26\u4e32\u53ef\u4ee5\u76f4\u63a5-in"},"\u5b57\u7b26\u4e32\u53ef\u4ee5\u76f4\u63a5 in"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'assert "word" in chain\n')),(0,r.kt)("p",null,"\u5b9e\u9645\u4e0a\u5c31\u662f\u5224\u65ad"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'"word" in chain.pure_text\n')),(0,r.kt)("h3",{id:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b"},"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"assert Text in chain\nassert chain.has(Text) == True\n")),(0,r.kt)("p",null,"\u6240\u6709\u6d88\u606f\u7247\u6bb5\u4e2d\uff0c\u662f\u5426\u6709\u6307\u5b9a\u7c7b\u578b\u7684\u6d88\u606f\u7247\u6bb5"),(0,r.kt)("h3",{id:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b\u7684\u5b9e\u4f8b"},"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b\u7684\u5b9e\u4f8b"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'assert Text("word2") not in chain\nassert Text("word word") in chain\nassert chain.has(Text("word word")) == True\nassert chain.has(Text("word word1")) == False\nassert chain.has(Face(123)) == True\nassert chain.has(Face(124)) == False\n')),(0,r.kt)("p",null,"\u6240\u6709\u6d88\u606f\u7247\u6bb5\u4e2d\uff0c\u662f\u5426\u6709\u6307\u5b9a\u7684\u6d88\u606f\u7c7b\u578b\u7684\u6d88\u606f\u7247\u6bb5\uff0c\u540c\u65f6\uff0c\u8be5\u6d88\u606f\u7247\u6bb5\u7684\u5185\u5bb9\u5e94\u4e0e\u63d0\u4f9b\u7684\u4e00\u81f4"),(0,r.kt)("h3",{id:"\u5feb\u6377\u65b9\u5f0f"},"\u5feb\u6377\u65b9\u5f0f"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'assert chain.has_and_first(Text) == (True, Text("word word"))\nassert chain.has_and_last(Text) == (True, Text("word word2"))\nassert chain.has_and_all(Text) == (True, [Text("word word"), Text("word word2")])\n')),(0,r.kt)("p",null,"\u5982\u679c\u6709 Text \u7c7b\u578b\u7684\u6d88\u606f\u7247\u6bb5\uff0c\u76f4\u63a5\u8fd4\u56de\u8be5\u6d88\u606f\u7247\u6bb5"),(0,r.kt)("h3",{id:"\u83b7\u53d6\u6240\u6709\u6307\u5b9a\u7c7b\u578b\u5b9e\u4f8b"},"\u83b7\u53d6\u6240\u6709\u6307\u5b9a\u7c7b\u578b\u5b9e\u4f8b"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'assert chain.faces == [Face(123)]\nassert chain.text == [Text("word word"), Text("word word2")]\n')),(0,r.kt)("p",null,"\u83b7\u53d6\u6d88\u606f\u94fe\u4e2d\uff0c\u6240\u6709\u6307\u5b9a\u7c7b\u578b\u7684\u6d88\u606f\u7247\u6bb5"),(0,r.kt)("h3",{id:"\u6309-index-\u53d6-segment"},"\u6309 index \u53d6 Segment"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'assert chain[1] == Text("word word")\n')),(0,r.kt)("p",null,"\u5df2\u77e5 chain.segments \u662f\u4e00\u4e2a\u5217\u8868\uff0c\u5f53\u7136\u4e5f\u5e94\u8be5\u53ef\u4ee5\u6309 index \u83b7\u53d6"),(0,r.kt)("h3",{id:"\u53ef\u4ee5\u76f4\u63a5\u5224\u65ad\u5b9e\u4f8b"},"\u53ef\u4ee5\u76f4\u63a5\u5224\u65ad\u5b9e\u4f8b"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'assert Text("word word") == Text("word word")\nassert Text("word word") != Text("word word2")\n')),(0,r.kt)("p",null,"\u6d88\u606f\u7247\u6bb5\u4e4b\u95f4\uff0c\u4e5f\u662f\u53ef\u4ee5\u76f4\u63a5\u6bd4\u8f83\u7684"),(0,r.kt)("h2",{id:"\u624b\u52a8\u6784\u9020\u6d88\u606f\u94fe"},"\u624b\u52a8\u6784\u9020\u6d88\u606f\u94fe"),(0,r.kt)("blockquote",null,(0,r.kt)("p",{parentName:"blockquote"},"PepperBot \u63d0\u4f9b\u4e86\u975e\u5e38\u65b9\u4fbf\u7684\u6784\u9020\u6d88\u606f\u7247\u6bb5\uff0c\u4ee5\u53ca\u7ec4\u5408\u6d88\u606f\u94fe\u7684\u65b9\u5f0f")),(0,r.kt)("p",null,"PepperBot \u4e2d\uff0c\u6240\u6709\u6d89\u53ca\u5230\u4f20\u9012",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u94fe"),"\u6216\u8005",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u7247\u6bb5"),"\u7684\u51fd\u6570\uff0c\u57fa\u672c\u90fd\u5b9e\u73b0\u4e86\u8fd9\u6837\u7684\u51fd\u6570\u7b7e\u540d"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"async def group_message(*segments, iterable: Optional[Iterable]=[]):\n    ...\n")),(0,r.kt)("p",null,"\u6839\u636e\u8fd9\u4e2a\u7b7e\u540d\uff0c\u6211\u4eec\u53ef\u4ee5\u603b\u7ed3\u51fa\u4ee5\u4e0b\u901a\u7528/\u5e38\u7528\u7528\u6cd5"),(0,r.kt)("admonition",{type:"info"},(0,r.kt)("p",{parentName:"admonition"},"*","segments \u8fd9\u6837\u7684\u8bed\u6cd5\uff0c\u610f\u601d\u662f varargs\uff0c\u5373\u4efb\u610f\u4e2a\u672a\u77e5\u53c2\u6570\uff0c\u5177\u4f53\u53ef\u4ee5\u89c1 python \u5b98\u65b9\u6587\u6863\uff0c\u6216\u8005",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d41\u7545\u7684 python")," \u4e00\u4e66")),(0,r.kt)("h3",{id:"\u76f4\u63a5\u4f20\u5165"},"\u76f4\u63a5\u4f20\u5165"),(0,r.kt)("p",null,"\u5728\u8c03\u7528 API \u65f6\uff0c\u76f4\u63a5\u5c06",(0,r.kt)("inlineCode",{parentName:"p"},"\u6d88\u606f\u7247\u6bb5"),"\u4f5c\u4e3a\u53c2\u6570\uff0c\u4f20\u5165\u51fd\u6570\u8c03\u7528\u4e2d"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'await group_message(\n    Text("123"),\n    Image("filepath"),\n    Text("456"),\n)\n')),(0,r.kt)("h3",{id:"\u5217\u8868\u89e3\u6784"},"\u5217\u8868\u89e3\u6784"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'predefined_message_chain = [\n    Text("123"),\n    Image("filepath"),\n    Text("456"),\n]\n')),(0,r.kt)("p",null,"\u5982\u679c\u4f60\u5728\u522b\u5904\u5df2\u7ecf\u5b9a\u4e49\u597d\u4e86\u4e00\u4e2a\u6d88\u606f\u7247\u6bb5\u7ec4\u6210\u7684\u5217\u8868/\u5143\u7ec4\uff0c\u60f3\u8981\u5c06\u5b83\u4f5c\u4e3a API \u8c03\u7528\u65f6\u4f7f\u7528\u7684\u6d88\u606f\u7247\u6bb5\uff0c\u6709\u4e24\u79cd\u65b9\u6cd5"),(0,r.kt)("p",null,"\u76f4\u63a5\u5217\u8868\u89e3\u6784"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"await group_message(*predefined_message_chain)\n")),(0,r.kt)("p",null,"\u6216\u8005\u4f7f\u7528\u5173\u952e\u8bcd\u53c2\u6570",(0,r.kt)("inlineCode",{parentName:"p"},"iterable")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"await group_message(iterable=predefined_message_chain)\n")),(0,r.kt)("admonition",{type:"warning"},(0,r.kt)("p",{parentName:"admonition"},"\u4e0d\u8981\u540c\u65f6\u4f7f\u7528",(0,r.kt)("inlineCode",{parentName:"p"},"varargs"),"\u548c",(0,r.kt)("inlineCode",{parentName:"p"},"iterable"),"\uff0c\u5982\u679c\u540c\u65f6\u4f7f\u7528\u4e86\uff0c\u4f1a\u5ffd\u7565",(0,r.kt)("inlineCode",{parentName:"p"},"varargs"),"\uff0c\u53ea\u4f20\u9012",(0,r.kt)("inlineCode",{parentName:"p"},"iterable"),"\u6307\u5b9a\u7684\u6d88\u606f\u7247\u6bb5")),(0,r.kt)("admonition",{title:"\u8fed\u4ee3\u5668\u7684\u591a\u5904\u4f7f\u7528",type:"info"}),(0,r.kt)("h3",{id:"\u51fd\u6570\u8fd4\u56de"},"\u51fd\u6570\u8fd4\u56de"),(0,r.kt)("p",null,"\u5047\u8bbe\u6709\u4e00\u4e2a\u8fd4\u56de\u7531\u6d88\u606f\u7247\u6bb5\u7ec4\u6210\u5217\u8868\u7684\u51fd\u6570"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'def gen_message():\n    return [\n        Text("123"),\n        Image("filepath"),\n        Text("456"),\n    ]\n')),(0,r.kt)("p",null,"\u90a3\u4e48\uff0c\u53ef\u4ee5\u50cf\u4f7f\u7528\u5217\u8868\u4e00\u6837\u4f7f\u7528"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"await group_message(*gen_message())\n\nawait group_message(iterable=gen_message())\n")),(0,r.kt)("p",null,"\u5982\u679c\u51fd\u6570\u53ea\u8fd4\u56de\u4e00\u4e2a\u6d88\u606f\u7247\u6bb5\uff0c\u90a3\u4e48\u53ef\u4ee5"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'def get_image():\n    return Image("filepath")\n\nawait group_message(\n    Text("123"),\n    gen_image(),\n    Text("456"),\n)\n')),(0,r.kt)("h2",{id:"\u6d88\u606f\u94fe\u4e0a\u7ed1\u5b9a\u7684\u65b9\u6cd5"},"\u6d88\u606f\u94fe\u4e0a\u7ed1\u5b9a\u7684\u65b9\u6cd5"),(0,r.kt)("p",null,"\u6d88\u606f\u94fe\u4e0a\u7ed1\u5b9a\u7684\u65b9\u6cd5\uff0c\u90fd\u662f\u8de8\u5e73\u53f0\u7684\uff0c"),(0,r.kt)("p",null,"chain.reply"),(0,r.kt)("p",null,"chain.withdraw()"))}m.isMDXComponent=!0},6877:(e,t,n)=>{n.d(t,{Z:()=>a});const a="data:image/png;base64,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"}}]);