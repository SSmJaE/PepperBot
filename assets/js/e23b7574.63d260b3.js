"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[9909],{3909:(e,t,o)=>{o.r(t),o.d(t,{assets:()=>d,contentTitle:()=>c,default:()=>u,frontMatter:()=>s,metadata:()=>i,toc:()=>m});var r=o(3085),n=(o(2374),o(224)),p=o(6616);const a='from apscheduler.triggers.interval import IntervalTrigger\nfrom pepperbot import PepperBot\nfrom pepperbot.core.bot.universal import ArbitraryApi\nfrom pepperbot.core.message.segment import Text\nfrom pepperbot.extensions.scheduler import async_scheduler\n\nbot = PepperBot(\n    port=53521,\n    debug=True,\n)\n\nbot.register_adapter(\n    bot_protocol="onebot",\n    receive_protocol="websocket",\n    backend_protocol="http",\n    backend_host="127.0.0.1",\n    backend_port=5700,\n)\n# bot.register_adapter(\n#     bot_protocol="keaimao",\n#     receive_protocol="http",\n#     backend_protocol="http",\n#     backend_host="192.168.0.109",\n#     backend_port=8090,\n# )\n\napi = ArbitraryApi\n\n\nasync def main():\n    await api.onebot.group_message("1041902989", Text("\u5b9a\u65f6\u6d88\u606f\u6d4b\u8bd5"))\n\n\nasync_scheduler.add_job(main, IntervalTrigger(seconds=10))\n\nbot.run()\n',s={},c=void 0,i={unversionedId:"\u793a\u4f8b/\u5b9a\u65f6\u4efb\u52a1",id:"\u793a\u4f8b/\u5b9a\u65f6\u4efb\u52a1",title:"\u5b9a\u65f6\u4efb\u52a1",description:"",source:"@site/docs/\u793a\u4f8b/\u5b9a\u65f6\u4efb\u52a1.mdx",sourceDirName:"\u793a\u4f8b",slug:"/\u793a\u4f8b/\u5b9a\u65f6\u4efb\u52a1",permalink:"/PepperBot/docs/\u793a\u4f8b/\u5b9a\u65f6\u4efb\u52a1",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/\u793a\u4f8b/\u5b9a\u65f6\u4efb\u52a1.mdx",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1681060563,formattedLastUpdatedAt:"2023\u5e744\u67089\u65e5",frontMatter:{},sidebar:"\u793a\u4f8b",previous:{title:"\u6982\u89c8",permalink:"/PepperBot/docs/\u793a\u4f8b/"},next:{title:"\u6d88\u606f\u8f6c\u53d1",permalink:"/PepperBot/docs/\u793a\u4f8b/\u6d88\u606f\u8f6c\u53d1"}},d={},m=[],l={toc:m},b="wrapper";function u(e){let{components:t,...o}=e;return(0,n.kt)(b,(0,r.Z)({},l,o,{components:t,mdxType:"MDXLayout"}),(0,n.kt)(p.Z,{className:"language-py",mdxType:"CodeBlock"},a))}u.isMDXComponent=!0}}]);