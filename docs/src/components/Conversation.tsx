import React from "react";

export interface IMessage {
    position: "left" | "right";
    sender: string;
    message: string;
}

export function Conversation({ messages }: { messages: IMessage[] }) {
    return (
        <div
            style={{
                width: "100%",
                border: "2px solid black",
                borderRadius: 8,
                fontSize: 24,
                fontFamily: "华文新魏",
                margin: "16px 0px",
            }}
        >
            {messages.map((message, index) => (
                <div
                    key={index}
                    style={{
                        position: "relative",
                        margin: "8px 0",
                    }}
                >
                    <div
                        style={{
                            display: "flex",
                            flexDirection: message.position === "left" ? "row" : "row-reverse",
                            alignItems: "center",
                            gap: 8,
                            position: "relative",
                            right: message.position === "right" ? 10 : undefined,
                            left: message.position === "left" ? 10 : undefined,
                        }}
                    >
                        <div>{message.sender}</div>
                        <div
                            style={{
                                whiteSpace: "pre-wrap",
                                border: "2px solid black",
                                padding: "4px 8px",
                                borderRadius: 8,
                            }}
                        >
                            {message.message}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}
