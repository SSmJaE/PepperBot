"use strict";(self.webpackChunkeoc=self.webpackChunkeoc||[]).push([[8170],{934:(e,n,t)=>{t.d(n,{r:()=>l});var a=t(2374);function l(e){let{messages:n}=e;return a.createElement("div",{style:{width:"100%",border:"2px solid black",borderRadius:8,fontSize:24,fontFamily:"\u534e\u6587\u65b0\u9b4f",margin:"16px 0px"}},n.map(((e,n)=>a.createElement("div",{key:n,style:{position:"relative",margin:"8px 0"}},a.createElement("div",{style:{display:"flex",flexDirection:"left"===e.position?"row":"row-reverse",alignItems:"center",gap:8,position:"relative",right:"right"===e.position?10:void 0,left:"left"===e.position?10:void 0}},a.createElement("div",null,e.sender),a.createElement("div",{style:{whiteSpace:"pre-wrap",border:"2px solid black",padding:"4px 8px",borderRadius:8}},e.message))))))}},2968:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>m,contentTitle:()=>o,default:()=>g,frontMatter:()=>p,metadata:()=>d,toc:()=>u});var a=t(3085),l=(t(2374),t(224)),r=t(934),i=t(6616);const s='from typing import Deque\n\nfrom pepperbot.core.message.chain import MessageChain\nfrom pepperbot.core.message.segment import Text\nfrom pepperbot.extensions.command import PatternArg, as_command\nfrom pepperbot.extensions.command.handle import CommandSender\nfrom pepperbot.store.command import HistoryItem\n\n\n@as_command(\n    need_prefix=True,\n    prefixes=["/", "#", "dan "],  # \u90fd\u662f\u6b63\u5219\uff0c\u81ea\u52a8\u52a0\u4e0a^\n    aliases=["\u67e5\u8be2", "\u6d4b\u8bd5"],  # \u90fd\u662f\u6b63\u5219\n    include_class_name=True,  # \u7c7b\u540d\u672c\u8eab\u4e0d\u4f5c\u4e3a\u6307\u4ee4\n    exit_patterns=["^/exit", "^\u9000\u51fa", "\u6211?\u9000\u51fa(\u5bf9\u8bdd)?"],  # \u90fd\u662f\u6b63\u5219\n    require_at=False,  # \u662f\u5426\u9700\u8981at\u673a\u5668\u4eba\n    timeout=30,  # \u4f1a\u8bdd\u8d85\u65f6\u65f6\u95f4\uff0c\u5355\u4f4d\u79d2\n)\nclass \u67e5\u8be2\u88c5\u5907:\n\n    # \u9ed8\u8ba4\u7684initial\uff0c\u201c\u5f00\u542f\u6307\u4ee4\u201c\u67e5\u8be2\u88c5\u5907\u201d\u7684\u4f1a\u8bdd\u201d\n    async def initial(self, sender: CommandSender):\n        await sender.send_message(\n            Text("\u5f00\u59cb\u6267\u884c\u6307\u4ee4\\n"),\n            Text("\u8bf7\u6309\u7167 \u6e38\u620f\u540d \u4eba\u7269\u5e8f\u53f7 \u7684\u683c\u5f0f\u8f93\u5165\\n"),\n        )\n\n        return self.choose_game\n\n    async def choose_game(\n        self,\n        sender: CommandSender,\n        game: str = PatternArg(),\n        npc: int = PatternArg(),\n    ):\n        await sender.send_message(Text(f"\u4f60\u9009\u62e9\u7684\u662f {game} \u7684 {npc}\uff0c\u9700\u8981\u67e5\u8be2\u4ed6\u7684\u4ec0\u4e48\u88c5\u5907\u5462\uff1f\u7a00\u6709\u5ea6\u4e3a\u4f55\uff1f"))\n\n        return self.choose_kind\n\n    async def choose_kind(\n        self,\n        sender: CommandSender,\n        kind: str = PatternArg(),\n        rarity: int = PatternArg(),\n    ):\n        results = [\n            "\u5927\u5251",\n            "\u64cd\u866b\u68cd",\n            "\u53cc\u624b\u5251",\n            "\u592a\u5200",\n        ]\n\n        await sender.send_message(\n            Text(f"\u67e5\u8be2\u5230\u4ee5\u4e0b\u88c5\u5907\\n"),\n            *[Text(f"- {result}\\n") for result in results],\n            Text("\\n\u662f\u5426\u7ee7\u7eed\u67e5\u8be2\uff1f\u56de\u590d\u201c\u7ee7\u7eed\u201d\u4ee5\u7ee7\u7eed"),\n        )\n\n        return self.whether_continue\n\n    async def whether_continue(self, sender: CommandSender, chain: MessageChain):\n        if "\u7ee7\u7eed" in chain:\n            await sender.send_message(Text("\u8bf7\u6309\u7167 \u6e38\u620f\u540d \u4eba\u7269\u5e8f\u53f7 \u7684\u683c\u5f0f\u8f93\u5165\\n"))\n            return self.choose_game\n\n        else:\n            # \u663e\u5f0freturn None\uff0c\u6216\u8005\u4e0dreturn\uff0c\u90fd\u4f1a\u7ed3\u675f\u4f1a\u8bdd\uff0c\u89e6\u53d1finish\u751f\u547d\u5468\u671f\n            return None\n\n    # \u7528\u6237\u4e3b\u52a8\u9000\u51fa\n    async def exit(self, sender: CommandSender):\n        await sender.send_message(Text(f"\u7528\u6237\u4e3b\u52a8\u9000\u51fa"))\n\n    # \u6d41\u7a0b\u6b63\u5e38\u9000\u51fa(\u5728\u4e2d\u95f4\u7684\u6d41\u7a0breturn False/None\u4e5f\u662f\u6b63\u5e38\u9000\u51fa)\n    async def finish(self, sender: CommandSender, history: Deque[HistoryItem]):\n        string = ""\n\n        for index, item in enumerate(history, start=1):\n            string += "----------\\n"\n            string += f"\u7b2c{index}\u6b21\u5bf9\u8bdd\\n"\n            string += f"\u7528\u6237\u8f93\u5165 : {item.chain.pure_text}\\n"\n            string += "\u89e3\u6790\u51fa\u5982\u4e0b\u53c2\u6570\\n"\n\n            # for argName, argValue in item.pattern:\n            #     reply("{argName} {argValue}")\n\n        await sender.send_message(Text("\u6307\u4ee4\u81ea\u7136\u9000\u51fa\uff0c\u5386\u53f2\u6210\u529f\u6d88\u606f\u5982\u4e0b\\n"), Text(string))\n\n    async def timeout(self, sender: CommandSender):\n        await sender.send_message(Text("\u7528\u6237\u8d85\u65f6\u672a\u56de\u590d\uff0c\u7ed3\u675f\u4f1a\u8bdd"))\n\n    async def catch(self, exception: Exception, sender: CommandSender):\n        await sender.send_message(\n            Text("\u6267\u884c\u8fc7\u7a0b\u4e2d\u672a\u6355\u83b7\u7684\u9519\u8bef\\n"),\n            Text(f"{exception}"),\n        )\n',p={},o=void 0,d={unversionedId:"\u6559\u7a0b/\u6307\u4ee4/\u58f0\u660e\u4e00\u4e2a\u6307\u4ee4",id:"\u6559\u7a0b/\u6307\u4ee4/\u58f0\u660e\u4e00\u4e2a\u6307\u4ee4",title:"\u58f0\u660e\u4e00\u4e2a\u6307\u4ee4",description:"\u4e00\u4e2a\u5c0f\u76ee\u6807",source:"@site/docs/\u6559\u7a0b/\u6307\u4ee4/\u58f0\u660e\u4e00\u4e2a\u6307\u4ee4.mdx",sourceDirName:"\u6559\u7a0b/\u6307\u4ee4",slug:"/\u6559\u7a0b/\u6307\u4ee4/\u58f0\u660e\u4e00\u4e2a\u6307\u4ee4",permalink:"/PepperBot/docs/\u6559\u7a0b/\u6307\u4ee4/\u58f0\u660e\u4e00\u4e2a\u6307\u4ee4",draft:!1,editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/\u6559\u7a0b/\u6307\u4ee4/\u58f0\u660e\u4e00\u4e2a\u6307\u4ee4.mdx",tags:[],version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1681060563,formattedLastUpdatedAt:"2023\u5e744\u67089\u65e5",frontMatter:{},sidebar:"\u6559\u7a0b",previous:{title:"\u6307\u4ee4\u7684\u751f\u547d\u5468\u671f",permalink:"/PepperBot/docs/\u6559\u7a0b/\u6307\u4ee4/\u6307\u4ee4\u7684\u751f\u547d\u5468\u671f"},next:{title:"\u4f7f\u7528\u6307\u4ee4",permalink:"/PepperBot/docs/\u6559\u7a0b/\u6307\u4ee4/\u4f7f\u7528\u6307\u4ee4"}},m={},u=[{value:"\u4e00\u4e2a\u5c0f\u76ee\u6807",id:"\u4e00\u4e2a\u5c0f\u76ee\u6807",level:2},{value:"\u89e6\u53d1\u6307\u4ee4",id:"\u89e6\u53d1\u6307\u4ee4",level:2},{value:"prefixes",id:"prefixes",level:3},{value:"include_class_name",id:"include_class_name",level:3},{value:"aliases",id:"aliases",level:3},{value:"require_at",id:"require_at",level:3},{value:"\u53ef\u9009\u7684 At \u89e6\u53d1",id:"\u53ef\u9009\u7684-at-\u89e6\u53d1",level:4},{value:"\u4ec5\u9700 At",id:"\u4ec5\u9700-at",level:4},{value:"\u6821\u9a8c\u53c2\u6570",id:"\u6821\u9a8c\u53c2\u6570",level:2},{value:"<code>initial</code>\u94a9\u5b50\u4e0e<code>PatternArg</code>",id:"initial\u94a9\u5b50\u4e0epatternarg",level:2},{value:"\u66f4\u65b0\u6307\u4ee4\u72b6\u6001(\u56de\u6eda)",id:"\u66f4\u65b0\u6307\u4ee4\u72b6\u6001\u56de\u6eda",level:2},{value:"\u6307\u4ee4\u8d85\u65f6/\u9000\u51fa",id:"\u6307\u4ee4\u8d85\u65f6\u9000\u51fa",level:2},{value:"\u5386\u53f2\u8bb0\u5f55\uff0chistory",id:"\u5386\u53f2\u8bb0\u5f55history",level:2},{value:"CommandSender",id:"commandsender",level:2},{value:"\u5b8c\u6574\u6307\u4ee4",id:"\u5b8c\u6574\u6307\u4ee4",level:2}],k={toc:u},c="wrapper";function g(e){let{components:n,...t}=e;return(0,l.kt)(c,(0,a.Z)({},k,t,{components:n,mdxType:"MDXLayout"}),(0,l.kt)("h2",{id:"\u4e00\u4e2a\u5c0f\u76ee\u6807"},"\u4e00\u4e2a\u5c0f\u76ee\u6807"),(0,l.kt)("p",null,"\u8fd9\u4e00\u7ae0\uff0c\u6211\u4eec\u7684\u6700\u7ec8\u76ee\u6807\uff0c\u662f\u5b9e\u73b0\u5982\u4e0b\u7684\u5bf9\u8bdd\u6548\u679c"),(0,l.kt)(r.r,{messages:[{position:"right",sender:"\u7528\u6237",message:"/\u67e5\u8be2\u88c5\u5907"},{position:"left",sender:"bot",message:"\u5f00\u59cb\u6267\u884c\u6307\u4ee4"},{position:"left",sender:"bot",message:"\u8bf7\u6309\u7167 \u6e38\u620f\u540d \u4eba\u7269\u5e8f\u53f7 \u7684\u683c\u5f0f\u8f93\u5165"},{position:"right",sender:"\u7528\u6237",message:"\u67d0\u6e38\u620f \u67d0\u4eba\u7269"},{position:"left",sender:"bot",message:"\u683c\u5f0f\u9519\u8bef\uff0c\u8bf7\u6309\u7167xxxxxx\u7684\u683c\u5f0f\uff0c\u8f93\u5165"},{position:"right",sender:"\u7528\u6237",message:"\u67d0\u6e38\u620f 9527"},{position:"left",sender:"bot",message:"\u4f60\u9009\u62e9\u7684\u662f \u67d0\u6e38\u620f \u7684 \u67d0\u4eba\u7269\uff0c\u9700\u8981\u67e5\u8be2\u4ed6\u7684\u4ec0\u4e48\u88c5\u5907\u5462\uff1f\u7a00\u6709\u5ea6\u4e3a\u4f55\uff1f"},{position:"right",sender:"\u7528\u6237",message:"\u6b66\u5668 5"},{position:"left",sender:"bot",message:"\u67e5\u8be2\u5230\u4ee5\u4e0b\u88c5\u5907"},{position:"left",sender:"bot",message:"- \u5927\u5251"},{position:"left",sender:"bot",message:"- \u64cd\u866b\u68cd"},{position:"left",sender:"bot",message:"- \u53cc\u624b\u5251"},{position:"left",sender:"bot",message:"- \u592a\u5200"},{position:"left",sender:"bot",message:"\u662f\u5426\u7ee7\u7eed\u67e5\u8be2\uff1f\u56de\u590d\u201c\u7ee7\u7eed\u201d\u4ee5\u7ee7\u7eed"},{position:"right",sender:"\u7528\u6237",message:"\u4e0d"},{position:"left",sender:"bot",message:"\u6307\u4ee4\u81ea\u7136\u9000\u51fa\uff0c\u5386\u53f2\u6210\u529f\u6d88\u606f\u5982\u4e0b\n----------\n\u7b2c1\u6b21\u5bf9\u8bdd\n\u7528\u6237\u8f93\u5165 : /\u67e5\u8be2\u88c5\u5907\n\u89e3\u6790\u51fa\u5982\u4e0b\u53c2\u6570\n----------\n\u7b2c2\u6b21\u5bf9\u8bdd\n\u7528\u6237\u8f93\u5165 : \u67d0\u6e38\u620f \u67d0\u4eba\u7269\n\u89e3\u6790\u51fa\u5982\u4e0b\u53c2\u6570\n<game : str> : \u67d0\u6e38\u620f\n<npc : str> : \u67d0\u4eba\u7269\n----------\n\u7b2c3\u6b21\u5bf9\u8bdd\n\u7528\u6237\u8f93\u5165 : \u67d0\u4eba\u7269 \u4f20\u8bf4\n\u89e3\u6790\u51fa\u5982\u4e0b\u53c2\u6570\n<kind : str> : \u6b66\u5668\n<clarity : int> : 5\n----------"}],mdxType:"Conversation"}),(0,l.kt)("p",null,"\u6211\u4eec\u6765\u62c6\u89e3\u4e00\u4e0b\uff0c\u5b9e\u73b0\u4e00\u4e2a\u8fd9\u6837\u7684\u6307\u4ee4\uff0c\u6211\u4eec\u9700\u8981\u6d89\u53ca\u54ea\u4e9b\u65b9\u9762"),(0,l.kt)("p",null,(0,l.kt)("inlineCode",{parentName:"p"},"as_command"),"\u5b8c\u6574\u53c2\u6570\u6587\u6863","[\u5728\u6b64]"),(0,l.kt)("h2",{id:"\u89e6\u53d1\u6307\u4ee4"},"\u89e6\u53d1\u6307\u4ee4"),(0,l.kt)("p",null,"\u60f3\u8981\u89e6\u53d1\u4e00\u4e2a\u6307\u4ee4\uff0c\u6211\u4eec\u9996\u5148\u8981\u80fd\u6ee1\u8db3\u6307\u4ee4\u7684\u5173\u952e\u5b57\u8bc6\u522b"),(0,l.kt)("p",null,"\u5e38\u89c1\u7684\u6307\u4ee4\u7531\u4ee5\u4e0b\u4e09\u4e2a\u90e8\u5206\u7ec4\u6210 \u524d\u7f00 + \u6307\u4ee4\u540d\u79f0 + \u53c2\u6570"),(0,l.kt)("p",null,'\u6bd4\u5982"/\u4eca\u65e5\u5934\u6761"\uff0c\u524d\u7f00\u4e3a\u201c/\u201d\uff0c\u6307\u4ee4\u540d\u79f0\u4e3a"\u4eca\u65e5\u5934\u6761"\uff0c\u6ca1\u6709\u53c2\u6570'),(0,l.kt)("p",null,"\u6bd4\u5982\u201c\u5929\u6c14 \u4e0a\u6d77\u201d\uff0c\u6ca1\u6709\u524d\u7f00\uff0c\u6216\u8005\u8bf4\u524d\u7f00\u4e3a\u7a7a\uff0c\u5373\u201c\u201d\uff0c\u6307\u4ee4\u540d\u79f0\u4e3a\u201c\u5929\u6c14\u201d\uff0c\u6709\u4e00\u4e2a\u53c2\u6570\uff0c\u201c\u4e0a\u6d77\u201d"),(0,l.kt)("h3",{id:"prefixes"},"prefixes"),(0,l.kt)("p",null,"\u901a\u8fc7",(0,l.kt)("inlineCode",{parentName:"p"},"as_command"),"\u4e2d\u7684",(0,l.kt)("inlineCode",{parentName:"p"},"prefixes"),"\u53c2\u6570\uff0c\u6211\u4eec\u53ef\u4ee5\u8bbe\u7f6e\u6307\u4ee4\u7684\u524d\u7f00\uff0c\u53ef\u4ee5\u8bbe\u7f6e\u591a\u4e2a\uff0c\u4e5f\u53ef\u4ee5\u4e00\u4e2a\u90fd\u4e0d\u8bbe\u7f6e"),(0,l.kt)("p",null,"\u6bd4\u5982\u6307\u4ee4\u201c\u4eca\u65e5\u5934\u6761\u201d\uff0c\u6211\u4eec\u8bbe\u7f6e",(0,l.kt)("inlineCode",{parentName:"p"},"prefixes"),"\u4e3a",'["/", "@", "#"]',"\uff0c\u5f53\u7528\u6237\u4f7f\u7528\u4efb\u610f\u4e00\u4e2a\u524d\u7f00\u65f6\uff0c\u90fd\u80fd\u89e6\u53d1\u8be5\u6307\u4ee4"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},'"/\u4eca\u65e5\u5934\u6761"\n"@\u4eca\u65e5\u5934\u6761"\n"#\u4eca\u65e5\u5934\u6761"\n')),(0,l.kt)("h3",{id:"include_class_name"},"include_class_name"),(0,l.kt)("p",null,"\u9ed8\u8ba4\u6765\u8bf4\uff0c\u6307\u4ee4\u7684\u7c7b\u540d\uff0c\u4e5f\u4f1a\u88ab\u89c6\u4f5c\u6307\u4ee4\u7684\u540d\u79f0\uff0c\u6bd4\u5982"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},"class \u5929\u6c14\u6307\u4ee4:\n    ...\n")),(0,l.kt)("p",null,"\u5047\u8bbe prefixes \u8bbe\u7f6e\u4e3a",'["/"]','\uff0c\u5f53\u7528\u6237\u8f93\u5165"/\u5929\u6c14\u6307\u4ee4"\u65f6\uff0c\u4f1a\u89e6\u53d1\u8be5\u6307\u4ee4'),(0,l.kt)("p",null,"\u8fd9\u4e00\u884c\u4e3a\u53ef\u4ee5\u8bbe\u7f6e include_class_name \u4e3a False \u5173\u95ed"),(0,l.kt)("h3",{id:"aliases"},"aliases"),(0,l.kt)("p",null,"\u6709\u65f6\u5019\uff0c\u60f3\u8981\u4e3a\u6307\u4ee4\u8bbe\u7f6e\u591a\u4e2a\u522b\u540d\uff0c\u53ef\u4ee5\u901a\u8fc7",(0,l.kt)("inlineCode",{parentName:"p"},"as_command"),"\u4e2d\u7684",(0,l.kt)("inlineCode",{parentName:"p"},"aliases"),"\u53c2\u6570\u5b9e\u73b0"),(0,l.kt)("p",null,"\u6bd4\u5982\u5929\u6c14\u6307\u4ee4\uff0c\u5f53\u8bbe\u7f6e",(0,l.kt)("inlineCode",{parentName:"p"},"aliases"),"\u4e3a",'["\u5929\u6c14", "\u6c14\u8c61", "\u98ce\u96e8"]',"\u65f6\uff0c\u7528\u6237\u8f93\u5165"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},'"\u5929\u6c14 \u4e0a\u6d77"\n"\u6c14\u8c61 \u5317\u4eac"\n"\u98ce\u96e8 \u6df1\u5733"\n')),(0,l.kt)("p",null,"\u90fd\u4f1a\u89e6\u53d1"),(0,l.kt)("p",null,"\u914d\u5408",(0,l.kt)("inlineCode",{parentName:"p"},"include_class_name"),"\u4f7f\u7528\uff0c\u53ef\u4ee5\u5b9e\u73b0\u975e\u5e38\u7075\u6d3b\u7684\u6548\u679c"),(0,l.kt)("h3",{id:"require_at"},"require_at"),(0,l.kt)("p",null,"\u5982\u679c\u4f60\u5e0c\u671b\u53ea\u6709\u5f53\u7fa4\u5458@\u4e86\u673a\u5668\u4eba\u65f6\uff0c\u624d\u80fd\u89e6\u53d1\u6307\u4ee4\uff0c\u53ef\u4ee5\u8bbe\u7f6e",(0,l.kt)("inlineCode",{parentName:"p"},"require_at"),"\u4e3a True"),(0,l.kt)("p",null,"\u6bd4\u5982\uff0c\u8bbe\u7f6e",(0,l.kt)("inlineCode",{parentName:"p"},"aliases"),"\u4e3a",(0,l.kt)("inlineCode",{parentName:"p"},'["\u5929\u6c14"]'),"\uff0c",(0,l.kt)("inlineCode",{parentName:"p"},"require_at"),"\u4e3a ",(0,l.kt)("inlineCode",{parentName:"p"},"True"),"\uff0c\u5f53\u7528\u6237\u8f93\u5165"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},"@bot \u5929\u6c14 \u4e0a\u6d77\n")),(0,l.kt)("p",null,"\u65f6\uff0c\u624d\u4f1a\u89e6\u53d1"),(0,l.kt)("h4",{id:"\u53ef\u9009\u7684-at-\u89e6\u53d1"},"\u53ef\u9009\u7684 At \u89e6\u53d1"),(0,l.kt)("p",null,"\u5982\u679c\u4f60\u5e0c\u671b\uff0c\u65e2\u53ef\u4ee5\u901a\u8fc7\u524d\u7f00\u89e6\u53d1\uff0c\u4e5f\u53ef\u4ee5\u901a\u8fc7@\u89e6\u53d1"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"\u901a\u8fc7\u524d\u7f00\u89e6\u53d1\uff0c\u4e0d\u9700\u8981@"),(0,l.kt)("li",{parentName:"ul"},"\u9700\u8981@\u7684\u89e6\u53d1")),(0,l.kt)("p",null,"\u53ef\u4ee5\u901a\u8fc7\u7ee7\u627f\u5b9e\u73b0"),(0,l.kt)("p",null,"\u53ef\u4ee5\u53d1\u73b0\uff0c",(0,l.kt)("inlineCode",{parentName:"p"},"PepperBot"),"\u4e2d\u7684\u6307\u4ee4\uff0c\u90fd\u662f\u901a\u8fc7",(0,l.kt)("inlineCode",{parentName:"p"},"as_command"),"\u88c5\u9970\u5668\u5b9e\u73b0\u7684"),(0,l.kt)("p",null,"\u800c",(0,l.kt)("inlineCode",{parentName:"p"},"as_command"),"\u88c5\u9970\u5668\u63a5\u53d7\u7684\uff0c\u662f\u4e00\u4e2a",(0,l.kt)("inlineCode",{parentName:"p"},"class")),(0,l.kt)("p",null,"\u6240\u4ee5\uff0c\u6211\u4eec\u53ef\u4ee5\u5c06\u6307\u4ee4\u5177\u4f53\u7684\u529f\u80fd\uff0c\u653e\u5230\u4e00\u4e2a",(0,l.kt)("inlineCode",{parentName:"p"},"class"),"\u4e2d\uff0c\u7136\u540e\u901a\u8fc7\u65b0\u5b9e\u73b0\u4e24\u4e2a",(0,l.kt)("inlineCode",{parentName:"p"},"class"),"\uff0c\u90fd\u7ee7\u627f\u8fd9\u4e2a",(0,l.kt)("inlineCode",{parentName:"p"},"class"),"\uff0c\u6765\u7ed1\u5b9a\u4e0d\u540c\u7684",(0,l.kt)("inlineCode",{parentName:"p"},"as_command"),"\u53c2\u6570"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},'class WeatherCommand:\n    async def initial(self):\n        ...\n\n@as_commond(\n    prefixes=["/"],\n    aliases=["\u5929\u6c14", "\u6c14\u8c61", "\u98ce\u96e8"],\n    include_class_name=False,\n)\nclass WeatherCommandWithPrefix(WeatherCommand):\n    pass\n\n@as_commond(\n    need_prefix=False,\n    # prefixes=[],\n    aliases=["\u5929\u6c14", "\u6c14\u8c61", "\u98ce\u96e8"],\n    include_class_name=False,\n    require_at=True,\n)\nclass WeatherCommandWithAt(WeatherCommand):\n    pass\n')),(0,l.kt)("p",null,"\u9700\u8981\u6ce8\u610f\u7684\u662f\uff0cclass \u7684\u540d\u79f0\uff0c\u4e0d\u80fd\u91cd\u590d\uff0c\u5426\u5219\u4f1a\u62a5\u9519"),(0,l.kt)("p",null,"\u6211\u4eec\u53ef\u4ee5\u901a\u8fc7",(0,l.kt)("inlineCode",{parentName:"p"},"as_command"),"\u7684",(0,l.kt)("inlineCode",{parentName:"p"},"aliases"),"\u548c",(0,l.kt)("inlineCode",{parentName:"p"},"include_class_name"),"\u53c2\u6570\uff0c\u6765\u5b9e\u73b0\u4e0d\u540c class \u4f7f\u7528\u76f8\u540c\u7684 prefix \u548c alias"),(0,l.kt)("h4",{id:"\u4ec5\u9700-at"},"\u4ec5\u9700 At"),(0,l.kt)("p",null,"\u5982\u679c\u4f60\u5e0c\u671b\u53ea\u8981@\u4e86\u673a\u5668\u4eba\uff0c\u5c31\u80fd\u89e6\u53d1\u6307\u4ee4\uff0c\u53ef\u4ee5\u8bbe\u7f6e",(0,l.kt)("inlineCode",{parentName:"p"},"require_at"),"\u4e3a True\uff0c\u540c\u65f6",(0,l.kt)("inlineCode",{parentName:"p"},"need_prefix"),"\u4e3a False"),(0,l.kt)("p",null,"\u7136\u540e\uff0c\u63d0\u4f9b\u4e00\u4e2a",(0,l.kt)("inlineCode",{parentName:"p"},"\u7a7a\u5b57\u7b26\u4e32"),"\uff0c\u4f5c\u4e3a alias \u5373\u53ef"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},'@as_commond(\n    need_prefix=False,\n    aliases=[""],\n    require_at=True,\n)\nclass WeatherCommandWithAt(WeatherCommand):\n    ...\n')),(0,l.kt)("p",null,"\u73b0\u5728\uff0c\u7528\u6237\u53ea\u8981@\u4e86\u673a\u5668\u4eba\uff0c\u5c31\u80fd\u89e6\u53d1\u6307\u4ee4\u4e86"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},"@bot\n")),(0,l.kt)("h2",{id:"\u6821\u9a8c\u53c2\u6570"},"\u6821\u9a8c\u53c2\u6570"),(0,l.kt)("p",null,"\u4ece\u4e0a\u65b9\u7684\u4f8b\u5b50\u53ef\u4ee5\u770b\u5230\uff0c\u6211\u4eec\u5b9e\u73b0\u4e86\u53c2\u6570\u6821\u9a8c\u7684\u529f\u80fd\uff0c\u53c2\u6570\u7684\u81ea\u52a8\u6821\u9a8c\u548c\u89e3\u6790\uff0c\u662f\u901a\u8fc7",(0,l.kt)("inlineCode",{parentName:"p"},"PatternArg"),"\u5b9e\u73b0\u7684"),(0,l.kt)("p",null,"\u53c2\u6570\u683c\u5f0f\u6709\u4e24\u70b9\u8981\u6c42"),(0,l.kt)("ul",null,(0,l.kt)("li",{parentName:"ul"},"\u53c2\u6570\u6570\u91cf\u8981\u548c\u5b9a\u4e49\u4e86\u7684",(0,l.kt)("inlineCode",{parentName:"li"},"PatternArg"),"\u6570\u91cf\u4e00\u81f4"),(0,l.kt)("li",{parentName:"ul"},"\u53c2\u6570\u7c7b\u578b\u8981\u548c\u5bf9\u5e94\u4f4d\u7f6e\u7684",(0,l.kt)("inlineCode",{parentName:"li"},"PatternArg"),"\u4e00\u81f4")),(0,l.kt)("p",null,"\u6bd4\u5982\u8fd9\u6837\u7684\u5b9a\u4e49"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},'async def choose_game(self, game: str = PatternArg(), sender: CommandSender, npc : int = PatternArg()):\n    sender.send_message(Text(f"\u4f60\u9009\u62e9\u7684\u662f {game} \u7684 {npc}\uff0c\u9700\u8981\u67e5\u8be2\u4ed6\u7684\u4ec0\u4e48\u88c5\u5907\u5462\uff1f\u7a00\u6709\u5ea6\u4e3a\u4f55\uff1f"))\n')),(0,l.kt)("p",null,"\u6211\u4eec\u5b9a\u4e49\u4e86\u4e24\u4e2a\u53c2\u6570\uff0c\u7b2c\u4e00\u4e2a\u53c2\u6570\u4e3a game\uff0c\u5b57\u7b26\u4e32\u7c7b\u578b\uff0c\u7b2c\u4e8c\u4e2a\u53c2\u6570\u4e3a npc\uff0c\u662f int \u7c7b\u578b"),(0,l.kt)("p",null,"\u53ef\u4ee5\u770b\u5230\uff0c\u6211\u4eec\u5728\u7edf\u8ba1\u53c2\u6570\u7684\u65f6\u5019\uff0c\u8df3\u8fc7\u4e86",(0,l.kt)("inlineCode",{parentName:"p"},"sender"),"\u8fd9\u6837\u7684\u4fdd\u7559\u53c2\u6570\uff0c\u53ea\u7edf\u8ba1\u4e86\u9ed8\u8ba4\u503c\u4e3a",(0,l.kt)("inlineCode",{parentName:"p"},"PatternArg()"),"\u7684\u53c2\u6570"),(0,l.kt)("p",null,"\u7528\u6237\u8f93\u5165\u53c2\u6570\u65f6\u7684\u987a\u5e8f\uff0c\u5e94\u8be5\u548c\u5b9a\u4e49\u7684\u987a\u5e8f\u4e00\u81f4\uff0c\u6bd4\u5982\uff0c\u7b2c\u4e00\u4e2a\u53c2\u6570\u56e0\u4e3a",(0,l.kt)("inlineCode",{parentName:"p"},"game"),"\uff0c\u7b2c\u4e8c\u4e2a\u53c2\u6570\u4e3a",(0,l.kt)("inlineCode",{parentName:"p"},"npc")),(0,l.kt)("p",null,"\u5982\u679c\u7528\u6237\u8f93\u5165\u7684\u53c2\u6570\u7684\u7c7b\u578b\uff0c\u4e0e\u6211\u4eec\u5b9a\u4e49\u7684\u4e0d\u4e00\u81f4\uff0c\u6bd4\u5982"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},'"\u67d0\u6e38\u620f \u67d0\u4eba\u7269"\n')),(0,l.kt)("p",null,'\u8fd9\u91cc\uff0cnpc \u5e94\u8be5\u4e3a int \u7c7b\u578b\uff0c\u800c\u6211\u4eec\u63d0\u4f9b\u7684\u662f\u5b57\u7b26\u4e32"\u67d0\u4eba\u7269"\uff0c\u90a3\u4e48\uff0c\u5f53 PepperBot \u8bd5\u56fe\u5c06\u5b57\u7b26\u4e32"\u67d0\u4eba\u7269"\u8f6c\u6362\u4e3a int \u7c7b\u578b\u65f6\uff0c\u81ea\u7136\u4f1a\u5931\u8d25'),(0,l.kt)("p",null,"\u5728 PepperBot \u4e2d\uff0c\u5f53\u7528\u6237\u7684\u8f93\u5165\u4e0d\u7b26\u5408\u8981\u6c42\u65f6\uff0c\u4f1a\u81ea\u52a8\u53d1\u9001\u683c\u5f0f\u63d0\u793a\uff0c\u6bd4\u5982"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},'" <str : xxx>\n')),(0,l.kt)("h2",{id:"initial\u94a9\u5b50\u4e0epatternarg"},(0,l.kt)("inlineCode",{parentName:"h2"},"initial"),"\u94a9\u5b50\u4e0e",(0,l.kt)("inlineCode",{parentName:"h2"},"PatternArg")),(0,l.kt)("p",null,"\u4e8b\u5b9e\u4e0a\uff0c",(0,l.kt)("inlineCode",{parentName:"p"},"initial"),"\u94a9\u5b50\u4e5f\u53ef\u4ee5\u4f7f\u7528",(0,l.kt)("inlineCode",{parentName:"p"},"PatternArg"),"\uff0c\u8fd9\u6837\u7684\u8bdd\uff0c\u6211\u4eec\u5c31\u53ef\u4ee5\u76f4\u63a5\u4e00\u6b65\u89e3\u6790\u51fa\u53c2\u6570\uff0c\u53ef\u4ee5\u7701\u7565\u6389\u4e00\u6b21\u8be2\u95ee\u7684\u8fc7\u7a0b\uff0c\u524d\u63d0\u662f\uff0c\u9700\u8981\u7528\u6237\u5df2\u7ecf\u77e5\u9053\u8be5\u6307\u4ee4\u7684\u53c2\u6570\u8f93\u5165\u89c4\u5219"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},"")),(0,l.kt)("p",null,"\u5982\u679c\u6ca1\u80fd\u6ee1\u8db3\u8981\u6c42\uff0c\u4e5f\u5c31\u662f\u6ca1\u6709\u901a\u8fc7\u53c2\u6570\u6821\u9a8c\u8fd9\u4e00\u5173\uff0c\u90a3\u4e48\uff0c\u6307\u4ee4\u5e76\u6ca1\u6709\u5f00\u59cb\u4f1a\u8bdd\uff0c\u8be5\u6307\u4ee4\u5e76\u4e0d\u89c6\u4e3a\u6267\u884c\u72b6\u6001\uff0c\u81ea\u7136\uff0c",(0,l.kt)("inlineCode",{parentName:"p"},"history"),"\u4e2d\uff0c\u4e5f\u5c31\u6ca1\u6709\u8be5\u6b21\uff0c\u7528\u6237\u53d1\u9001\u7684\u6d88\u606f"),(0,l.kt)("p",null,"\u518d\u6b21\u5f3a\u8c03\uff0c\u53ea\u6709\u6210\u529f\u901a\u8fc7\u53c2\u6570\u6821\u9a8c\u7684",(0,l.kt)("inlineCode",{parentName:"p"},"handler"),"\uff0c\u7528\u6237\u53d1\u9001\u7684\u6d88\u606f\u624d\u4f1a\u88ab\u6ce8\u5165",(0,l.kt)("inlineCode",{parentName:"p"},"history"),"\uff0c\u8fd9\u6837\u5b9e\u73b0\uff0c\u662f\u4e3a\u4e86\u964d\u4f4e\u5fc3\u667a\u8d1f\u62c5\uff0c\u5373\uff0c\u51fa\u73b0\u5728",(0,l.kt)("inlineCode",{parentName:"p"},"history"),"\u4e2d\u7684\u6d88\u606f\uff0c\u90fd\u662f\u6ee1\u8db3\u8981\u6c42\u7684\uff0c\u548c\u6211\u4eec\u81ea\u5df1\u5b9a\u4e49\u7684\uff0c\u4e0d\u51fa\u9519\u65f6\uff0c\u903b\u8f91\u7684\u6267\u884c\u987a\u5e8f\u662f\u4e00\u81f4\u7684"),(0,l.kt)("h2",{id:"\u66f4\u65b0\u6307\u4ee4\u72b6\u6001\u56de\u6eda"},"\u66f4\u65b0\u6307\u4ee4\u72b6\u6001(\u56de\u6eda)"),(0,l.kt)("p",null,"\u6211\u4eec\u5b9a\u4e49\u4e86\u51e0\u4e2a\u9636\u6bb5\uff0c\u9996\u5148\uff0c \u9009\u62e9\u6e38\u620f\uff0c\u5176\u6b21\uff0c\u9009\u62e9\u88c5\u5907\uff0c\u90a3\u4e48\uff0c\u600e\u4e48\u5c06\u8fd9\u4e24\u4e2a",(0,l.kt)("inlineCode",{parentName:"p"},"\u65b9\u6cd5"),"\u94fe\u63a5\u8d77\u6765\u5462\uff1f"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},"def choose_game():\n    ...\n    return self.choose_kind\n\ndef choose_kind():\n    ...\n    return self.whether_continue\n")),(0,l.kt)("p",null,"\u901a\u8fc7",(0,l.kt)("inlineCode",{parentName:"p"},"\u65b9\u6cd5"),"\u7684\u8fd4\u56de\u503c\uff0c\u8fd4\u56de\u4e0b\u4e00\u6b65\u8981\u6267\u884c\u7684\u51fd\u6570"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},"\ndef choose_game():\n    return self.choose_kind\n\n")),(0,l.kt)("admonition",{type:"warning"},(0,l.kt)("p",{parentName:"admonition"},"\u6ce8\u610f\uff0c\u8fd4\u56de\u51fd\u6570\u5bf9\u8c61"),(0,l.kt)("pre",{parentName:"admonition"},(0,l.kt)("code",{parentName:"pre",className:"language-py"},"return self.function_name\n")),(0,l.kt)("p",{parentName:"admonition"},"\u800c\u4e0d\u662f\u8fd4\u56de\u51fd\u6570\u8c03\u7528"),(0,l.kt)("pre",{parentName:"admonition"},(0,l.kt)("code",{parentName:"pre",className:"language-py"},"return self.function_call()\n"))),(0,l.kt)("p",null,"\u4e0d\u4f46\u53ef\u4ee5\u5411\u4e0b\u8df3\u8f6c\uff0c\u8fd8\u53ef\u4ee5\u5411\u4e0a\u8df3\u8f6c"),(0,l.kt)("p",null,"\u5728\u8be5\u793a\u4f8b\u4e2d\uff0c\u6211\u4eec\u5b9e\u73b0\u4e86\u7ee7\u7eed\u67e5\u8be2\uff0c\u8df3\u8f6c\u56de\u4e0a\u4e00\u6b65"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},'def whether_continue():\n    if "\u7ee7\u7eed" in chain:\n        return self.choose_game\n\n')),(0,l.kt)("p",null,"\u5982\u679c\u6ca1\u6709 return \u8bed\u53e5\uff0c\u6216\u8005 return None\uff0c\u90a3\u4e48\uff0c\u4f1a\u89e6\u53d1 finish \u94a9\u5b50"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},"def func():\n    ...\n    # no return\n\ndef func():\n    return\n    # implicit return None\u9690\u5f0f\u8fd4\u56deNone\n\ndef func():\n    return None\n\ndef func():\n    return self.finish\n")),(0,l.kt)("p",null,"\u8fd9\u56db\u79cd\u90fd\u7b49\u4ef7\n\u81ea\u7136\u9000\u51fa"),(0,l.kt)("h2",{id:"\u6307\u4ee4\u8d85\u65f6\u9000\u51fa"},"\u6307\u4ee4\u8d85\u65f6/\u9000\u51fa"),(0,l.kt)("p",null,"\u901a\u8fc7\u5b9a\u4e49",(0,l.kt)("inlineCode",{parentName:"p"},"exit_patterns"),"\uff0c"),(0,l.kt)("p",null,"\u90fd\u662f\u6b63\u5219\u8868\u8fbe\u5f0f\uff0c\u548c",(0,l.kt)("inlineCode",{parentName:"p"},"prefixes"),"\u6709\u70b9\u50cf"),(0,l.kt)("p",null,"\u6ee1\u8db3",(0,l.kt)("inlineCode",{parentName:"p"},"exit_patterns"),"\u800c\u9000\u51fa\uff0c\u662f\u7528\u6237\u4e3b\u52a8\u9000\u51fa\uff0c\u89e6\u53d1\u7684\u662f",(0,l.kt)("inlineCode",{parentName:"p"},"exit"),"\u94a9\u5b50"),(0,l.kt)("p",null,(0,l.kt)("inlineCode",{parentName:"p"},"exit"),"\u94a9\u5b50\uff0c\u65e0\u6cd5\u901a\u8fc7 return self.exit \u624b\u52a8\u89e6\u53d1"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},"\n\n")),(0,l.kt)("h2",{id:"\u5386\u53f2\u8bb0\u5f55history"},"\u5386\u53f2\u8bb0\u5f55\uff0chistory"),(0,l.kt)("p",null,"\u5982\u679c\u6709\u53c2\u6570\u89e3\u6790\uff0c\u53ea\u6709\u6210\u529f\u89e3\u6790\u4e86\u53c2\u6570\u7684\u7528\u6237\u8f93\u5165\uff0c\u4f1a\u88ab\u6536\u5f55"),(0,l.kt)("p",null,"\u53ef\u4ee5\u901a\u8fc7\u5728\u51fd\u6570\u7b7e\u540d\u4e2d\uff0c\u5b9a\u4e49",(0,l.kt)("inlineCode",{parentName:"p"},"history"),"\u53c2\u6570\uff0c\u6765\u83b7\u5f97"),(0,l.kt)("pre",null,(0,l.kt)("code",{parentName:"pre",className:"language-py"},"async def func(self, history):\n    for history_item in history:\n\n")),(0,l.kt)("h2",{id:"commandsender"},"CommandSender"),(0,l.kt)("p",null,"\u53ef\u4ee5\u53d1\u73b0\uff0c\u6211\u4eec\u5728\u6307\u4ee4\u4e2d\uff0c\u5e76\u6ca1\u6709\u4f7f\u7528 bot.group_message \u4e4b\u7c7b\u7684 api\uff0c\u800c\u662f sender.send_message"),(0,l.kt)("p",null,"\u90a3\u4e48\uff0c\u6211\u4eec\u4e3a\u4ec0\u4e48\u5f15\u5165 sender \u8fd9\u6837\u4e00\u4e2a\u65b0\u6982\u5ff5\u5462\uff1f"),(0,l.kt)("p",null,"sender\uff0c\u5176\u5b9e\u5c31\u662f\u4e2a\u5feb\u6377\u65b9\u5f0f\uff0c\u81ea\u52a8\u5411\u4e0d\u540c\u6d88\u606f\u6765\u6e90\u7684\u5bf9\u8c61\u53d1\u9001\u6d88\u606f\u7684\u5feb\u6377\u65b9\u5f0f"),(0,l.kt)("p",null,"\u56e0\u4e3a\u4f5c\u4e3a\u6307\u4ee4\u7684\u8bdd\uff0c\u4f60\u4e0d\u77e5\u9053\uff0c\u7528\u6237\u662f\u4ece\u79c1\u804a\u6d88\u606f\uff0c\u8fd8\u662f\u4ece\u7fa4\u6d88\u606f\u53d1\u9001\u7684"),(0,l.kt)("p",null,"\u65b0\u5f15\u5165 sender \u5bf9\u8c61\uff0c\u901a\u8fc7 sender.send_message\uff0c\u53ef\u4ee5\u81ea\u52a8\u5224\u65ad\uff0c\u4e0d\u9700\u8981\u624b\u52a8 bot.onebot \u4e4b\u7c7b\u4e86"),(0,l.kt)("p",null,"\u5f53\u7136\uff0c\u6211\u4eec\u5728\u6307\u4ee4\u4e2d\u4e5f\u662f\u53ef\u4ee5\u7ee7\u7eed\u4f7f\u7528 bot.xxx \u98ce\u683c\u7684 api \u7684\uff0c\u89c1",(0,l.kt)("inlineCode",{parentName:"p"},"arbitrary API")),(0,l.kt)("h2",{id:"\u5b8c\u6574\u6307\u4ee4"},"\u5b8c\u6574\u6307\u4ee4"),(0,l.kt)(i.Z,{className:"language-py",mdxType:"CodeBlock"},s))}g.isMDXComponent=!0}}]);