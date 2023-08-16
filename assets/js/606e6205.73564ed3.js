"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[7391],{224:(e,n,t)=>{t.d(n,{Zo:()=>m,kt:()=>N});var a=t(2374);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function l(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function p(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?l(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):l(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function i(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},l=Object.keys(e);for(a=0;a<l.length;a++)t=l[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(a=0;a<l.length;a++)t=l[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var o=a.createContext({}),d=function(e){var n=a.useContext(o),t=n;return e&&(t="function"==typeof e?e(n):p(p({},n),e)),t},m=function(e){var n=d(e.components);return a.createElement(o.Provider,{value:n},e.children)},k="mdxType",c={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},u=a.forwardRef((function(e,n){var t=e.components,r=e.mdxType,l=e.originalType,o=e.parentName,m=i(e,["components","mdxType","originalType","parentName"]),k=d(t),u=r,N=k["".concat(o,".").concat(u)]||k[u]||c[u]||l;return t?a.createElement(N,p(p({ref:n},m),{},{components:t})):a.createElement(N,p({ref:n},m))}));function N(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var l=t.length,p=new Array(l);p[0]=u;var i={};for(var o in n)hasOwnProperty.call(n,o)&&(i[o]=n[o]);i.originalType=e,i[k]="string"==typeof e?e:r,p[1]=i;for(var d=2;d<l;d++)p[d]=t[d];return a.createElement.apply(null,p)}return a.createElement.apply(null,t)}u.displayName="MDXCreateElement"},641:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>o,contentTitle:()=>p,default:()=>c,frontMatter:()=>l,metadata:()=>i,toc:()=>d});var a=t(3085),r=(t(2374),t(224));const l={title:"\u4e8b\u4ef6\u4f20\u64ad\u4e0e\u4f18\u5148\u7ea7"},p=void 0,i={unversionedId:"tutorial/advance/propagation",id:"tutorial/advance/propagation",title:"\u4e8b\u4ef6\u4f20\u64ad\u4e0e\u4f18\u5148\u7ea7",description:"\u5f53\u6211\u4eec\u6709\u5f88\u591ahandler\u3001command\u65f6\uff0c\u5f88\u53ef\u80fd\u6709\u8fd9\u6837\u7684\u573a\u666f",source:"@site/docs/tutorial/advance/propagation.md",sourceDirName:"tutorial/advance",slug:"/tutorial/advance/propagation",permalink:"/PepperBot/docs/tutorial/advance/propagation",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/tutorial/advance/propagation.md",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1692177493,formattedLastUpdatedAt:"2023\u5e748\u670816\u65e5",frontMatter:{title:"\u4e8b\u4ef6\u4f20\u64ad\u4e0e\u4f18\u5148\u7ea7"},sidebar:"\u6559\u7a0b",previous:{title:"\u4e00\u4e2a\u5c0f\u76ee\u6807",permalink:"/PepperBot/docs/tutorial/command/define"},next:{title:"\u6743\u9650\u63a7\u5236",permalink:"/PepperBot/docs/tutorial/advance/available"}},o={},d=[{value:"<code>PepperBot</code>\u7684\u4e8b\u4ef6\u4f20\u64ad\u673a\u5236",id:"pepperbot\u7684\u4e8b\u4ef6\u4f20\u64ad\u673a\u5236",level:2},{value:"<code>handler</code>\u7684\u5e76\u53d1\u6267\u884c",id:"handler\u7684\u5e76\u53d1\u6267\u884c",level:3},{value:"<code>PepperBot</code>\u5982\u4f55\u5904\u7406\uff0c\u540c\u65f6\u5b58\u5728<code>\u5e76\u53d1\u6267\u884c</code>\u4e0e<code>\u987a\u5e8f\u6267\u884c</code>\u7684\u60c5\u51b5",id:"pepperbot\u5982\u4f55\u5904\u7406\u540c\u65f6\u5b58\u5728\u5e76\u53d1\u6267\u884c\u4e0e\u987a\u5e8f\u6267\u884c\u7684\u60c5\u51b5",level:3},{value:"\u987a\u5e8f\u6267\u884c\u4ee5\u5b9e\u73b0\u4e8b\u4ef6\u4f20\u64ad\u7684\u63a7\u5236",id:"\u987a\u5e8f\u6267\u884c\u4ee5\u5b9e\u73b0\u4e8b\u4ef6\u4f20\u64ad\u7684\u63a7\u5236",level:3},{value:"\u901a\u8fc7\u5bf9\u4f20\u64ad\u8fdb\u884c\u5206\u7ec4\uff0c\u907f\u514d\u5e72\u6270",id:"\u901a\u8fc7\u5bf9\u4f20\u64ad\u8fdb\u884c\u5206\u7ec4\u907f\u514d\u5e72\u6270",level:2},{value:"\u5177\u4f53\u5982\u4f55\u8bbe\u7f6e",id:"\u5177\u4f53\u5982\u4f55\u8bbe\u7f6e",level:2},{value:"\u8bbe\u7f6e<code>class_handler</code>",id:"\u8bbe\u7f6eclass_handler",level:3},{value:"\u8bbe\u7f6e<code>class_command</code>",id:"\u8bbe\u7f6eclass_command",level:3}],m={toc:d},k="wrapper";function c(e){let{components:n,...l}=e;return(0,r.kt)(k,(0,a.Z)({},m,l,{components:n,mdxType:"MDXLayout"}),(0,r.kt)("p",null,"\u5f53\u6211\u4eec\u6709\u5f88\u591a",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command"),"\u65f6\uff0c\u5f88\u53ef\u80fd\u6709\u8fd9\u6837\u7684\u573a\u666f"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"\u6211\u5e0c\u671b\u5b9e\u73b0\u4e00\u4e2a\u62e6\u622a\u6027\u8d28\u7684",(0,r.kt)("inlineCode",{parentName:"li"},"handler"),"\uff0c\u5bf9\u4e8b\u4ef6\u8fdb\u884c\u9884\u5904\u7406\uff0c\u53ea\u6709\u6ee1\u8db3\u8981\u6c42\u65f6\uff0c\u624d\u653e\u884c\u7ed9\u540e\u7eed\u7684\u5176\u4ed6",(0,r.kt)("inlineCode",{parentName:"li"},"handler"),"\u5904\u7406"),(0,r.kt)("li",{parentName:"ul"},"\u6211\u5e0c\u671b\u5b9e\u73b0\u9009\u62e9\u6027\u7684\u6267\u884c\u67d0\u4e9b",(0,r.kt)("inlineCode",{parentName:"li"},"handler"),"\uff0c\u5f53\u6267\u884c\u4e86\u5176\u4e2d\u4efb\u4f55\u4e00\u4e2a\uff0c\u5c31\u653e\u5f03\u6267\u884c\u5176\u4ed6\u7684",(0,r.kt)("inlineCode",{parentName:"li"},"handler"))),(0,r.kt)("p",null,"\u63a5\u4e0b\u6765\uff0c\u6211\u4eec\u5c06\u4ecb\u7ecd\u5982\u4f55\u5b9e\u73b0\u7b2c\u4e00\u6761\uff0c\u7b2c\u4e8c\u6761\u5982\u4f55\u5b9e\u73b0\uff0c\u89c1",(0,r.kt)("a",{parentName:"p",href:"./available"},"\u6743\u9650\u63a7\u5236")),(0,r.kt)("h2",{id:"pepperbot\u7684\u4e8b\u4ef6\u4f20\u64ad\u673a\u5236"},(0,r.kt)("inlineCode",{parentName:"h2"},"PepperBot"),"\u7684\u4e8b\u4ef6\u4f20\u64ad\u673a\u5236"),(0,r.kt)("p",null,(0,r.kt)("img",{src:t(832).Z,width:"1229",height:"144"})),(0,r.kt)("p",null,"\u5f53\u63a5\u53d7\u5230\u4e00\u4e2a\u4e8b\u4ef6\u65f6\uff0c",(0,r.kt)("inlineCode",{parentName:"p"},"PepperBot"),"\u4f1a\u5c06\u6240\u6709\u53ef\u7528\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command"),"\uff0c\u6309\u7167",(0,r.kt)("inlineCode",{parentName:"p"},"priority"),"\u8fdb\u884c\u6392\u5e8f\uff0c",(0,r.kt)("inlineCode",{parentName:"p"},"priority"),"\u8d8a\u5927\uff0c\u8d8a\u9760\u524d"),(0,r.kt)("p",null,"\u9ed8\u8ba4\u60c5\u51b5\u4e0b\uff0c\u5982\u679c\u6ca1\u6709\u4efb\u4f55",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command"),"\u963b\u65ad\u4e8b\u4ef6\u7684\u4f20\u64ad(stop propagation)\uff0c\u90a3\u4e48\u5c31\u4f9d\u6b21\u6267\u884c"),(0,r.kt)("p",null,"\u5982\u679c\u6709",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command"),"\u963b\u65ad\u4e86\u4e8b\u4ef6\u7684\u4f20\u64ad\uff0c\u90a3\u4e48\u5c31\u4e0d\u4f1a\u6267\u884c\u540e\u7eed\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command")),(0,r.kt)("p",null,"\u4f46\u662f\uff0c\u6709\u4e00\u4e2a\u524d\u63d0\uff0c\u5c31\u662f",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command"),"\u5fc5\u987b\u8bbe\u7f6e",(0,r.kt)("inlineCode",{parentName:"p"},"concurrency"),"\u4e3a",(0,r.kt)("inlineCode",{parentName:"p"},"False")),(0,r.kt)("h3",{id:"handler\u7684\u5e76\u53d1\u6267\u884c"},(0,r.kt)("inlineCode",{parentName:"h3"},"handler"),"\u7684\u5e76\u53d1\u6267\u884c"),(0,r.kt)("p",null,"\u5bf9\u4e8e\u5927\u591a\u6570\u7684\u4f7f\u7528\u573a\u666f\u6765\u8bf4\uff0c\u6211\u4eec\u5e0c\u671b",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u662f\u5e76\u53d1\u6267\u884c\u7684\uff0c\u8fd9\u6837\u53ef\u4ee5\u63d0\u9ad8\u6027\u80fd"),(0,r.kt)("p",null,"\u5982\u679c\u4e0d\u5e76\u53d1(\u4e5f\u5c31\u662f\u987a\u5e8f\u6267\u884c)\uff0c\u4f1a\u662f\u4ec0\u4e48\u6837\u5b50\u5462\uff1f"),(0,r.kt)("p",null,"\u5047\u8bbe\u6211\u4eec\u6709\u4e00\u4e2a\u6bd4\u8f83\u8017\u65f6\u7684\u3001\u5e76\u4e14\u662f\u963b\u585e\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\uff0c\u90a3\u4e48\u76f4\u5230\u8fd9\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u6267\u884c\u5b8c\u6bd5\uff0c",(0,r.kt)("inlineCode",{parentName:"p"},"PepperBot"),"\u624d\u4f1a\u7ee7\u7eed\u6267\u884c\u540e\u7eed\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler")),(0,r.kt)("p",null,"\u5982\u679c",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u4e4b\u95f4\u5e76\u6ca1\u6709\u903b\u8f91\u4e0a\u7684\u8054\u7cfb(\u4e5f\u5c31\u662f\u8bf4\uff0c\u65e0\u6240\u8c13\u6267\u884c\u7684\u5148\u540e\u987a\u5e8f)\uff0c\u90a3\u4e48\u8fd9\u6837\u7684\u6267\u884c\u65b9\u5f0f\uff0c\u663e\u7136\u4f1a\u663e\u8457\u7684\u964d\u4f4e\u54cd\u5e94\u901f\u5ea6(\u56e0\u4e3a\u8981\u7b49\u5f85\u4e4b\u524d\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u6267\u884c\u5b8c\u6bd5)"),(0,r.kt)("h3",{id:"pepperbot\u5982\u4f55\u5904\u7406\u540c\u65f6\u5b58\u5728\u5e76\u53d1\u6267\u884c\u4e0e\u987a\u5e8f\u6267\u884c\u7684\u60c5\u51b5"},(0,r.kt)("inlineCode",{parentName:"h3"},"PepperBot"),"\u5982\u4f55\u5904\u7406\uff0c\u540c\u65f6\u5b58\u5728",(0,r.kt)("inlineCode",{parentName:"h3"},"\u5e76\u53d1\u6267\u884c"),"\u4e0e",(0,r.kt)("inlineCode",{parentName:"h3"},"\u987a\u5e8f\u6267\u884c"),"\u7684\u60c5\u51b5"),(0,r.kt)("p",null,"\u5047\u8bbe\u6211\u4eec\u6709\u8fd9\u6837\u51e0\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command")),(0,r.kt)("table",null,(0,r.kt)("thead",{parentName:"table"},(0,r.kt)("tr",{parentName:"thead"},(0,r.kt)("th",{parentName:"tr",align:null},"priority"),(0,r.kt)("th",{parentName:"tr",align:null},"concurrency"),(0,r.kt)("th",{parentName:"tr",align:null},"type"),(0,r.kt)("th",{parentName:"tr",align:null},"name"))),(0,r.kt)("tbody",{parentName:"table"},(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"500"),(0,r.kt)("td",{parentName:"tr",align:null},"True"),(0,r.kt)("td",{parentName:"tr",align:null},"class_handler"),(0,r.kt)("td",{parentName:"tr",align:null},"handler1")),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"400"),(0,r.kt)("td",{parentName:"tr",align:null},"True"),(0,r.kt)("td",{parentName:"tr",align:null},"class_command"),(0,r.kt)("td",{parentName:"tr",align:null},"command1")),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"300"),(0,r.kt)("td",{parentName:"tr",align:null},"False"),(0,r.kt)("td",{parentName:"tr",align:null},"class_handler"),(0,r.kt)("td",{parentName:"tr",align:null},"handler2")),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"200"),(0,r.kt)("td",{parentName:"tr",align:null},"False"),(0,r.kt)("td",{parentName:"tr",align:null},"class_command"),(0,r.kt)("td",{parentName:"tr",align:null},"command2")),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"100"),(0,r.kt)("td",{parentName:"tr",align:null},"True"),(0,r.kt)("td",{parentName:"tr",align:null},"class_handler"),(0,r.kt)("td",{parentName:"tr",align:null},"handler3")),(0,r.kt)("tr",{parentName:"tbody"},(0,r.kt)("td",{parentName:"tr",align:null},"0"),(0,r.kt)("td",{parentName:"tr",align:null},"True"),(0,r.kt)("td",{parentName:"tr",align:null},"class_command"),(0,r.kt)("td",{parentName:"tr",align:null},"command3")))),(0,r.kt)("p",null,(0,r.kt)("img",{src:t(4300).Z,width:"1672",height:"453"})),(0,r.kt)("p",null,"\u53ef\u4ee5\u770b\u5230\uff0c",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command2"),"\u662f\u987a\u5e8f\u6267\u884c\u7684\uff0c\u800c\u5176\u4ed6\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command"),"\u662f\u5e76\u53d1\u6267\u884c\u7684"),(0,r.kt)("p",null,"\u540c\u65f6\uff0c\u56e0\u4e3a",(0,r.kt)("inlineCode",{parentName:"p"},"handler1"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command1"),"\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"priority"),"\u6bd4",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command2"),"\u5927\uff0c\u6240\u4ee5",(0,r.kt)("inlineCode",{parentName:"p"},"handler1"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command1"),"\u4f1a\u5148\u4e8e",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command2"),"\u6267\u884c"),(0,r.kt)("p",null,"\u56e0\u4e3a",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command2"),"\u662f\u975e\u5e76\u53d1\u7684\uff0c\u6240\u4ee5",(0,r.kt)("inlineCode",{parentName:"p"},"handler3"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command3"),"\u4f1a\u5728",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command2"),"\u6267\u884c\u5b8c\u6bd5\u540e\uff0c\u624d\u4f1a\u6267\u884c"),(0,r.kt)("p",null,"\u6216\u8005\u6362\u53e5\u8bdd\u8bf4\uff0c\u5982\u679c\u5728\u6309\u7167",(0,r.kt)("inlineCode",{parentName:"p"},"priority"),"\u6392\u5e8f\u540e\u7684handler\u4e2d\uff0c\u5982\u679c\u5b58\u5728\u975e\u5e76\u53d1\u7684handler\uff0c\u5219\u4f1a\u5728\u6267\u884c\u8be5handler\u4e4b\u524d\uff0c\u4f1a\u7b49\u5f85\u8be5handler\u4e4b\u524d\u6240\u6709\u7684\u5e76\u53d1handler\u6267\u884c\u5b8c\u6bd5"),(0,r.kt)("h3",{id:"\u987a\u5e8f\u6267\u884c\u4ee5\u5b9e\u73b0\u4e8b\u4ef6\u4f20\u64ad\u7684\u63a7\u5236"},"\u987a\u5e8f\u6267\u884c\u4ee5\u5b9e\u73b0\u4e8b\u4ef6\u4f20\u64ad\u7684\u63a7\u5236"),(0,r.kt)("p",null,"\u53ea\u6709\u5f53\u4e00\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u6216\u8005",(0,r.kt)("inlineCode",{parentName:"p"},"command"),"\u6267\u884c\u5b8c\u6210\uff0c\u6211\u4eec\u624d\u80fd\u77e5\u9053\uff0c\u8be5",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u662f\u5426\u963b\u65ad\u4e86\u4e8b\u4ef6\u7684\u4f20\u64ad"),(0,r.kt)("p",null,"\u4ece\u4e0a\u56fe\u53ef\u4ee5\u770b\u5230\uff0c",(0,r.kt)("inlineCode",{parentName:"p"},"handler1"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command1"),"\u662f\u5e76\u53d1\u6267\u884c\u7684\uff0c\u6240\u4ee5\u5047\u8bbe",(0,r.kt)("inlineCode",{parentName:"p"},"handler1"),"\u963b\u65ad\u4e86\u4e8b\u4ef6\u7684\u4f20\u64ad\uff0c\u56e0\u4e3a\u5e76\u53d1(\u540c\u65f6)\u6267\u884c\u7684\u539f\u56e0\uff0c\u6b64\u65f6",(0,r.kt)("inlineCode",{parentName:"p"},"command1"),"\u5df2\u7ecf\u6267\u884c\u4e86\uff0c\u6240\u4ee5\u6b64\u65f6",(0,r.kt)("inlineCode",{parentName:"p"},"stop propagation"),"\u5e76\u672a\u8d77\u6548\uff0c\u867d\u7136",(0,r.kt)("inlineCode",{parentName:"p"},"handler1"),"\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"\u4f18\u5148\u7ea7"),"\u6bd4",(0,r.kt)("inlineCode",{parentName:"p"},"command2"),"\u7684\u9ad8"),(0,r.kt)("p",null,"\u4f46\u662f\uff0c\u5bf9\u4e8e",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\u6765\u8bf4\uff0c\u5b83\u662f\u987a\u5e8f\u6267\u884c\u7684\uff0c\u6240\u4ee5\u5728",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\u6267\u884c\u4e4b\u524d\uff0c\u4f1a\u7b49\u5f85",(0,r.kt)("inlineCode",{parentName:"p"},"handler1"),"\u6267\u884c\u5b8c\u6bd5\uff0c\u6b64\u65f6\uff0c\u5982\u679c",(0,r.kt)("inlineCode",{parentName:"p"},"handler1"),"\u963b\u65ad\u4e86\u4e8b\u4ef6\u7684\u4f20\u64ad\uff0c\u90a3\u4e48",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\u5c31\u4e0d\u4f1a\u6267\u884c\u4e86"),(0,r.kt)("p",null,"\u6240\u4ee5\u603b\u7ed3\u4e00\u4e0b\uff0c\u5982\u679c\u6211\u4eec\u5e0c\u671b\u5b9e\u73b0\u4e8b\u4ef6\u4f20\u64ad\u7684\u63a7\u5236\uff0c\u90a3\u4e48\u6211\u4eec\u53ef\u4ee5\u5c06",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command"),"\u8bbe\u7f6e\u4e3a\u987a\u5e8f\u6267\u884c\uff0c\u8fd9\u6837\u5c31\u53ef\u4ee5\u5728",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u3001",(0,r.kt)("inlineCode",{parentName:"p"},"command"),"\u6267\u884c\u5b8c\u6bd5\u540e\uff0c\u77e5\u9053\u662f\u5426\u963b\u65ad\u4e86\u4e8b\u4ef6\u7684\u4f20\u64ad"),(0,r.kt)("h2",{id:"\u901a\u8fc7\u5bf9\u4f20\u64ad\u8fdb\u884c\u5206\u7ec4\u907f\u514d\u5e72\u6270"},"\u901a\u8fc7\u5bf9\u4f20\u64ad\u8fdb\u884c\u5206\u7ec4\uff0c\u907f\u514d\u5e72\u6270"),(0,r.kt)("p",null,"\u56de\u5230\u6211\u4eec\u4e00\u5f00\u59cb\u5047\u8bbe\u7684\u573a\u666f"),(0,r.kt)("blockquote",null,(0,r.kt)("p",{parentName:"blockquote"},"\u6211\u5e0c\u671b\u5b9e\u73b0\u4e00\u4e2a\u62e6\u622a\u6027\u8d28\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\uff0c\u5bf9\u4e8b\u4ef6\u8fdb\u884c\u9884\u5904\u7406\uff0c\u53ea\u6709\u6ee1\u8db3\u8981\u6c42\u65f6\uff0c\u624d\u653e\u884c\u7ed9\u540e\u7eed\u7684\u5176\u4ed6",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u5904\u7406")),(0,r.kt)("p",null,"\u5982\u679c\u6211\u7684\u8fd9\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"\u62e6\u622ahandler"),"\uff0c\u53ea\u60f3\u4f5c\u7528\u4e8e\u540e\u7eed\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\uff0c\u800c\u5b8c\u5168\u4e0d\u5173\u5fc3\u5176\u4ed6\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler")),(0,r.kt)("p",null,"\u5047\u8bbe\u6b64\u65f6",(0,r.kt)("inlineCode",{parentName:"p"},"\u62e6\u622ahandler"),"\u963b\u65ad\u4e86\u4f20\u64ad\uff0c\u867d\u7136\u786e\u5b9e\u5b9e\u73b0\u4e86\u62e6\u622a",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\u7684\u6267\u884c\uff0c\u4f46\u662f\u540c\u65f6\uff0c\u4e5f\u5f71\u54cd\u4e86\u5176\u4ed6\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler")),(0,r.kt)("p",null,"\u90a3\u4e48\uff0c\u6211\u4eec\u53ef\u4ee5\u901a\u8fc7\u5bf9\u4f20\u64ad\u8fdb\u884c\u5206\u7ec4\uff0c\u6765\u907f\u514d\u8fd9\u79cd\u5e72\u6270"),(0,r.kt)("p",null,(0,r.kt)("img",{src:t(8231).Z,width:"1065",height:"487"})),(0,r.kt)("p",null,"\u73b0\u5728\uff0c\u5f53",(0,r.kt)("inlineCode",{parentName:"p"},"\u62e6\u622ahandler"),"\u963b\u65ad\u4e86\u4f20\u64ad\u65f6\uff0c\u53ea\u4f1a\u5f71\u54cd\u540c\u4e00\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"\u4f20\u64ad\u7ec4"),"\u4e2d\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler2"),"\uff0c\u800c\u4e0d\u4f1a\u5f71\u54cd\u5230\u5176\u4ed6\u4f20\u64ad\u7ec4"),(0,r.kt)("p",null,"\u591a\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"\u4f20\u64ad\u7ec4"),"\u4e4b\u95f4\uff0c\u65e2\u7136\u6ca1\u6709\u4e86\u903b\u8f91\u4e0a\u7684\u8054\u7cfb\uff0c\u81ea\u7136\u4e5f\u662f\u5e76\u53d1\u6267\u884c\u7684"),(0,r.kt)("h2",{id:"\u5177\u4f53\u5982\u4f55\u8bbe\u7f6e"},"\u5177\u4f53\u5982\u4f55\u8bbe\u7f6e"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"priority"),"\u9ed8\u8ba4\u4e3a",(0,r.kt)("inlineCode",{parentName:"li"},"0")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"concurrency"),"\u9ed8\u8ba4\u4e3a",(0,r.kt)("inlineCode",{parentName:"li"},"True")),(0,r.kt)("li",{parentName:"ul"},(0,r.kt)("inlineCode",{parentName:"li"},"propagation_group"),"\u9ed8\u8ba4\u4e3a",(0,r.kt)("inlineCode",{parentName:"li"},"default"))),(0,r.kt)("h3",{id:"\u8bbe\u7f6eclass_handler"},"\u8bbe\u7f6e",(0,r.kt)("inlineCode",{parentName:"h3"},"class_handler")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'from pepperbot.store.event import PropagationConfig\n\nclass MyHandler:\n    config = PropagationConfig(\n        priority=100,\n        concurrency=False,\n        propagation_group="test",\n    )\n\n    async def group_message(self, ...):\n        ...\n')),(0,r.kt)("h3",{id:"\u8bbe\u7f6eclass_command"},"\u8bbe\u7f6e",(0,r.kt)("inlineCode",{parentName:"h3"},"class_command")),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'@as_command(\n    ...\n    priority=100,\n    concurrency=False,\n    propagation_group="test",\n)\nclass MyCommand:\n    ...\n')))}c.isMDXComponent=!0},4300:(e,n,t)=>{t.d(n,{Z:()=>a});const a=t.p+"assets/images/concurrency_propagation.excalidraw-6b058593c38bdbf346d34eeba3ded755.png"},832:(e,n,t)=>{t.d(n,{Z:()=>a});const a=t.p+"assets/images/propagation.excalidraw-37b5f7f45ae0b2d05b49189a5ebf88a7.png"},8231:(e,n,t)=>{t.d(n,{Z:()=>a});const a=t.p+"assets/images/propagation_group.excalidraw-a80bfddc0fa2ba670aa0914ea4ddcc77.png"}}]);