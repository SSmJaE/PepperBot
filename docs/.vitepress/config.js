module.exports = {
    title: "PepperBot Docs",
    description: "Just playing around.",
    base: "/PepperBot/",

    themeConfig: {
        repo: "SSmJaE/PepperBot",
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
                        { text: "群机器人", link: "/Introduction/install" },
                        { text: "生命周期", link: "/Introduction/install" },
                        { text: "Bot", link: "/Introduction/install" },
                        { text: "Chain", link: "/Introduction/install" },
                        { text: "Sender", link: "/Introduction/install" },
                    ],
                },
                {
                    text: "主动行为",
                    children: [
                        { text: "成员管理", link: "/Introduction/install" },
                        { text: "定时任务", link: "/Introduction/install" },
                    ],
                },
                {
                    text: "插件",
                    children: [
                        { text: "定义插件", link: "/Introduction/install" },
                        { text: "发布插件", link: "/Introduction/install" },
                        { text: "install插件", link: "/Introduction/install" },
                    ],
                },
            ],
        },
    },
};
