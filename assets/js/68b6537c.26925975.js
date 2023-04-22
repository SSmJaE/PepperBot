"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[2667],{224:(e,t,r)=>{r.d(t,{Zo:()=>d,kt:()=>f});var n=r(2374);function a(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function o(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function i(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?o(Object(r),!0).forEach((function(t){a(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):o(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function c(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},o=Object.keys(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(n=0;n<o.length;n++)r=o[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var l=n.createContext({}),p=function(e){var t=n.useContext(l),r=t;return e&&(r="function"==typeof e?e(t):i(i({},t),e)),r},d=function(e){var t=p(e.components);return n.createElement(l.Provider,{value:t},e.children)},u="mdxType",s={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},m=n.forwardRef((function(e,t){var r=e.components,a=e.mdxType,o=e.originalType,l=e.parentName,d=c(e,["components","mdxType","originalType","parentName"]),u=p(r),m=a,f=u["".concat(l,".").concat(m)]||u[m]||s[m]||o;return r?n.createElement(f,i(i({ref:t},d),{},{components:r})):n.createElement(f,i({ref:t},d))}));function f(e,t){var r=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=r.length,i=new Array(o);i[0]=m;var c={};for(var l in t)hasOwnProperty.call(t,l)&&(c[l]=t[l]);c.originalType=e,c[u]="string"==typeof e?e:a,i[1]=c;for(var p=2;p<o;p++)i[p]=r[p];return n.createElement.apply(null,i)}return n.createElement.apply(null,r)}m.displayName="MDXCreateElement"},6746:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>l,contentTitle:()=>i,default:()=>s,frontMatter:()=>o,metadata:()=>c,toc:()=>p});var n=r(3085),a=(r(2374),r(224));const o={title:"\u90e8\u7f72"},i=void 0,c={unversionedId:"tutorial/advance/deploy",id:"tutorial/advance/deploy",title:"\u90e8\u7f72",description:"\u8fd9\u91cc\u4ee5ubuntu 22.04\u4e3a\u4f8b\uff0c\u5176\u4ed6\u7248\u672c\u7684linux\u7cfb\u7edf\u4e5f\u7c7b\u4f3c",source:"@site/docs/tutorial/advance/deploy.md",sourceDirName:"tutorial/advance",slug:"/tutorial/advance/deploy",permalink:"/PepperBot/docs/tutorial/advance/deploy",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/tutorial/advance/deploy.md",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1682179822,formattedLastUpdatedAt:"2023\u5e744\u670822\u65e5",frontMatter:{title:"\u90e8\u7f72"},sidebar:"\u6559\u7a0b",previous:{title:"\u65e5\u5fd7",permalink:"/PepperBot/docs/tutorial/advance/log"},next:{title:"\u4ec0\u4e48\u662f\u5e02\u573a",permalink:"/PepperBot/docs/tutorial/market/overview"}},l={},p=[{value:"\u57fa\u4e8e<code>sanic</code>\u81ea\u5e26\u7684<code>worker manager</code>\u7684\u90e8\u7f72",id:"\u57fa\u4e8esanic\u81ea\u5e26\u7684worker-manager\u7684\u90e8\u7f72",level:2},{value:"\u57fa\u4e8e<code>docker</code>\u7684\u90e8\u7f72",id:"\u57fa\u4e8edocker\u7684\u90e8\u7f72",level:2}],d={toc:p},u="wrapper";function s(e){let{components:t,...r}=e;return(0,a.kt)(u,(0,n.Z)({},d,r,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("p",null,"\u8fd9\u91cc\u4ee5",(0,a.kt)("inlineCode",{parentName:"p"},"ubuntu 22.04"),"\u4e3a\u4f8b\uff0c\u5176\u4ed6\u7248\u672c\u7684linux\u7cfb\u7edf\u4e5f\u7c7b\u4f3c"),(0,a.kt)("h2",{id:"\u57fa\u4e8esanic\u81ea\u5e26\u7684worker-manager\u7684\u90e8\u7f72"},"\u57fa\u4e8e",(0,a.kt)("inlineCode",{parentName:"h2"},"sanic"),"\u81ea\u5e26\u7684",(0,a.kt)("inlineCode",{parentName:"h2"},"worker manager"),"\u7684\u90e8\u7f72"),(0,a.kt)("p",null,"\u76f4\u63a5\u8fd0\u884c",(0,a.kt)("inlineCode",{parentName:"p"},"python3 main.py"),"\u5373\u53ef\uff0c",(0,a.kt)("inlineCode",{parentName:"p"},"sanic"),"\u8d1f\u8d23\u4f59\u4e0b\u5de5\u4f5c"),(0,a.kt)("p",null,"\u5efa\u8bae\u8bbe\u7f6e",(0,a.kt)("inlineCode",{parentName:"p"},"debug"),"\u4e3a",(0,a.kt)("inlineCode",{parentName:"p"},"False"),"\uff0c\u4ee5\u63d0\u9ad8\u6027\u80fd"),(0,a.kt)("h2",{id:"\u57fa\u4e8edocker\u7684\u90e8\u7f72"},"\u57fa\u4e8e",(0,a.kt)("inlineCode",{parentName:"h2"},"docker"),"\u7684\u90e8\u7f72"))}s.isMDXComponent=!0}}]);