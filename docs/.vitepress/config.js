module.exports = {
    title: "PepperBot Docs",
    description: "Just playing around.",
    base: "/PepperBot/",

    themeConfig: {
        repo: "SSmJaE/PepperBot",

        // if your docs are in a different repo from your main project:
        docsRepo: "SSmJaE/PepperBot",
        // if your docs are not at the root of the repo:
        docsDir: "docs",
        // if your docs are in a specific branch (defaults to 'master'):
        docsBranch: "master",
        // defaults to false, set to true to enable
        editLinks: true,
        // custom text for edit link. Defaults to "Edit this page"
        editLinkText: "帮助我们改进此页面",

        nav: [
            // 带get started按钮的首页，卡片式feature展示，vibora
            { text: "Guide", link: "/", activeMatch: "^/$|^/guide/" },
            {
                text: "API",
                link: "/config/basics",
                activeMatch: "^/config/",
            },
            // todo 搜索框
        ],

        sidebar: {
            "/": [
                {
                    text: "概览",
                    children: [
                        { text: "为什么要造轮子？", link: "/Introduction/motivation" },
                        { text: "相关概念", link: "/Introduction/about" },
                        { text: "安装", link: "/Introduction/install" },
                    ],
                },
                {
                    text: "响应事件",
                    children: [
                        { text: "消息链", link: "/Event/notExist" },
                        { text: "群消息机器人", link: "/Event/notExist" },
                        { text: "关键字参数的妙用", link: "/Event/kwargs" },
                        { text: "生命周期", link: "/Event/notExist" },
                        { text: "上下文", link: "/Event/notExist" },
                        { text: "类的混入", link: "/Event/notExist" },
                        { text: "Bot", link: "/Event/notExist" },
                        { text: "Chain", link: "/Event/notExist" },
                        { text: "Sender", link: "/Event/notExist" },
                    ],
                },
                {
                    text: "指令",
                    children: [
                        { text: "PepperBot中的指令", link: "/Command/introduction" },
                        { text: "指令的上下文", link: "/Command/introduction" },
                    ],
                },
                {
                    text: "主动行为",
                    children: [
                        { text: "行为链", link: "/Event/notExist" },
                        { text: "成员管理", link: "/Event/notExist" },
                        { text: "定时任务", link: "/Event/notExist" },
                        { text: "一次性任务", link: "/Event/notExist" },
                        { text: "群文件", link: "/Event/notExist" },
                        { text: "群公告", link: "/Event/notExist" },
                    ],
                },
                {
                    text: "插件",
                    children: [
                        { text: "定义插件", link: "/Event/notExist" },
                        { text: "发布插件", link: "/Event/notExist" },
                        { text: "安装插件", link: "/Event/notExist" },
                    ],
                },
                {
                    text: "部署",
                    children: [
                        { text: "两套配置文件", link: "/Event/notExist" },
                        { text: "日志", link: "/Event/notExist" },
                    ],
                },
            ],
        },
    },
};
