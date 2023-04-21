import React from "react";
import clsx from "clsx";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import useBaseUrl from "@docusaurus/useBaseUrl";
import styles from "./styles.module.css";

const features = [
    {
        title: "易于使用",
        imageUrl: "img/undraw_docusaurus_mountain.svg",
        description: <>易于上手使用的事件响应机制，api符合语意</>,
    },
    // {
    //     title: "专注问题",
    //     imageUrl: "img/undraw_docusaurus_tree.svg",
    //     description: <>解放生产力，专注于真正能提高能力的练习上</>,
    // },
    // {
    //     title: "完全的类型提示",
    //     imageUrl: "img/undraw_docusaurus_react.svg",
    //     description: <>易于使用，符合直觉的api；cli；文档完善</>,
    // },
];

function Feature({ imageUrl, title, description }) {
    const imgUrl = useBaseUrl(imageUrl);
    return (
        <div className={clsx("col col--4 text--center", styles.feature)}>
            {imgUrl && (
                <div className="text--center">
                    <img className={styles.featureImage} src={imgUrl} alt={title} />
                </div>
            )}
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
    );
}

export default function Home() {
    const context = useDocusaurusContext();
    const { siteConfig = {} } = context;
    return (
        <Layout
            title={`Hello from ${siteConfig.title}`}
            description="Description will go into a meta tag in <head />"
        >
            <header className={clsx("hero hero--primary", styles.heroBanner)}>
                <div className="container">
                    <h1 className="hero__title">{siteConfig.title}</h1>
                    <p className="hero__subtitle">{siteConfig.tagline}</p>
                    <div className={styles.buttons}>
                        <Link
                            className={clsx(
                                "button button--outline button--secondary button--lg",
                                styles.getStarted,
                            )}
                            to={useBaseUrl("docs/tutorial/")}
                        >
                            Get Started
                        </Link>
                    </div>
                </div>
            </header>
            <main>
                {features && features.length > 0 && (
                    <section className={styles.features}>
                        <div className="container">
                            <div className="row">
                                {features.map((props, idx) => (
                                    <Feature key={idx} {...props} />
                                ))}
                            </div>
                        </div>
                    </section>
                )}
            </main>
        </Layout>
    );
}
