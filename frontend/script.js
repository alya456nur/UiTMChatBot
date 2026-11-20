const inputMessage = document.getElementById("inputMessage");
const sendBtn = document.getElementById("sendBtn");
const chatbox = document.getElementById("chatbox");

function appendMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);

    const textBubble = document.createElement("span");
    textBubble.classList.add("text-bubble");

    // Markdown → HTML for bot, raw text for user
    if (sender === "bot") {
        textBubble.innerHTML = marked.parse(text);
    } else {
        textBubble.textContent = text;
    }

    if (sender === "bot") {
        const iconImg = document.createElement("img");
        iconImg.src = "logo.png";
        iconImg.classList.add("bot-chat-logo");
        iconImg.alt = "bot logo";
        msgDiv.appendChild(iconImg);
    }

    msgDiv.appendChild(textBubble);
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
    const message = inputMessage.value.trim();
    if (!message) return;

    appendMessage(message, "user");
    inputMessage.value = "";
    sendBtn.disabled = true;

    try {
        // Updated to relative path since backend and frontend are together
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();
        appendMessage(data.reply, "bot");

    } catch (err) {
        appendMessage("Error: Server not reachable", "bot");
    } finally {
        sendBtn.disabled = false;
        inputMessage.focus();
    }
}

sendBtn.addEventListener("click", sendMessage);

inputMessage.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

window.onload = () => {
    appendMessage("Hi! I'm UiTM Bot 🎓 Ask me anything about UiTM!", "bot");
};