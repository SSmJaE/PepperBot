"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[8168],{224:(e,t,r)=>{r.d(t,{Zo:()=>u,kt:()=>f});var n=r(2374);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function l(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var c=n.createContext({}),p=function(e){var t=n.useContext(c),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},u=function(e){var t=p(e.components);return n.createElement(c.Provider,{value:t},e.children)},s="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},m=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,c=e.parentName,u=l(e,["components","mdxType","originalType","parentName"]),s=p(r),m=a,f=s["".concat(c,".").concat(m)]||s[m]||d[m]||o;return r?n.createElement(f,i(i({ref:t},u),{},{components:r})):n.createElement(f,i({ref:t},u))}));function f(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,i=new Array(o);i[0]=m;var l={};for(var c in t)hasOwnProperty.call(t,c)&&(l[c]=t[c]);l.originalType=e,l[s]="string"==typeof e?e:a,i[1]=l;for(var p=2;p<o;p++)i[p]=r[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}m.displayName="MDXCreateElement"},9131:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>c,contentTitle:()=>i,default:()=>d,frontMatter:()=>o,metadata:()=>l,toc:()=>p});var n=r(3085),a=(r(2374),r(224));const o={title:"\u5b9a\u65f6\u4efb\u52a1"},i=void 0,l={unversionedId:"tutorial/action/crontab",id:"tutorial/action/crontab",title:"\u5b9a\u65f6\u4efb\u52a1",description:"PepperBot \u96c6\u6210\u4e86apscheduler\uff0c\u53ef\u4ee5\u975e\u5e38\u8f7b\u677e\u7684\u5b9e\u73b0\u5f02\u6b65\u5b9a\u65f6\u4efb\u52a1(\u540c\u6b65\u4efb\u52a1\u4e5f\u53ef\u4ee5)",source:"@site/docs/tutorial/action/crontab.md",sourceDirName:"tutorial/action",slug:"/tutorial/action/crontab",permalink:"/PepperBot/docs/tutorial/action/crontab",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/tutorial/action/crontab.md",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1682179822,formattedLastUpdatedAt:"2023\u5e744\u670822\u65e5",frontMatter:{title:"\u5b9a\u65f6\u4efb\u52a1"},sidebar:"\u6559\u7a0b",previous:{title:"\u4e00\u6b21\u6027\u4efb\u52a1",permalink:"/PepperBot/docs/tutorial/action/disposable"},next:{title:"\u4f55\u65f6\u4f7f\u7528\u6307\u4ee4",permalink:"/PepperBot/docs/tutorial/command/occasion"}},c={},p=[],u={toc:p},s="wrapper";function d(e){let{components:t,...r}=e;return(0,a.kt)(s,(0,n.Z)({},u,r,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("p",null,"PepperBot \u96c6\u6210\u4e86",(0,a.kt)("inlineCode",{parentName:"p"},"apscheduler"),"\uff0c\u53ef\u4ee5\u975e\u5e38\u8f7b\u677e\u7684\u5b9e\u73b0\u5f02\u6b65\u5b9a\u65f6\u4efb\u52a1(\u540c\u6b65\u4efb\u52a1\u4e5f\u53ef\u4ee5)"),(0,a.kt)("p",null,"\u5f53\u7136\uff0c\u4f60\u4e5f\u53ef\u4ee5\u76f4\u63a5\u901a\u8fc7",(0,a.kt)("inlineCode",{parentName:"p"},"Sanic"),"\u7684",(0,a.kt)("inlineCode",{parentName:"p"},"add_task"),"\u6765\u5b9e\u73b0\u5b9a\u65f6\u4efb\u52a1"),(0,a.kt)("p",null,"\u5176\u5b9e\u5b9a\u65f6\u4efb\u52a1\u548c\u4e00\u6b21\u6027\u4efb\u52a1\u5f88\u76f8\u4f3c\uff0c\u533a\u522b\u5728\u4e8e"),(0,a.kt)("ul",null,(0,a.kt)("li",{parentName:"ul"},"\u5982\u679c\u76f4\u63a5\u901a\u8fc7 ",(0,a.kt)("inlineCode",{parentName:"li"},"asyncio.run()"),"\u8fd0\u884c\u4efb\u52a1\uff0c\u90a3\u4e48\u5c31\u53ea\u4f1a\u6267\u884c\u4e00\u6b21\uff0c\u4e5f\u5c31\u662f\u4e00\u6b21\u6027\u4efb\u52a1"),(0,a.kt)("li",{parentName:"ul"},"\u5982\u679c\u901a\u8fc7 ",(0,a.kt)("inlineCode",{parentName:"li"},"bot.run()"),"\uff0c\u5e76\u4e14\u5c06\u4efb\u52a1\u6ce8\u518c\u5230\u4e86 ",(0,a.kt)("inlineCode",{parentName:"li"},"async_scheduler")," \u4e2d\uff0c\u90a3\u4e48\u4ed6\u5c31\u662f\u4f1a\u591a\u6b21\u6267\u884c\u7684\u5b9a\u65f6\u4efb\u52a1\u4e86")),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-py"},'from pepperbot import async_scheduler\n\nasync def task():\n    print("Hello World")\n\nasync_scheduler.add_job(task, "interval", seconds=5)\n')),(0,a.kt)("p",null,(0,a.kt)("inlineCode",{parentName:"p"},"async_scheduler"),"\u5176\u5b9e\u5c31\u662f\u4e00\u4e2a\u5b9e\u4f8b\u5316\u7684\uff0c",(0,a.kt)("inlineCode",{parentName:"p"},"apscheduler")," \u7684 ",(0,a.kt)("inlineCode",{parentName:"p"},"AsyncScheduler"),"\uff0c\u6240\u4ee5\u5177\u4f53\u53c2\u6570\u89c1 ",(0,a.kt)("inlineCode",{parentName:"p"},"apscheduler")," \u7684","[\u6587\u6863]","\u5373\u53ef"),(0,a.kt)("p",null,"\u5177\u4f53\u4f8b\u5b50",(0,a.kt)("a",{parentName:"p",href:"../../examples/%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1"},"\u89c1\u6b64")))}d.isMDXComponent=!0}}]);