const iconPath = "/img/icon.png";

/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
    title: "PepperBot Docs",
    tagline: "PepperBot的文档",
    favicon: iconPath,

    url: "https://SSmJaE.github.io/",
    baseUrl: "/PepperBot/",

    organizationName: "SSmJaE", // Usually your GitHub org/user name.
    projectName: "PepperBot", // Usually your repo name.

    onBrokenLinks: "throw",
    onBrokenMarkdownLinks: "warn",

    // Even if you don't use internalization, you can use this field to set useful
    // metadata like html lang. For example, if your site is Chinese, you may want
    // to replace "en" with "zh-Hans".
    i18n: {
        defaultLocale: 'zh-Hans',
        locales: ['zh-Hans', 'en'],
    },

    themeConfig: {
        navbar: {
            title: "PepperBot",
            logo: {
                alt: "My Site Logo",
                src: iconPath,
            },
            items: [
                {
                    to: "docs/教程/",
                    label: "教程",
                    position: "left",
                },
                {
                    to: "docs/示例/",
                    label: "示例",
                    position: "left",
                },
                {
                    to: "docs/事件/",
                    label: "事件一览",
                    position: "left",
                },
                {
                    to: "docs/API/",
                    label: "API",
                    position: "left",
                },
                {
                    to: "/market/",
                    label: "市场",
                    position: "left",
                },
                {
                    to: "docs/参与开发/",
                    label: "参与开发",
                    position: "left",
                },
                // {
                //   to: 'docs/',
                //   activeBasePath: 'docs',
                //   label: 'Docs',
                //   position: 'left',
                // },
                // {to: 'blog', label: 'Blog', position: 'left'},
                {
                    href: "https://github.com/SSmJaE/PepperBot",
                    position: "right",
                    className: "header-github-link",
                    "aria-label": "GitHub repository",
                },
            ],
        },
        // footer: {
        //     style: "dark",
        //     // links: [
        //     //     {
        //     //         title: "Docs",
        //     //         items: [
        //     //             {
        //     //                 label: "Getting Started",
        //     //                 to: "docs/",
        //     //             },
        //     //         ],
        //     //     },
        //     //     {
        //     //         title: "Community",
        //     //         items: [
        //     //             {
        //     //                 label: "Stack Overflow",
        //     //                 href: "https://stackoverflow.com/questions/tagged/docusaurus",
        //     //             },
        //     //             {
        //     //                 label: "Discord",
        //     //                 href: "https://discordapp.com/invite/docusaurus",
        //     //             },
        //     //             {
        //     //                 label: "Twitter",
        //     //                 href: "https://twitter.com/docusaurus",
        //     //             },
        //     //         ],
        //     //     },
        //     //     {
        //     //         title: "More",
        //     //         items: [
        //     //             {
        //     //                 label: "Blog",
        //     //                 to: "blog",
        //     //             },
        //     //             {
        //     //                 label: "GitHub",
        //     //                 href: "https://github.com/facebook/docusaurus",
        //     //             },
        //     //         ],
        //     //     },
        //     // ],
        //     copyright: `Built with Docusaurus.`,
        // },
        prism: {
            theme: require("prism-react-renderer/themes/oceanicNext"),
            darkTheme: require("prism-react-renderer/themes/vsDark"),
        },
        algolia: {
            // The application ID provided by Algolia
            appId: "UEP361PJRS",

            // Public API key: it is safe to commit it
            apiKey: "9a05028bf5adffd680061446e2abb411",

            indexName: "pepperbot",

            // Optional: see doc section below
            contextualSearch: true,

            // Optional: Specify domains where the navigation should occur through window.location instead on history.push. Useful when our Algolia config crawls multiple documentation sites and we want to navigate with window.location.href to them.
            externalUrlRegex: "external\\.com|domain\\.com",

            // Optional: Algolia search parameters
            searchParameters: {},

            // Optional: path for search page that enabled by default (`false` to disable it)
            searchPagePath: "search",

            //... other Algolia params
        },
    },
    presets: [
        [
            // "@docusaurus/preset-classic",
            'classic',

            {
                docs: {
                    sidebarPath: require.resolve("./sidebars.js"),
                    // Please change this to your repo.
                    editUrl: "https://github.com/SSmJaE/PepperBot/edit/master/docs/",
                    showLastUpdateAuthor: true,
                    showLastUpdateTime: true,
                    // remarkPlugins: [[require("remark-admonitions"), { infima: false }]],
                },
                // blog: {
                //     showReadingTime: true,
                //     // Please change this to your repo.
                //     editUrl: "https://github.com/facebook/docusaurus/edit/master/website/blog/",
                // },
                theme: {
                    customCss: [
                        require.resolve("./src/css/custom.css"),
                        // require.resolve("remark-admonitions/styles/classic.css"),
                    ],
                },
            },
        ],
    ],
};
