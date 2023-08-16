"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[2523],{224:(e,n,t)=>{t.d(n,{Zo:()=>m,kt:()=>f});var a=t(2374);function r(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function o(e,n){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);n&&(a=a.filter((function(n){return Object.getOwnPropertyDescriptor(e,n).enumerable}))),t.push.apply(t,a)}return t}function l(e){for(var n=1;n<arguments.length;n++){var t=null!=arguments[n]?arguments[n]:{};n%2?o(Object(t),!0).forEach((function(n){r(e,n,t[n])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(n){Object.defineProperty(e,n,Object.getOwnPropertyDescriptor(t,n))}))}return e}function p(e,n){if(null==e)return{};var t,a,r=function(e,n){if(null==e)return{};var t,a,r={},o=Object.keys(e);for(a=0;a<o.length;a++)t=o[a],n.indexOf(t)>=0||(r[t]=e[t]);return r}(e,n);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(a=0;a<o.length;a++)t=o[a],n.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(e,t)&&(r[t]=e[t])}return r}var c=a.createContext({}),i=function(e){var n=a.useContext(c),t=n;return e&&(t="function"==typeof e?e(n):l(l({},n),e)),t},m=function(e){var n=i(e.components);return a.createElement(c.Provider,{value:n},e.children)},s="mdxType",d={inlineCode:"code",wrapper:function(e){var n=e.children;return a.createElement(a.Fragment,{},n)}},u=a.forwardRef((function(e,n){var t=e.components,r=e.mdxType,o=e.originalType,c=e.parentName,m=p(e,["components","mdxType","originalType","parentName"]),s=i(t),u=r,f=s["".concat(c,".").concat(u)]||s[u]||d[u]||o;return t?a.createElement(f,l(l({ref:n},m),{},{components:t})):a.createElement(f,l({ref:n},m))}));function f(e,n){var t=arguments,r=n&&n.mdxType;if("string"==typeof e||r){var o=t.length,l=new Array(o);l[0]=u;var p={};for(var c in n)hasOwnProperty.call(n,c)&&(p[c]=n[c]);p.originalType=e,p[s]="string"==typeof e?e:r,l[1]=p;for(var i=2;i<o;i++)l[i]=t[i];return a.createElement.apply(null,l)}return a.createElement.apply(null,t)}u.displayName="MDXCreateElement"},4734:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>c,contentTitle:()=>l,default:()=>d,frontMatter:()=>o,metadata:()=>p,toc:()=>i});var a=t(3085),r=(t(2374),t(224));const o={title:"\u4f7f\u7528\u6307\u4ee4"},l=void 0,p={unversionedId:"tutorial/command/use",id:"tutorial/command/use",title:"\u4f7f\u7528\u6307\u4ee4",description:"\u5728BotRoute\u4e2d\u6ce8\u518c",source:"@site/docs/tutorial/command/use.md",sourceDirName:"tutorial/command",slug:"/tutorial/command/use",permalink:"/PepperBot/docs/tutorial/command/use",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/tutorial/command/use.md",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1692177493,formattedLastUpdatedAt:"2023\u5e748\u670816\u65e5",frontMatter:{title:"\u4f7f\u7528\u6307\u4ee4"},sidebar:"\u6559\u7a0b",previous:{title:"\u4f55\u65f6\u4f7f\u7528\u6307\u4ee4",permalink:"/PepperBot/docs/tutorial/command/occasion"},next:{title:"\u914d\u7f6e\u6307\u4ee4",permalink:"/PepperBot/docs/tutorial/command/config"}},c={},i=[{value:"\u5728<code>BotRoute</code>\u4e2d\u6ce8\u518c",id:"\u5728botroute\u4e2d\u6ce8\u518c",level:2},{value:"\u901a\u8fc7\u88c5\u9970\u5668\u5f62\u5f0f\u5b9a\u4e49\u6307\u4ee4",id:"\u901a\u8fc7\u88c5\u9970\u5668\u5f62\u5f0f\u5b9a\u4e49\u6307\u4ee4",level:2},{value:"\u624b\u52a8\u201c\u8c03\u7528\u201d\u88c5\u9970\u5668\uff0c\u5c06\u540c\u4e00\u4e2a<code>class</code>\u6ce8\u518c\u4e3a\u591a\u4e2a\u6307\u4ee4",id:"\u624b\u52a8\u8c03\u7528\u88c5\u9970\u5668\u5c06\u540c\u4e00\u4e2aclass\u6ce8\u518c\u4e3a\u591a\u4e2a\u6307\u4ee4",level:2}],m={toc:i},s="wrapper";function d(e){let{components:n,...t}=e;return(0,r.kt)(s,(0,a.Z)({},m,t,{components:n,mdxType:"MDXLayout"}),(0,r.kt)("h2",{id:"\u5728botroute\u4e2d\u6ce8\u518c"},"\u5728",(0,r.kt)("inlineCode",{parentName:"h2"},"BotRoute"),"\u4e2d\u6ce8\u518c"),(0,r.kt)("p",null,"\u548c",(0,r.kt)("inlineCode",{parentName:"p"},"\u4e8b\u4ef6\u54cd\u5e94"),"\u4e2d\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u4e00\u6837\uff0c\u6211\u4eec\u4e5f\u9700\u8981\u5c06",(0,r.kt)("inlineCode",{parentName:"p"},"\u6307\u4ee4"),"\uff0c\u901a\u8fc7",(0,r.kt)("inlineCode",{parentName:"p"},"BotRoute"),"\u6ce8\u518c\u4e4b\u540e\uff0c\u624d\u80fd\u8dd1\u8d77\u6765"),(0,r.kt)("p",null,"\u914d\u7f6e\u548c",(0,r.kt)("inlineCode",{parentName:"p"},"handler"),"\u7c7b\u4f3c"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'@as_command()\nclass MyCommand:\n    pass\n\nbot.apply_routes([\n    BotRoute(\n        friends=None,\n        groups={\n            "onebot": ["123456"]\n        },\n        handlers=[],\n        commands = [MyCommand],\n    )\n])\n')),(0,r.kt)("h2",{id:"\u901a\u8fc7\u88c5\u9970\u5668\u5f62\u5f0f\u5b9a\u4e49\u6307\u4ee4"},"\u901a\u8fc7\u88c5\u9970\u5668\u5f62\u5f0f\u5b9a\u4e49\u6307\u4ee4"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"@as_command()\nclass MyCommand:\n    pass\n")),(0,r.kt)("h2",{id:"\u624b\u52a8\u8c03\u7528\u88c5\u9970\u5668\u5c06\u540c\u4e00\u4e2aclass\u6ce8\u518c\u4e3a\u591a\u4e2a\u6307\u4ee4"},"\u624b\u52a8\u201c\u8c03\u7528\u201d\u88c5\u9970\u5668\uff0c\u5c06\u540c\u4e00\u4e2a",(0,r.kt)("inlineCode",{parentName:"h2"},"class"),"\u6ce8\u518c\u4e3a\u591a\u4e2a\u6307\u4ee4"),(0,r.kt)("p",null,"\u5f53\u6211\u4eec\u4ece\u793e\u533a\u83b7\u53d6\u6307\u4ee4\u65f6\uff0c\u6709\u65f6\uff0c\u6307\u4ee4\u7684\u4f5c\u8005\u5e76\u6ca1\u6709\u5bf9\u6307\u4ee4\u5e94\u7528as_command\uff0c\u800c\u662f\u5c06\u8fd9\u4e00\u6b65\u8bb2\u7ed9\u4e86\u6211\u4eec\u6765\u5b9e\u73b0"),(0,r.kt)("p",null,"\u8fd9\u6837\uff0c\u6211\u4eec\u5c31\u80fd\u901a\u8fc7\u914d\u7f6e",(0,r.kt)("inlineCode",{parentName:"p"},"as_command"),"\u7684\u53c2\u6570\uff0c\u6765\u5b9e\u73b0\u4e0d\u540c\u7684\u6548\u679c"),(0,r.kt)("p",null,"\u6211\u4eec\u5df2\u7ecf\u53ef\u4ee5\u83b7\u53d6\u5230\u6307\u4ee4\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"class"),"\uff0c\u4f46\u662f\u4f3c\u4e4e\u6ca1\u6709\u529e\u6cd5\u5728\u8fd9\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"class"),"\u4e0a\u4f7f\u7528\u88c5\u9970\u5668\u4e86\uff0c\u56e0\u4e3a\u8fd9\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"class"),"\u5b9a\u4e49\u597d\u4e86"),(0,r.kt)("p",null,"\u8fd9\u65f6\u5019\uff0c\u6211\u4eec\u5c31\u53ef\u4ee5\u624b\u52a8\u8c03\u7528",(0,r.kt)("inlineCode",{parentName:"p"},"as_command"),"\uff0c\u6765\u5c06\u8fd9\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"class"),"\u6ce8\u518c\u4e3a\u6307\u4ee4"),(0,r.kt)("p",null,"\u56e0\u4e3a",(0,r.kt)("inlineCode",{parentName:"p"},"as_command"),"\u88c5\u9970\u5668\u7684\u672c\u8d28\uff0c\u5c31\u662f\u4e00\u4e2a\u51fd\u6570\uff0c\u8fd9\u4e2a\u51fd\u6570\uff0c\u4f1a\u8fd4\u56de\u7b2c\u4e8c\u4e2a\u51fd\u6570\uff0c\u8fd9\u4e2a\u7b2c\u4e8c\u4e2a\u51fd\u6570\uff0c\u63a5\u53d7\u4e00\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"class"),"\uff0c\u5c06\u5176\u6ce8\u518c\u4e3a\u6307\u4ee4"),(0,r.kt)("p",null,"\u6240\u4ee5"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"@as_command()\nclass MyCommand:\n    pass\n")),(0,r.kt)("p",null,"\u7b49\u4ef7\u4e8e"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},"as_command()(MyCommand)\n")),(0,r.kt)("p",null,"\u56e0\u4e3a\u6211\u4eec\u4e4b\u540e\u8981\u5c06\u6ce8\u518c\u5b8c\u6210\u7684",(0,r.kt)("inlineCode",{parentName:"p"},"class"),"\uff0c\u518d\u5e94\u7528\u5230",(0,r.kt)("inlineCode",{parentName:"p"},"BotRoute"),"\u4e2d\uff0c\u6240\u4ee5\uff0c\u6211\u4eec\u53ef\u4ee5\u5c06\u8fd9\u4e2a",(0,r.kt)("inlineCode",{parentName:"p"},"class"),"\uff0c\u8d4b\u503c\u7ed9\u4e00\u4e2a\u53d8\u91cf"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-py"},'my_command = as_command()(MyCommand)\n\nbot.apply_routes([\n    BotRoute(\n        friends=None,\n        groups={\n            "onebot": ["123456"]\n        },\n        handlers=[],\n        commands = [my_command],\n    )\n])\n')))}d.isMDXComponent=!0}}]);