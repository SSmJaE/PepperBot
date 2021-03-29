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
            { text: "Guide", link: "/", activeMatch: "^/$|^/guide/" },
            {
                text: "API",
                link: "/config/basics",
                activeMatch: "^/config/",
            },
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
                        { text: "群机器人", link: "/Event/notExist" },
                        { text: "生命周期", link: "/Event/notExist" },
                        { text: "Bot", link: "/Event/notExist" },
                        { text: "Chain", link: "/Event/notExist" },
                        { text: "Sender", link: "/Event/notExist" },
                    ],
                },
                {
                    text: "主动行为",
                    children: [
                        { text: "成员管理", link: "/Event/notExist" },
                        { text: "定时任务", link: "/Event/notExist" },
                    ],
                },
                {
                    text: "插件",
                    children: [
                        { text: "定义插件", link: "/Event/notExist" },
                        { text: "发布插件", link: "/Event/notExist" },
                        { text: "install插件", link: "/Event/notExist" },
                    ],
                },
            ],
        },
    },
};
