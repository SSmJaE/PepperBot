(window.webpackJsonp=window.webpackJsonp||[]).push([[11],{115:function(e,t,n){"use strict";n.d(t,"a",(function(){return d})),n.d(t,"b",(function(){return h}));var r=n(0),a=n.n(r);function c(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function b(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?i(Object(n),!0).forEach((function(t){c(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):i(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},c=Object.keys(e);for(r=0;r<c.length;r++)n=c[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var c=Object.getOwnPropertySymbols(e);for(r=0;r<c.length;r++)n=c[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var o=a.a.createContext({}),p=function(e){var t=a.a.useContext(o),n=t;return e&&(n="function"==typeof e?e(t):b(b({},t),e)),n},d=function(e){var t=p(e.components);return a.a.createElement(o.Provider,{value:t},e.children)},s={inlineCode:"code",wrapper:function(e){var t=e.children;return a.a.createElement(a.a.Fragment,{},t)}},u=a.a.forwardRef((function(e,t){var n=e.components,r=e.mdxType,c=e.originalType,i=e.parentName,o=l(e,["components","mdxType","originalType","parentName"]),d=p(n),u=r,h=d["".concat(i,".").concat(u)]||d[u]||s[u]||c;return n?a.a.createElement(h,b(b({ref:t},o),{},{components:n})):a.a.createElement(h,b({ref:t},o))}));function h(e,t){var n=arguments,r=t&&t.mdxType;if("string"==typeof e||r){var c=n.length,i=new Array(c);i[0]=u;var b={};for(var l in t)hasOwnProperty.call(t,l)&&(b[l]=t[l]);b.originalType=e,b.mdxType="string"==typeof e?e:r,i[1]=b;for(var o=2;o<c;o++)i[o]=n[o];return a.a.createElement.apply(null,i)}return a.a.createElement.apply(null,n)}u.displayName="MDXCreateElement"},143:function(e,t,n){"use strict";n.r(t),t.default="data:image/png;base64,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"},80:function(e,t,n){"use strict";n.r(t),n.d(t,"frontMatter",(function(){return i})),n.d(t,"metadata",(function(){return b})),n.d(t,"toc",(function(){return l})),n.d(t,"default",(function(){return p}));var r=n(3),a=n(7),c=(n(0),n(115)),i={},b={unversionedId:"\u4e8b\u4ef6/\u6d88\u606f\u94fe",id:"\u4e8b\u4ef6/\u6d88\u606f\u94fe",isDocsHomePage:!1,title:"\u6d88\u606f\u94fe",description:"\u6700\u540e\u4e00\u6b65",source:"@site/docs/\u4e8b\u4ef6/\u6d88\u606f\u94fe.md",slug:"/\u4e8b\u4ef6/\u6d88\u606f\u94fe",permalink:"/PepperBot/docs/\u4e8b\u4ef6/\u6d88\u606f\u94fe",editUrl:"https://github.com/SSmJaE/PepperBot/edit/master/docs/docs/\u4e8b\u4ef6/\u6d88\u606f\u94fe.md",version:"current",lastUpdatedBy:"EdIfiMr",lastUpdatedAt:1622217138,formattedLastUpdatedAt:"5/28/2021",sidebar:"\u6559\u7a0b",previous:{title:"\u4e8b\u4ef6\u53c2\u6570",permalink:"/PepperBot/docs/\u4e8b\u4ef6/\u4e8b\u4ef6\u53c2\u6570"},next:{title:"\u7fa4\u6d88\u606f\u54cd\u5e94",permalink:"/PepperBot/docs/\u4e8b\u4ef6/\u7fa4\u6d88\u606f\u54cd\u5e94"}},l=[{value:"\u6700\u540e\u4e00\u6b65",id:"\u6700\u540e\u4e00\u6b65",children:[]},{value:"\u4ec0\u4e48\u662f\u6d88\u606f\u94fe",id:"\u4ec0\u4e48\u662f\u6d88\u606f\u94fe",children:[]},{value:"\u4e3a\u4ec0\u4e48\u79f0\u4e3a\u94fe",id:"\u4e3a\u4ec0\u4e48\u79f0\u4e3a\u94fe",children:[]},{value:"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5",id:"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5",children:[]},{value:"\u63a5\u53d7\u5230\u7684\u6d88\u606f\u94fe",id:"\u63a5\u53d7\u5230\u7684\u6d88\u606f\u94fe",children:[]},{value:"\u64cd\u4f5c\u6d88\u606f\u94fe",id:"\u64cd\u4f5c\u6d88\u606f\u94fe",children:[{value:"\u5b57\u7b26\u4e32\u53ef\u4ee5\u76f4\u63a5in",id:"\u5b57\u7b26\u4e32\u53ef\u4ee5\u76f4\u63a5in",children:[]},{value:"\u53ea\u53d6pure_text",id:"\u53ea\u53d6pure_text",children:[]},{value:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b",id:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b",children:[]},{value:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b\u7684\u5b9e\u4f8b",id:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b\u7684\u5b9e\u4f8b",children:[]},{value:"\u5feb\u6377\u65b9\u5f0f",id:"\u5feb\u6377\u65b9\u5f0f",children:[]},{value:"\u83b7\u53d6\u6240\u6709\u6307\u5b9a\u7c7b\u578b\u5b9e\u4f8b",id:"\u83b7\u53d6\u6240\u6709\u6307\u5b9a\u7c7b\u578b\u5b9e\u4f8b",children:[]},{value:"\u6309index\u53d6Segment",id:"\u6309index\u53d6segment",children:[]},{value:"\u53ef\u4ee5\u76f4\u63a5\u5224\u65ad\u5b9e\u4f8b",id:"\u53ef\u4ee5\u76f4\u63a5\u5224\u65ad\u5b9e\u4f8b",children:[]}]},{value:"\u624b\u52a8\u6784\u9020\u6d88\u606f\u94fe",id:"\u624b\u52a8\u6784\u9020\u6d88\u606f\u94fe",children:[{value:"\u76f4\u63a5\u4f20\u5165",id:"\u76f4\u63a5\u4f20\u5165",children:[]},{value:"\u51fd\u6570\u8fd4\u56de",id:"\u51fd\u6570\u8fd4\u56de",children:[]},{value:"\u5217\u8868\u89e3\u6784\uff0c*args",id:"\u5217\u8868\u89e3\u6784\uff0cargs",children:[]}]},{value:"\u6d88\u606f\u94fe\u4e0a\u7ed1\u5b9a\u7684\u65b9\u6cd5",id:"\u6d88\u606f\u94fe\u4e0a\u7ed1\u5b9a\u7684\u65b9\u6cd5",children:[]}],o={toc:l};function p(e){var t=e.components,i=Object(a.a)(e,["components"]);return Object(c.b)("wrapper",Object(r.a)({},o,i,{components:t,mdxType:"MDXLayout"}),Object(c.b)("h2",{id:"\u6700\u540e\u4e00\u6b65"},"\u6700\u540e\u4e00\u6b65"),Object(c.b)("p",null,"\u5728\u52a8\u624b\u5b9a\u4e49\u7fa4\u6d88\u606f\u4e8b\u4ef6\u54cd\u5e94\u4e4b\u524d\uff0c\u6211\u4eec\u6700\u540e\uff0c\u8fd8\u9700\u8981\u4e86\u89e3\u4e00\u4e0b\u6d88\u606f\u94fe\u7684\u6982\u5ff5"),Object(c.b)("h2",{id:"\u4ec0\u4e48\u662f\u6d88\u606f\u94fe"},"\u4ec0\u4e48\u662f\u6d88\u606f\u94fe"),Object(c.b)("p",null,"\u6d88\u606f\u7247\u6bb5"),Object(c.b)("h2",{id:"\u4e3a\u4ec0\u4e48\u79f0\u4e3a\u94fe"},"\u4e3a\u4ec0\u4e48\u79f0\u4e3a\u94fe"),Object(c.b)("p",null,"\u6d88\u606f\u94fe\u5c31\u662f\u6211\u4eec\u5b9e\u9645\u4e0a\u63a5\u53d7\u5230\u7684\u6d88\u606f\uff0c\u901a\u5e38\u53c8\u6709\u8868\u60c5\uff0c\u53c8\u6709\u6587\u5b57\uff0c\u6216\u8005\u53c8\u6709\u6587\u5b57\uff0c\u53c8\u6709\u56fe\u7247"),Object(c.b)("p",null,"\u7ec4\u6210\u6d88\u606f\u7684\u6bcf\u4e00\u4e2a\u5355\u5143\uff0c\u79f0\u4e3a\u4e00\u4e2a\u6d88\u606f\u7247\u6bb5"),Object(c.b)("p",null,"\u6bd4\u5982\u8fd9\u6837\u4e00\u6761\u6d88\u606f"),Object(c.b)("p",null,Object(c.b)("img",{src:n(143).default})),Object(c.b)("p",null,"\u5b9e\u9645\u4e0a\u7531\u4e09\u4e2a\u7247\u6bb5\u7ec4\u6210\uff0c\u5206\u522b\u662f\u6587\u5b57\u7247\u6bb5(Text)12345\uff0c\u8868\u60c5\u7247\u6bb5(Face)\u6ed1\u7a3d\uff0c\u6587\u5b57\u7247\u6bb567890"),Object(c.b)("h2",{id:"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5"},"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5"),Object(c.b)("p",null,"PepperBot\u7684\u6d88\u606f\u7c7b\u578b\u57fa\u672c\u7b26\u5408OneBot\u534f\u8bae\uff0c\u56e0\u4e3a\u4e3b\u8981\u540e\u7aef\u662fgo-cqhttp\uff0c\u6240\u4ee5\u4ee5go-cqhttp\u652f\u6301\u7684\u6709\u9650"),Object(c.b)("p",null,"\u53ef\u7528\u7684\u6d88\u606f\u7247\u6bb5\u53ef\u4ee5\u53c2\u8003",Object(c.b)("a",{parentName:"p",href:"https://github.com/SSmJaE/PepperBot/blob/master/pepperbot/message/segment.py"},"\u8fd9\u4e2a\u6587\u4ef6")),Object(c.b)("p",null,"go-cqhttp\u5bf9\u6d88\u606f\u7247\u6bb5\u7684\u652f\u6301\uff0c\u53ef\u89c1",Object(c.b)("a",{parentName:"p",href:"https://docs.go-cqhttp.org/cqcode/#qq-%E8%A1%A8%E6%83%85"},"\u6b64\u5904")),Object(c.b)("div",{className:"admonition admonition-info alert alert--info"},Object(c.b)("div",{parentName:"div",className:"admonition-heading"},Object(c.b)("h5",{parentName:"div"},Object(c.b)("span",{parentName:"h5",className:"admonition-icon"},Object(c.b)("svg",{parentName:"span",xmlns:"http://www.w3.org/2000/svg",width:"14",height:"16",viewBox:"0 0 14 16"},Object(c.b)("path",{parentName:"svg",fillRule:"evenodd",d:"M7 2.3c3.14 0 5.7 2.56 5.7 5.7s-2.56 5.7-5.7 5.7A5.71 5.71 0 0 1 1.3 8c0-3.14 2.56-5.7 5.7-5.7zM7 1C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7-3.14-7-7-7zm1 3H6v5h2V4zm0 6H6v2h2v-2z"}))),"info")),Object(c.b)("div",{parentName:"div",className:"admonition-content"},Object(c.b)("p",{parentName:"div"},"\u53d1\u9001\u8bed\u97f3\u548c\u89c6\u9891\uff0c\u9700\u8981\u5c06ffmpeg\u653e\u81f3go-cqhttp.exe\u540c\u76ee\u5f55\u4e0b\uff0c\u6216\u8005\u5c06ffmpeg\u7684\u53ef\u6267\u884c\u6587\u4ef6\u6dfb\u52a0\u81f3\u7cfb\u7edf\u53d8\u91cf"))),Object(c.b)("h2",{id:"\u63a5\u53d7\u5230\u7684\u6d88\u606f\u94fe"},"\u63a5\u53d7\u5230\u7684\u6d88\u606f\u94fe"),Object(c.b)("p",null,"\u5728\u63a5\u53d7\u5230\u7fa4\u6d88\u606f\u4e4b\u540e\uff0cPepperBot\u4f1a\u81ea\u52a8\u5c06\u63a5\u6536\u5230\u7684\u6d88\u606f\uff0c\u8f6c\u6362\u6210\u7b26\u5408PepperBot\u7684\u6d88\u606f\u94fe\uff0c\u5e76\u63d0\u4f9b\u4e86\u4e00\u5b9a\u7684\u5c5e\u6027\u548c\u65b9\u6cd5\uff0c\u4fbf\u4e8e\u64cd\u4f5c\u6d88\u606f\u94fe"),Object(c.b)("p",null,"\u7c7b\u578b\u4e3aMessageChain\u7684chain\u53c2\u6570\uff0c\u5373\u4e3a\u6d88\u606f\u94fe\nchain\u5b9e\u4f8b\u7684chain\u5c5e\u6027\uff0c\u5373chain.chain\uff0c\u5c31\u662f\u4e8b\u5b9e\u4e0a\u7684\u6d88\u606f\u94fe\uff0c\u4ed6\u662f\u4e00\u4e2a\u5217\u8868\uff0c\u5305\u542b\u6240\u6709\u6d88\u606f\u7247\u6bb5\uff0c\u53ef\u4ee5\u8fed\u4ee3"),Object(c.b)("p",null,"\u5f53\u7136\uff0c\u4e5f\u53ef\u4ee5\u76f4\u63a5\u8fed\u4ee3\u6307\u5b9a\u7c7b\u578b\u7684\u6d88\u606f\u7247\u6bb5\uff0c"),Object(c.b)("p",null,"\u6bd4\u5982\u8fed\u4ee3\u6240\u6709\u56fe\u7247\uff0c\u53ef\u4ee5\u76f4\u63a5 for image in chain.images\uff0c"),Object(c.b)("p",null,"\u8fed\u4ee3\u6240\u6709\u8868\u60c5\uff0cfor face in chain.faces"),Object(c.b)("p",null,"\u8bf8\u5982\u6b64\u7c7b"),Object(c.b)("p",null,"\u6587\u5b57\u6709\u6240\u4e0d\u540c\uff0c\u5e76\u6ca1\u6709\u63d0\u4f9bchain.text\u8fd9\u6837\u4e00\u4e2a\u5c5e\u6027\uff0c\u800c\u662f\u63d0\u4f9b\u4e86chain.pure_text,"),Object(c.b)("p",null,"\u8fd8\u662f",Object(c.b)("img",{src:n(143).default}),"\u8fd9\u4e2a\u4f8b\u5b50"),Object(c.b)("p",null,'chain.pure_text\u65e0\u89c6\u4e86\u4e24\u4e2a\u6587\u5b57\u7247\u6bb5\u4e2d\u95f4\u7684\u8868\u60c5\u7c7b\u578b\u7247\u6bb5\uff0c\u6700\u540e\u7ec4\u5408\u6210\u4e86\u4e00\u4e2a\u5b57\u7b26\u4e32\uff0c\u5b57\u7b26\u4e32\u7684\u503c\u4e3a"1234567890"'),Object(c.b)("p",null,"pure_text\u5728\u5224\u65ad\u6d88\u606f\u7684\u6587\u5b57\u5185\u5bb9\u662f\u6bd4\u8f83\u6709\u7528"),Object(c.b)("h2",{id:"\u64cd\u4f5c\u6d88\u606f\u94fe"},"\u64cd\u4f5c\u6d88\u606f\u94fe"),Object(c.b)("h3",{id:"\u5b57\u7b26\u4e32\u53ef\u4ee5\u76f4\u63a5in"},"\u5b57\u7b26\u4e32\u53ef\u4ee5\u76f4\u63a5in"),Object(c.b)("pre",null,Object(c.b)("code",{parentName:"pre",className:"language-py3"},'assert "word" in chain\n')),Object(c.b)("h3",{id:"\u53ea\u53d6pure_text"},"\u53ea\u53d6pure_text"),Object(c.b)("pre",null,Object(c.b)("code",{parentName:"pre",className:"language-py3"},'assert "123" not in chain\n')),Object(c.b)("h3",{id:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b"},"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b"),Object(c.b)("pre",null,Object(c.b)("code",{parentName:"pre",className:"language-py3"},"assert Text in chain\nassert chain.has(Text) == True\n")),Object(c.b)("h3",{id:"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b\u7684\u5b9e\u4f8b"},"\u53ef\u4ee5\u5224\u65ad\u662f\u5426\u6307\u5b9a\u7c7b\u578b\u7684\u5b9e\u4f8b"),Object(c.b)("pre",null,Object(c.b)("code",{parentName:"pre",className:"language-py3"},'assert Text("word2") not in chain\nassert Text("word word") in chain\nassert chain.has(Text("word word")) == True\nassert chain.has(Text("word word1")) == False\nassert chain.has(Face(123)) == True\nassert chain.has(Face(124)) == False\n')),Object(c.b)("h3",{id:"\u5feb\u6377\u65b9\u5f0f"},"\u5feb\u6377\u65b9\u5f0f"),Object(c.b)("pre",null,Object(c.b)("code",{parentName:"pre",className:"language-py3"},'assert chain.has_and_first(Text) == (True, Text("word word"))\nassert chain.has_and_last(Text) == (True, Text("word word2"))\nassert chain.has_and_all(Text) == (True, [Text("word word"), Text("word word2")])\n')),Object(c.b)("h3",{id:"\u83b7\u53d6\u6240\u6709\u6307\u5b9a\u7c7b\u578b\u5b9e\u4f8b"},"\u83b7\u53d6\u6240\u6709\u6307\u5b9a\u7c7b\u578b\u5b9e\u4f8b"),Object(c.b)("pre",null,Object(c.b)("code",{parentName:"pre",className:"language-py3"},'assert chain.faces == [Face(123)]\nassert chain.text == [Text("word word"), Text("word word2")]\n')),Object(c.b)("h3",{id:"\u6309index\u53d6segment"},"\u6309index\u53d6Segment"),Object(c.b)("pre",null,Object(c.b)("code",{parentName:"pre",className:"language-py3"},'assert chain[1] == Text("word word")\n')),Object(c.b)("h3",{id:"\u53ef\u4ee5\u76f4\u63a5\u5224\u65ad\u5b9e\u4f8b"},"\u53ef\u4ee5\u76f4\u63a5\u5224\u65ad\u5b9e\u4f8b"),Object(c.b)("pre",null,Object(c.b)("code",{parentName:"pre",className:"language-py3"},'assert Text("word word") == Text("word word")\nassert Text("word word") != Text("word word2")\n')),Object(c.b)("h2",{id:"\u624b\u52a8\u6784\u9020\u6d88\u606f\u94fe"},"\u624b\u52a8\u6784\u9020\u6d88\u606f\u94fe"),Object(c.b)("blockquote",null,Object(c.b)("p",{parentName:"blockquote"},"PepperBot\u63d0\u4f9b\u4e86\u975e\u5e38\u65b9\u4fbf\u7684\u6784\u9020\u6d88\u606f\u7247\u6bb5\uff0c\u4ee5\u53ca\u7ec4\u5408\u6d88\u606f\u94fe\u7684\u65b9\u5f0f")),Object(c.b)("h3",{id:"\u76f4\u63a5\u4f20\u5165"},"\u76f4\u63a5\u4f20\u5165"),Object(c.b)("h3",{id:"\u51fd\u6570\u8fd4\u56de"},"\u51fd\u6570\u8fd4\u56de"),Object(c.b)("h3",{id:"\u5217\u8868\u89e3\u6784\uff0cargs"},"\u5217\u8868\u89e3\u6784\uff0c*args"),Object(c.b)("h2",{id:"\u6d88\u606f\u94fe\u4e0a\u7ed1\u5b9a\u7684\u65b9\u6cd5"},"\u6d88\u606f\u94fe\u4e0a\u7ed1\u5b9a\u7684\u65b9\u6cd5"),Object(c.b)("p",null,"chain.reply"),Object(c.b)("p",null,"chain.withdraw()"))}p.isMDXComponent=!0}}]);