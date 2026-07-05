const chatbox = document.getElementById("chatbox");
const input = document.getElementById("message");

function addMessage(sender, text) {
    const message = document.createElement("div");

    if (sender === "user") {
        message.className = "message user";
        message.innerHTML = `<strong>You:</strong><br>${text}`;
    } else {
        message.className = "message ai";
        message.innerHTML = `<strong>JARVIS:</strong><br>${text}`;
    }

    chatbox.appendChild(message);
    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {

    const text = input.value.trim();

    if (text === "") return;

    addMessage("user", text);

    input.value = "";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });

        const data = await response.json();

        addMessage("jarvis", data.reply);

    } catch (err) {

        addMessage(
            "jarvis",
            "Connection failed. Is the server running?"
        );

    }

}

input.addEventListener("keypress", function(event){

    if(event.key === "Enter"){
        sendMessage();
    }

});
