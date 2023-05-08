// @ts-check

// /** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
module.exports = {
    教程: [
        {
            type: "category",
            label: "概览",
            collapsed: false,
            items: [
                "tutorial/overview/motivation",
                "tutorial/overview/about",
                "tutorial/overview/instruction",
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
                        "tutorial/environment/install",
                        "tutorial/environment/initialize",
                        "tutorial/environment/adapt",
                    ],
                },
                {
                    type: "category",
                    label: "协议配置",
                    collapsed: true,
                    items: [
                        "tutorial/environment/qq",
                        "tutorial/environment/qq_guild",
                        "tutorial/environment/wechat",
                        "tutorial/environment/wechat_subscription",
                        "tutorial/environment/telegram",
                        "tutorial/environment/discord",
                        "tutorial/environment/kook",
                    ],
                },
            ],
        },
        {
            type: "category",
            label: "响应事件",
            collapsed: false,
            items: [
                "tutorial/event/route",
                "tutorial/event/mechanism",
                "tutorial/event/event_args",
                "tutorial/event/message_chain",
                "tutorial/event/message_segment",
                "tutorial/event/helloworld",
                // "教程/事件/hooks",
                // "教程/事件/其它事件",
            ],
        },
        {
            type: "category",
            label: "主动行为",
            collapsed: false,
            items: [
                "tutorial/action/call_api",
                // "教程/行为/跨平台API",
                "tutorial/action/disposable",
                "tutorial/action/crontab",
                // "教程/行为/行为链",
                // "教程/行为/web调度",
            ],
        },
        {
            type: "category",
            label: "指令",
            collapsed: true,
            items: [
                "tutorial/command/occasion",
                "tutorial/command/use",
                "tutorial/command/config",
                "tutorial/command/strategy",
                "tutorial/command/lifecycle",
                "tutorial/command/state",
                "tutorial/command/arguments",
                "tutorial/command/define",
                "tutorial/command/cli",
            ],
        },
        {
            type: "category",
            label: "进阶",
            collapsed: false,
            items: [
                "tutorial/advance/propagation",
                "tutorial/advance/available",
                "tutorial/advance/sanic",
                "tutorial/advance/database",
                "tutorial/advance/multi_process",
                "tutorial/advance/config",
                "tutorial/advance/log",
                "tutorial/advance/deploy",
            ],
        },
        {
            type: "category",
            label: "市场",
            collapsed: true,
            items: [
                "tutorial/market/overview",
                "tutorial/market/publish",
                "tutorial/market/use",
            ],
        },
    ],
    示例: ["examples/概览", "examples/定时任务", "examples/消息转发", "examples/课程表"],
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
    贡献指南: ["contribution/overview"],
};
