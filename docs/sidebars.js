module.exports = {
    教程: [
        {
            type: "category",
            label: "概览",
            collapsed: false,
            items: [
                "概览/动机",
                "概览/关于",
                {
                    type: "category",
                    label: "安装",
                    collapsed: false,
                    items: ["概览/配置go-cqhttp", "概览/配置pepperbot"],
                },
                "概览/如何使用本文档",
            ],
        },
        {
            type: "category",
            label: "响应事件",
            collapsed: false,
            items: [
                "事件/事件响应",
                "事件/生命周期",
                "事件/事件参数",
                "事件/消息链",
                "事件/群消息响应",
                "事件/示例",
            ],
        },
        {
            type: "category",
            label: "指令",
            collapsed: false,
            items: [
                "指令/何时使用指令",
                "指令/声明一个指令",
                "指令/使用指令",
                "指令/指令的上下文",
                "指令/指令的作用范围",
                "指令/CLI式指令",
            ],
        },
        {
            type: "category",
            label: "主动行为",
            collapsed: false,
            items: [
                "行为/行为链",
                "行为/一次性任务",
                "行为/定时任务",
                "行为/web调度",
                {
                    type: "category",
                    label: "各种操作实例",
                    collapsed: true,
                    items: ["行为/群文件", "行为/成员管理"],
                },
            ],
        },
        {
            type: "category",
            label: "插件",
            collapsed: false,
            items: [],
        },
        {
            type: "category",
            label: "部署",
            collapsed: false,
            items: ["部署/两套配置文件", "部署/日志", "部署/linux下部署"],
        },
    ],
    实战: [],
    API: [],
};
