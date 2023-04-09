// @ts-check

// /** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
module.exports = {
    教程: [
        {
            type: "category",
            label: "概览",
            collapsed: false,
            items: [
                "教程/概览/动机",
                "教程/概览/关于",
                "教程/概览/架构",
                "教程/概览/如何使用本文档",
            ],
        },
        {
            type: "category",
            label: "环境搭建",
            collapsed: false,
            items: [
                {
                    type: "category",
                    label: "PepperBot配置",
                    collapsed: true,
                    items: [
                        "教程/环境/PepperBot安装",
                        "教程/环境/初始化项目",
                        "教程/环境/PepperBot对接",
                    ],
                },
                {
                    type: "category",
                    label: "协议配置",
                    collapsed: true,
                    items: [
                        "教程/环境/配置QQ",
                        "教程/环境/配置微信",
                        "教程/环境/配置Telegram",
                        "教程/环境/配置Discord",
                    ],
                },
            ],
        },
        {
            type: "category",
            label: "响应事件",
            collapsed: false,
            items: [
                "教程/事件/路由",
                "教程/事件/事件响应机制",
                "教程/事件/事件参数",
                "教程/事件/消息链",
                "教程/事件/消息片段",
                "教程/事件/群消息响应",
                "教程/事件/运行机器人",
                // "教程/事件/hooks",
                // "教程/事件/其它事件",
            ],
        },
        {
            type: "category",
            label: "主动行为",
            collapsed: false,
            items: [
                "教程/行为/调用API",
                // "教程/行为/跨平台API",
                "教程/行为/一次性任务",
                "教程/行为/定时任务",
                // "教程/行为/行为链",
                // "教程/行为/web调度",
            ],
        },
        {
            type: "category",
            label: "指令",
            collapsed: true,
            items: [
                "教程/指令/何时使用指令",
                "教程/指令/指令的生命周期",
                "教程/指令/声明一个指令",
                "教程/指令/使用指令",
                // "教程/指令/指令的状态",
                // "教程/指令/指令的权限管理",
                // "教程/指令/指令的作用范围",
                // "教程/指令/命令行式指令",
                // "教程/指令/发布指令至指令市场",
                // "教程/指令/安装并使用社区指令",
            ],
        },
        {
            type: "category",
            label: "进阶",
            collapsed: false,
            items: [
                "教程/进阶/直接操作Sanic",
                "教程/进阶/数据库",
                "教程/进阶/多进程",
                "教程/进阶/配置文件",
                "教程/进阶/日志",
                "教程/进阶/Linux下部署",
            ],
        },
        {
            type: "category",
            label: "市场",
            collapsed: true,
            items: [
                "教程/市场/什么是市场",
                "教程/市场/发布项目",
                "教程/市场/使用项目",
            ],
        },
        // {
        //     type: "category",
        //     label: "插件",
        //     collapsed: false,
        //     items: [],
        // },
        // {
        //     type: "category",
        //     label: "部署",
        //     collapsed: false,
        //     items: [],
        // },
    ],
    示例: ["示例/概览", "示例/定时任务", "示例/消息转发", "示例/课程表"],
    事件一览: [
        "API/事件参数/概览",
        "API/事件参数/跨平台",
        "API/事件参数/Onebot",
        "API/事件参数/可爱猫",
        "API/事件参数/Telegram",
    ],
    API: [
        "API/概览",
        {
            type: "category",
            label: "Arbitrary API",
            collapsed: false,
            items: [
                "API/Arbitrary API/Onebot",
                "API/Arbitrary API/可爱猫",
                "API/Arbitrary API/Telegram",
            ],
        },
        {
            type: "category",
            label: "区分模式 API",
            collapsed: false,
            items: [
                {
                    type: "category",
                    label: "群",
                    collapsed: false,
                    items: [
                        "API/区分模式 API/群/跨平台",
                        "API/区分模式 API/群/Onebot",
                        "API/区分模式 API/群/可爱猫",
                        "API/区分模式 API/群/Telegram",
                    ],
                },
                {
                    type: "category",
                    label: "私聊",
                    collapsed: false,
                    items: [
                        "API/区分模式 API/私聊/跨平台",
                        "API/区分模式 API/私聊/Onebot",
                        "API/区分模式 API/私聊/可爱猫",
                        "API/区分模式 API/私聊/Telegram",
                    ],
                },
            ],
        },
    ],
    贡献指南: ["贡献/概览"],
};
