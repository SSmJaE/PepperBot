/** @type {import('@docusaurus/types').DocusaurusConfig} */
module.exports = {
    title: "PepperBot Docs",
    tagline: "PepperBot的文档",
    url: "https://github.com/SSmJaE",
    baseUrl: "/PepperBot/",
    onBrokenLinks: "throw",
    onBrokenMarkdownLinks: "warn",
    favicon: "img/favicon.ico",
    organizationName: "SSmJaE", // Usually your GitHub org/user name.
    projectName: "PepperBot", // Usually your repo name.
    themeConfig: {
        navbar: {
            title: "PepperBot",
            logo: {
                alt: "My Site Logo",
                src: "img/logo.svg",
            },
            items: [
                {
                    to: "docs/概览/",
                    label: "教程",
                    position: "left",
                },
                {
                    to: "docs/实战/",
                    label: "实战",
                    position: "left",
                },
                {
                    to: "docs/API/",
                    label: "示例",
                    position: "left",
                },
                {
                    to: "docs/API/",
                    label: "API",
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
                    label: " ",
                    position: "right",
                    className: "header-github-link",
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
    },
    presets: [
        [
            "@docusaurus/preset-classic",
            {
                docs: {
                    sidebarPath: require.resolve("./sidebars.js"),
                    // Please change this to your repo.
                    editUrl: "https://github.com/SSmJaE/PepperBot/edit/master/docs/",
                    showLastUpdateAuthor: true,
                    showLastUpdateTime: true,
                },
                // blog: {
                //     showReadingTime: true,
                //     // Please change this to your repo.
                //     editUrl: "https://github.com/facebook/docusaurus/edit/master/website/blog/",
                // },
                theme: {
                    customCss: require.resolve("./src/css/custom.css"),
                },
            },
        ],
    ],
};
