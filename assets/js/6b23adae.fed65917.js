"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[4010],{224:(e,t,r)=>{r.d(t,{Zo:()=>s,kt:()=>k});var a=r(2374);function n(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function i(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,a)}return r}function p(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?i(Object(r),!0).forEach((function(t){n(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):i(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function m(e,t){if(null==e)return{};var r,a,n=function(e,t){if(null==e)return{};var r,a,n={},i=Object.keys(e);for(a=0;a<i.length;a++)r=i[a],t.indexOf(r)>=0||(n[r]=e[r]);return n}(e,t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(e);for(a=0;a<i.length;a++)r=i[a],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}var o=a.createContext({}),l=function(e){var t=a.useContext(o),r=t;return e&&(r="function"==typeof e?e(t):p(p({},t),e)),r},s=function(e){var t=l(e.components);return a.createElement(o.Provider,{value:t},e.children)},c="mdxType",d={inlineCode:"code",wrapper:function(e){var t=e.children;return a.createElement(a.Fragment,{},t)}},g=a.forwardRef((function(e,t){var r=e.components,n=e.mdxType,i=e.originalType,o=e.parentName,s=m(e,["components","mdxType","originalType","parentName"]),c=l(r),g=n,k=c["".concat(o,".").concat(g)]||c[g]||d[g]||i;return r?a.createElement(k,p(p({ref:t},s),{},{components:r})):a.createElement(k,p({ref:t},s))}));function k(e,t){var r=arguments,n=t&&t.mdxType;if("string"==typeof e||n){var i=r.length,p=new Array(i);p[0]=g;var m={};for(var o in t)hasOwnProperty.call(t,o)&&(m[o]=t[o]);m.originalType=e,m[c]="string"==typeof e?e:n,p[1]=m;for(var l=2;l<i;l++)p[l]=r[l];return a.createElement.apply(null,p)}return a.createElement.apply(null,r)}g.displayName="MDXCreateElement"},1899:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>o,contentTitle:()=>p,default:()=>d,frontMatter:()=>i,metadata:()=>m,toc:()=>l});var a=r(3085),n=(r(2374),r(224));const i={},p=void 0,m={unversionedId:"API/\u4e8b\u4ef6\u53c2\u6570/Telegram",id:"API/\u4e8b\u4ef6\u53c2\u6570/Telegram",title:"Telegram",description:"inline_query",source:"@site/docs/API/\u4e8b\u4ef6\u53c2\u6570/Telegram.md",sourceDirName:"API/\u4e8b\u4ef6\u53c2\u6570",slug:"/API/\u4e8b\u4ef6\u53c2\u6570/Telegram",permalink:"/PepperBot/docs/API/\u4e8b\u4ef6\u53c2\u6570/Telegram",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/API/\u4e8b\u4ef6\u53c2\u6570/Telegram.md",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1681060563,formattedLastUpdatedAt:"2023\u5e744\u67089\u65e5",frontMatter:{},sidebar:"\u4e8b\u4ef6\u4e00\u89c8",previous:{title:"\u53ef\u7231\u732b",permalink:"/PepperBot/docs/API/\u4e8b\u4ef6\u53c2\u6570/\u53ef\u7231\u732b"}},o={},l=[{value:"inline_query",id:"inline_query",level:2},{value:"callback_query",id:"callback_query",level:2},{value:"edited_message",id:"edited_message",level:2},{value:"private_message",id:"private_message",level:2},{value:"group_message",id:"group_message",level:2}],s={toc:l},c="wrapper";function d(e){let{components:t,...r}=e;return(0,n.kt)(c,(0,a.Z)({},s,r,{components:t,mdxType:"MDXLayout"}),(0,n.kt)("h2",{id:"inline_query"},"inline_query"),(0,n.kt)("table",null,(0,n.kt)("thead",{parentName:"table"},(0,n.kt)("tr",{parentName:"thead"},(0,n.kt)("th",{parentName:"tr",align:"center"},"\u53c2\u6570\u540d\u79f0"),(0,n.kt)("th",{parentName:"tr",align:"center"},"\u7c7b\u578b"))),(0,n.kt)("tbody",{parentName:"table"},(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"raw_event"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from typing import Dict"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"client"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.client import Client"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"inline_query"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.types.inline_mode.inline_query import InlineQuery"))))),(0,n.kt)("pre",null,(0,n.kt)("code",{parentName:"pre",className:"language-py"},"from typing import Dict\nfrom pyrogram.client import Client\nfrom pyrogram.types.inline_mode.inline_query import InlineQuery\n\n\nclass MyHandler:\n    async def inline_query(\n        raw_event: Dict,\n        client: Client,\n        inline_query: InlineQuery,\n    ):\n        pass\n")),(0,n.kt)("h2",{id:"callback_query"},"callback_query"),(0,n.kt)("table",null,(0,n.kt)("thead",{parentName:"table"},(0,n.kt)("tr",{parentName:"thead"},(0,n.kt)("th",{parentName:"tr",align:"center"},"\u53c2\u6570\u540d\u79f0"),(0,n.kt)("th",{parentName:"tr",align:"center"},"\u7c7b\u578b"))),(0,n.kt)("tbody",{parentName:"table"},(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"raw_event"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from typing import Dict"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"client"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.client import Client"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"callback_query"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery"))))),(0,n.kt)("pre",null,(0,n.kt)("code",{parentName:"pre",className:"language-py"},"from typing import Dict\nfrom pyrogram.client import Client\nfrom pyrogram.types.bots_and_keyboards.callback_query import CallbackQuery\n\n\nclass MyHandler:\n    async def callback_query(\n        raw_event: Dict,\n        client: Client,\n        callback_query: CallbackQuery,\n    ):\n        pass\n")),(0,n.kt)("h2",{id:"edited_message"},"edited_message"),(0,n.kt)("table",null,(0,n.kt)("thead",{parentName:"table"},(0,n.kt)("tr",{parentName:"thead"},(0,n.kt)("th",{parentName:"tr",align:"center"},"\u53c2\u6570\u540d\u79f0"),(0,n.kt)("th",{parentName:"tr",align:"center"},"\u7c7b\u578b"))),(0,n.kt)("tbody",{parentName:"table"},(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"raw_event"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from typing import Dict"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"client"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.client import Client"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"message"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.types.messages_and_media.message import Message"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"bot"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pepperbot.adapters.telegram.api import TelegramPrivateBot"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"chain"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pepperbot.core.message.chain import MessageChain"))))),(0,n.kt)("pre",null,(0,n.kt)("code",{parentName:"pre",className:"language-py"},"from typing import Dict\nfrom pyrogram.client import Client\nfrom pyrogram.types.messages_and_media.message import Message\nfrom pepperbot.adapters.telegram.api import TelegramPrivateBot\nfrom pepperbot.core.message.chain import MessageChain\n\n\nclass MyHandler:\n    async def edited_message(\n        raw_event: Dict,\n        client: Client,\n        message: Message,\n        bot: TelegramPrivateBot,\n        chain: MessageChain,\n    ):\n        pass\n")),(0,n.kt)("h2",{id:"private_message"},"private_message"),(0,n.kt)("table",null,(0,n.kt)("thead",{parentName:"table"},(0,n.kt)("tr",{parentName:"thead"},(0,n.kt)("th",{parentName:"tr",align:"center"},"\u53c2\u6570\u540d\u79f0"),(0,n.kt)("th",{parentName:"tr",align:"center"},"\u7c7b\u578b"))),(0,n.kt)("tbody",{parentName:"table"},(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"raw_event"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from typing import Dict"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"client"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.client import Client"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"message"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.types.messages_and_media.message import Message"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"bot"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pepperbot.adapters.telegram.api import TelegramPrivateBot"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"chain"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pepperbot.core.message.chain import MessageChain"))))),(0,n.kt)("pre",null,(0,n.kt)("code",{parentName:"pre",className:"language-py"},"from typing import Dict\nfrom pyrogram.client import Client\nfrom pyrogram.types.messages_and_media.message import Message\nfrom pepperbot.adapters.telegram.api import TelegramPrivateBot\nfrom pepperbot.core.message.chain import MessageChain\n\n\nclass MyHandler:\n    async def private_message(\n        raw_event: Dict,\n        client: Client,\n        message: Message,\n        bot: TelegramPrivateBot,\n        chain: MessageChain,\n    ):\n        pass\n")),(0,n.kt)("h2",{id:"group_message"},"group_message"),(0,n.kt)("table",null,(0,n.kt)("thead",{parentName:"table"},(0,n.kt)("tr",{parentName:"thead"},(0,n.kt)("th",{parentName:"tr",align:"center"},"\u53c2\u6570\u540d\u79f0"),(0,n.kt)("th",{parentName:"tr",align:"center"},"\u7c7b\u578b"))),(0,n.kt)("tbody",{parentName:"table"},(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"raw_event"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from typing import Dict"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"client"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.client import Client"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"message"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pyrogram.types.messages_and_media.message import Message"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"bot"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pepperbot.adapters.telegram.api import TelegramGroupBot"))),(0,n.kt)("tr",{parentName:"tbody"},(0,n.kt)("td",{parentName:"tr",align:"center"},"chain"),(0,n.kt)("td",{parentName:"tr",align:"center"},(0,n.kt)("inlineCode",{parentName:"td"},"from pepperbot.core.message.chain import MessageChain"))))),(0,n.kt)("pre",null,(0,n.kt)("code",{parentName:"pre",className:"language-py"},"from typing import Dict\nfrom pyrogram.client import Client\nfrom pyrogram.types.messages_and_media.message import Message\nfrom pepperbot.adapters.telegram.api import TelegramGroupBot\nfrom pepperbot.core.message.chain import MessageChain\n\n\nclass MyHandler:\n    async def group_message(\n        raw_event: Dict,\n        client: Client,\n        message: Message,\n        bot: TelegramGroupBot,\n        chain: MessageChain,\n    ):\n        pass\n")))}d.isMDXComponent=!0}}]);