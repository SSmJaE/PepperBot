"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[5298],{224:(n,e,t)=>{t.d(e,{Zo:()=>m,kt:()=>f});var r=t(2374);function a(n,e,t){return e in n?Object.defineProperty(n,e,{value:t,enumerable:!0,configurable:!0,writable:!0}):n[e]=t,n}function o(n,e){var t=Object.keys(n);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(n);e&&(r=r.filter((function(e){return Object.getOwnPropertyDescriptor(n,e).enumerable}))),t.push.apply(t,r)}return t}function c(n){for(var e=1;e<arguments.length;e++){var t=null!=arguments[e]?arguments[e]:{};e%2?o(Object(t),!0).forEach((function(e){a(n,e,t[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(n,Object.getOwnPropertyDescriptors(t)):o(Object(t)).forEach((function(e){Object.defineProperty(n,e,Object.getOwnPropertyDescriptor(t,e))}))}return n}function s(n,e){if(null==n)return{};var t,r,a=function(n,e){if(null==n)return{};var t,r,a={},o=Object.keys(n);for(r=0;r<o.length;r++)t=o[r],e.indexOf(t)>=0||(a[t]=n[t]);return a}(n,e);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(n);for(r=0;r<o.length;r++)t=o[r],e.indexOf(t)>=0||Object.prototype.propertyIsEnumerable.call(n,t)&&(a[t]=n[t])}return a}var i=r.createContext({}),l=function(n){var e=r.useContext(i),t=e;return n&&(t="function"==typeof n?n(e):c(c({},e),n)),t},m=function(n){var e=l(n.components);return r.createElement(i.Provider,{value:e},n.children)},u="mdxType",p={inlineCode:"code",wrapper:function(n){var e=n.children;return r.createElement(r.Fragment,{},e)}},d=r.forwardRef((function(n,e){var t=n.components,a=n.mdxType,o=n.originalType,i=n.parentName,m=s(n,["components","mdxType","originalType","parentName"]),u=l(t),d=a,f=u["".concat(i,".").concat(d)]||u[d]||p[d]||o;return t?r.createElement(f,c(c({ref:e},m),{},{components:t})):r.createElement(f,c({ref:e},m))}));function f(n,e){var t=arguments,a=e&&e.mdxType;if("string"==typeof n||a){var o=t.length,c=new Array(o);c[0]=d;var s={};for(var i in e)hasOwnProperty.call(e,i)&&(s[i]=e[i]);s.originalType=n,s[u]="string"==typeof n?n:a,c[1]=s;for(var l=2;l<o;l++)c[l]=t[l];return r.createElement.apply(null,c)}return r.createElement.apply(null,t)}d.displayName="MDXCreateElement"},4011:(n,e,t)=>{t.r(e),t.d(e,{assets:()=>i,contentTitle:()=>c,default:()=>p,frontMatter:()=>o,metadata:()=>s,toc:()=>l});var r=t(3085),a=(t(2374),t(224));const o={},c=void 0,s={unversionedId:"tutorial/action/\u884c\u4e3a\u94fe",id:"tutorial/action/\u884c\u4e3a\u94fe",title:"\u884c\u4e3a\u94fe",description:"\u884c\u4e3a\u94fe\u5c1a\u672a\u5b9e\u73b0\uff0c\u8fd9\u91cc\u53ea\u662f\u5c55\u793a\u884c\u4e3a\u94fe\u53ef\u80fd\u7684\u6837\u5b50",source:"@site/docs/tutorial/action/\u884c\u4e3a\u94fe.md",sourceDirName:"tutorial/action",slug:"/tutorial/action/\u884c\u4e3a\u94fe",permalink:"/PepperBot/docs/tutorial/action/\u884c\u4e3a\u94fe",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/tutorial/action/\u884c\u4e3a\u94fe.md",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1682179822,formattedLastUpdatedAt:"2023\u5e744\u670822\u65e5",frontMatter:{}},i={},l=[],m={toc:l},u="wrapper";function p(n){let{components:e,...t}=n;return(0,a.kt)(u,(0,r.Z)({},m,t,{components:e,mdxType:"MDXLayout"}),(0,a.kt)("admonition",{type:"warning"},(0,a.kt)("p",{parentName:"admonition"},"\u884c\u4e3a\u94fe\u5c1a\u672a\u5b9e\u73b0\uff0c\u8fd9\u91cc\u53ea\u662f\u5c55\u793a\u884c\u4e3a\u94fe\u53ef\u80fd\u7684\u6837\u5b50")),(0,a.kt)("pre",null,(0,a.kt)("code",{parentName:"pre",className:"language-py"},'async def do_something():\n    await actionBot.selectGroup(1111).new_notice(\n        title="",\n        body=""\n    ).run()\n\n    await (\n        actionBot\n        .selectGroups(1111, 2222, 3333, 4444)\n        .send_message(Text("\u4e00\u6761\u8de8\u7fa4\u6d88\u606f"))\n        .sleep(5)\n        .send_message(Face(100))\n        .run()\n    )\n\n    # ? \u5f02\u5e38\u60c5\u51b5\n    # \u5982\u679c\u673a\u5668\u4eba\u4e0d\u5728\u8be5\u7fa4\u4e2d\uff0c\u4f1a\u62a5\u9519\uff0c\u53ef\u4ee5try except\n    await (\n        actionBot\n        .selectGroup(1111)\n        .catch()\n        .send_message(Text("\u4e00\u6761\u8de8\u7fa4\u6d88\u606f"))\n        .run()\n    )\n\n    # ? catchHandler\u7684\u58f0\u660e\n    # \u51fd\u6570\u662f\u4e00\u7b49\u5bf9\u8c61\u7684\u6982\u5ff5\n    # \u4e3a\u4ec0\u4e48\u4e0d\u5efa\u8bae\u4f7f\u7528\u533f\u540d\u51fd\u6570\uff1f\n    # \u4e0d\u6613\u7406\u89e3\uff0c\u6ca1\u6709\u7c7b\u578b\u63d0\u793a\uff0c\u4e0d\u53ef\u590d\u7528\n\n    # \u6839\u636ecatch\u6807\u8bb0\u8fdb\u884c\u5206\u5272\u7247\u6bb5\uff0c\u6355\u83b7\u6bcf\u4e00\u4e2a\u7247\u6bb5\n    # \u6bd4\u8f83\u957f\u7684\u884c\u4e3a\u94fe+catch\u7684try except\u7b49\u4ef7\u5b9e\u73b0\n    await (\n        actionBot\n        .selectGroups(1111, 2222, 3333, 4444)\n        .send_message(Text("4\u4e2a\u7fa4"))\n        .exclude(111)  # \u5220\u9664\u4e0d\u5b58\u5728\u7684\u7fa4\uff0c\u4e0d\u4f1a\u62a5\u9519\n        .send_message(Text("3\u4e2a\u7fa4"))\n        .catch(catchHandler)\n        .exclude(222)\n        .send_message(Text("2\u4e2a\u7fa4"))\n        .exclude(333)\n        .send_message(Text("1\u4e2a\u7fa4"))\n        .run()\n    )\n\n    # ? \u590d\u6742\u9009\u62e9\u64cd\u4f5c\n    await (\n        actionBot\n        .selectGroups(1111, 2222, 3333, 4444)\n        .send_message(Text("4\u4e2a\u7fa4"))\n        .exclude(1111)  # \u5220\u9664\u4e0d\u5b58\u5728\u7684\u7fa4\uff0c\u4e0d\u4f1a\u62a5\u9519\n        .send_message(Text("3\u4e2a\u7fa4"))\n        .clear()\n        .send_message(Text("0\u4e2a\u7fa4\uff0c\u6b64\u65f6\u4f1a\u62a5\u9519\uff0c\u88abcatch\u62e6\u622a"))\n        .catch(catchHandler)\n        .include(5555)\n        .send_message(Text("1\u4e2a\u7fa4"))\n        .include(6666)\n        .send_message(Text("2\u4e2a\u7fa4"))\n        .run()\n    )\n\n    # ? \u590d\u7528\u9009\u62e9\u7ed3\u679c\n    \u4ea4\u6d41\u7fa4 = actionBot.selectGroup(1111)\n\n    # ? \u552f\u4e00\u6027\u6570\u636e\uff0c\u76f4\u63a5\u8fd4\u56de\n    \u4ea4\u6d41\u7fa4.admins()\n    \u4ea4\u6d41\u7fa4.info()\n\n    # ? \u51e1\u662f\u8981\u8fd4\u56de\u53ef\u8fed\u4ee3\u6570\u636e\u7684\uff0c\u5168\u90fd\u662f\u5f02\u6b65\u751f\u6210\u5668\n    \u4ea4\u6d41\u7fa4.files()\n\n    async for member in \u4ea4\u6d41\u7fa4.members():\n        nickname = member.nickname\n\n        if re.search("(\u7f51\u8bfe)|(\u4ee3\u5237)|(\u5de5\u4f5c\u5ba4)|(\u63a5\u5355)", nickname):\n            await member.kickout()\n\n    async for file in \u4ea4\u6d41\u7fa4.files():\n        print(file.name)\n\n    # ? \u4e0d\u8981\u8026\u5408\u53d1\u9001\u64cd\u4f5c(send_message)\u548c\u83b7\u53d6\u64cd\u4f5c(members)\n    #! \u4e0d\u8981\u8fd9\u6837\u505a\uff0c\u9519\u8bef\u793a\u4f8b\n    # todo \u8c03\u7528members\u7b49\u975erun end point\u65f6\uff0c\u4e5f\u5728\u5185\u90e8\u6267\u884c\u4e00\u6b21run\u6267\u884c\u7684\u65b9\u6cd5\uff0c\u4ee5\u9002\u914d\u8fd9\u79cd\u60c5\u51b5\n    getMembersAfterSendMessage = (\n        actionBot\n        .selectGroup(1111)\n        .send_message(Text("\u4e00\u6761\u8de8\u7fa4\u6d88\u606f"))\n        .members()\n    )\n\n    async for member in getMembersAfterSendMessage:\n        print(member.nickname)\n\n    # \u5206\u4e24\u6b21\uff0c\u4ee3\u7801\u66f4\u6613\u8bfb\uff0c\u6700\u4f73\u5b9e\u8df5\n    # \u53ef\u4ee5\u590d\u7528\u9009\u62e9\u7ed3\u679c\n    targetGroup = actionBot.selectGroup(1111)\n\n    # \u4e00\u4e2aaction\u53d1\u9001\u6d88\u606f\n    await targetGroup.send_message(Text("\u4e00\u6761\u8de8\u7fa4\u6d88\u606f")).run()\n\n    # \u4e00\u4e2aaction\u83b7\u53d6\u7fa4\u5458\n    getMembersIndependently = targetGroup.members()\n\n    async for member in getMembersIndependently:\n        print(member.nickname)\n\n    # ? \u5bf9\u6bcf\u4e2a\u7fa4\u6267\u884c\u540c\u6837\u7684\u64cd\u4f5c\uff0c\u901a\u8fc7each\u6216\u8005async_each\n    await (\n        actionBot\n        .selectGroups(1111, 2222, 3333, 4444)\n        .catch(catchHandler)\n        .each(eachGroup)\n        .async_each(eachGroup)\n        .run()\n    )\n\n    # ? members\uff0cinfo\uff0cfiles\u7b49\u83b7\u53d6\u65b9\u6cd5\u4e0a\uff0c\u5e76\u6ca1\u6709run\u65b9\u6cd5\n    # \u8fd9\u4e9b\u83b7\u53d6\u65b9\u6cd5\u548crun\u65b9\u6cd5\u4e00\u6837\uff0c\u90fd\u662f\u884c\u4e3a\u94fe\u7684end point\n    (\n        actionBot\n        .selectGroup(1111)\n        .members()\n        # .run() #! members\u662fend point\uff0c\u65e0\u6cd5\u518d\u8c03\u7528run\u65b9\u6cd5\n    )\n\n    # ? action\u5206\u652f\u9009\u62e9\n    targetUser = actionBot.selectUser(1111)\n\n    action1 = targetUser.send_message(Text("11"))\n    action2 = targetUser.send_message(Face(100))\n\n    finalAction = None\n\n    if "condition1":\n        finalAction = action1\n    else:\n        finalAction = action2\n\n    finalAction.run()\n\n    # ? \u6279\u91cf\u8fd0\u884caction\n\n    # \u53ef\u4ee5\u624b\u52a8\u8fd0\u884c\n    await targetUser.send_message(Text("11")).run()\n    await targetUser.send_message(Face(100)).run()\n\n    # \u4e5f\u53ef\u4ee5\u4f7f\u7528\u5de5\u5177\u51fd\u6570\n    action1 = targetUser.send_message(Text("11"))\n    action2 = targetUser.send_message(Face(100))\n\n    # \u53ea\u80fd\u63a5\u53d7runnable\u7684action\uff0c\u5373\u4e0d\u80fd\u662fmembers\uff0cinfo\u7b49\u4e3a\u7ec8\u70b9\u7684\u884c\u4e3a\u94fe\n    results = await ActionRunner.in_turn(action1, action2)\n    results = await ActionRunner.all(action1, action2)\n    results = await ActionRunner.all_settled(action1, action2)\n\n\nif __name__ == "__main__":\n    asyncio.run(do_something())\n\n')))}p.isMDXComponent=!0}}]);