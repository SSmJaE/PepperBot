module.exports = {
    title: "PepperBot Docs",
    description: "Just playing around.",

    themeConfig: {
        nav: [
            { text: "Guide", link: "/", activeMatch: "^/$|^/guide/" },
            {
                text: "Api",
                link: "/config/basics",
                activeMatch: "^/config/",
            },
        ],

        sidebar: {
            "/": [
                {
                    text: "概览",
                    children: [{ text: "安装", link: "/概览/安装" }],
                },
                {
                    text: "响应事件",
                    children: [
                        { text: "群机器人", link: "/概览/安装" },
                        { text: "生命周期", link: "/概览/安装" },
                        { text: "Bot", link: "/概览/安装" },
                        { text: "Chain", link: "/概览/安装" },
                        { text: "Sender", link: "/概览/安装" },
                    ],
                },
                {
                    text: "主动行为",
                    children: [
                        { text: "成员管理", link: "/概览/安装" },
                        { text: "定时任务", link: "/概览/安装" },
                    ],
                },
                {
                    text: "插件",
                    children: [
                        { text: "定义插件", link: "/概览/安装" },
                        { text: "发布插件", link: "/概览/安装" },
                        { text: "安装插件", link: "/概览/安装" },
                    ],
                },
            ],
        },
    },
};
