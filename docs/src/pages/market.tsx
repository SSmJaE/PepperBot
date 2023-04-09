import marketSource from "!!raw-loader!../../../archive/market.yaml";
import yaml from "js-yaml";
import debounce from "lodash/debounce";
import React, { useCallback, useMemo, useState } from "react";

import Link from "@docusaurus/Link";
import useBaseUrl from "@docusaurus/useBaseUrl";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import { Theme } from "@emotion/react";
import styled from "@emotion/styled";
import CodeBlock from "@theme/CodeBlock";
import Layout from "@theme/Layout";

import { CapabilityType, capabilityTypes, packageManagers, store, useStore } from "../store";

interface ICapability {
    name: string;
    type: CapabilityType[];
    /** 这个是可选的，并不强求 */
    "package-name"?: string;
    "import-code"?: string;
    repository: string;
    /** 一些简短的描述，不需要详细描述，想要看详细描述的话，可以直接跳转到仓库 */
    description: string;
}

interface IMarket {
    capabilities: ICapability[];
}

const MARKET = yaml.load(marketSource) as IMarket;
console.log(MARKET);

const ItemContainer = styled.div({
    border: "2px solid black",
    borderRadius: "8px",
});

const ItemField = styled.div({
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    // border: "1px solid hotpink",
    margin: "8px 0px",
    fontSize: "24px",
    fontFamily: "Consolas",
});

const ItemFieldLabel = styled.div({
    margin: "0px 16px",
    fontSize: "24px",
    fontFamily: "华文新魏",
    width: "100px",
    flexShrink: 0,
});

function CopyableCommand({ children }: { children: React.ReactNode }) {
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "row",
                alignItems: "center",
                position: "relative",
            }}
        >
            <div
                style={{
                    // backgroundColor: "#ccc",
                    whiteSpace: "pre-wrap",
                }}
            >
                {children}
            </div>
            {/* <button
                style={{
                    // position: "relative",
                    // right: "8px",
                    // backgroundColor: "grey",
                    border: "1px solid black",
                }}
                onClick={() => {
                    navigator.clipboard.writeText(children);
                }}
            >
                点击复制
            </button> */}
        </div>
    );
}

export function Capability({ data }: { data: ICapability }) {
    return (
        <ItemContainer>
            <div>
                <ItemField>
                    <ItemFieldLabel>项目名称</ItemFieldLabel>
                    <div>{data.name}</div>
                </ItemField>

                <ItemField>
                    <ItemFieldLabel>项目类型</ItemFieldLabel>
                    <div>{data.type.join(", ")}</div>
                </ItemField>

                <ItemField>
                    <ItemFieldLabel>项目仓库</ItemFieldLabel>
                    <Link to={data.repository}>{data.repository}</Link>
                    {/* <div>{data.repository}</div> */}
                </ItemField>

                {data["package-name"] && (
                    <ItemField>
                        <ItemFieldLabel>安装指令</ItemFieldLabel>
                        <CopyableCommand>
                            {generateDownloadCommand(data["package-name"])}
                        </CopyableCommand>
                    </ItemField>
                )}

                {data["import-code"] && (
                    <ItemField>
                        <ItemFieldLabel>导入代码</ItemFieldLabel>
                        <CopyableCommand>{data["import-code"]}</CopyableCommand>
                    </ItemField>
                )}

                <ItemField>
                    <ItemFieldLabel>简要描述</ItemFieldLabel>
                    <div>
                        {data.description}
                        {/* {data.description}
                        {data.description} */}
                    </div>
                </ItemField>
            </div>
        </ItemContainer>
    );
}

function generateDownloadCommand(packageName: string) {
    const { packageManager } = useStore();

    if (packageManager === "pip") {
        return `pip install ${packageName}`;
    } else if (packageManager === "poetry") {
        return `poetry add ${packageName}`;
    } else if (packageManager === "pdm") {
        return `pdm add ${packageName}`;
    }
}

export const theme: Theme = {
    colors: {
        primary: "rgb(255, 255, 255)", // 60%
        secondary: "rgb(230, 230, 230)", // 30%
        active: "#2196f3", // 10%
        activeSecondary: "rgb(231, 243, 255)",
        error: "rgb(231, 71, 93)",
    },
    answerTypeColorMapping: {
        GPT: "orange",
        标答: "limegreen",
        无答案: "rgb(231, 71, 93)",
    },
};

const FilterItem = styled.div({
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    // gap: "8px",
    margin: "8px 0px",
});

const FilterItemLabel = styled.div({
    margin: "0px 16px",

    fontSize: "24px",
    fontFamily: "华文新魏",
    width: "100px",
    // flexShrink: 0,
});

const ButtonSwitchGroup = styled.div({
    display: "flex",
    flexDirection: "row",
    gap: "8px",
});

const ButtonSwitch = styled.div<{ active: boolean }>(
    {
        fontSize: "24px",
        fontFamily: "华文新魏",
        padding: "4px 8px",
        borderRadius: "8px",
    },
    ({ active }) => ({
        backgroundColor: active ? theme.colors.active : "white",
        color: active ? "white" : "black",
        ":hover": {
            backgroundColor: active ? theme.colors.active : theme.colors.secondary,
            cursor: "pointer",
        },
    }),
);

const SearchInput = styled.input({
    height: "40px",
    width: "600px",
    fontSize: "24px",
    fontFamily: "华文新魏",
    padding: "4px 8px",
    border: "none",
    borderBottom: "1px solid black",
    outline: "none" /* 防止点击后出现边框 */,
});

const FilterContainer = styled.div({
    display: "flex",
    flexDirection: "column",
    // alignItems: "center",
    justifyContent: "center",
    // gap: "8px",
    // margin: "8px 0px",
    width: "1000px",
    position: "fixed",
    height: "200px",
    // border: "1px solid hotpink",
    backgroundColor: "white",
    zIndex: 1, // 使得滚动时不会被遮挡
});

const CapabilitiesList = styled.div({
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    marginTop: "200px",
});

export default function Home() {
    const { selectedTypes, packageManager } = useStore();

    const [searchText, setSearchText] = useState("");
    const [debouncedSearchText, setDebouncedSearchText] = useState("");

    const debouncedSetSearchText = useCallback(
        debounce((value) => {
            setDebouncedSearchText(value);
        }, 300),
        [],
    );

    const filteredData: ICapability[] = useMemo(() => {
        return MARKET.capabilities.filter((item) => {
            if (selectedTypes.length > 0) {
                if (!selectedTypes.some((type) => item.type.includes(type))) {
                    return false;
                }
            }

            if (debouncedSearchText) {
                if (!JSON.stringify(item).includes(debouncedSearchText)) {
                    return false;
                }
            }

            return true;
        });
    }, [selectedTypes, debouncedSearchText]);

    return (
        <Layout sidebar>
            <div
                style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                }}
            >
                <div
                    style={{
                        width: "1000px",
                        // border: "1px solid hotpink",
                        display: "flex",
                        flexDirection: "column",
                    }}
                >
                    <FilterContainer>
                        <FilterItem>
                            <FilterItemLabel>搜索项目</FilterItemLabel>
                            <SearchInput
                                type="text"
                                placeholder="可以是名称、描述，任意满足都会匹配"
                                value={searchText}
                                onChange={(e) => {
                                    setSearchText(e.target.value);
                                    debouncedSetSearchText(e.target.value);
                                }}
                            />
                        </FilterItem>

                        <FilterItem>
                            <FilterItemLabel>项目类型</FilterItemLabel>
                            <ButtonSwitchGroup>
                                {capabilityTypes.map((type) => (
                                    <ButtonSwitch
                                        active={selectedTypes.includes(type)}
                                        onClick={() => store.toggleSelectedType(type)}
                                    >
                                        {type}
                                    </ButtonSwitch>
                                ))}
                            </ButtonSwitchGroup>
                        </FilterItem>

                        <FilterItem>
                            <FilterItemLabel>包管理器</FilterItemLabel>

                            <ButtonSwitchGroup>
                                {packageManagers.map((type) => (
                                    <ButtonSwitch
                                        active={packageManager === type}
                                        onClick={() => store.setPackageManager(type)}
                                    >
                                        {type}
                                    </ButtonSwitch>
                                ))}
                            </ButtonSwitchGroup>
                        </FilterItem>
                    </FilterContainer>

                    <CapabilitiesList>
                        {filteredData.map((capability) => {
                            return (
                                <Capability key={capability["package-name"]} data={capability} />
                            );
                        })}
                    </CapabilitiesList>
                </div>
            </div>
        </Layout>
    );
}
