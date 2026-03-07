function addMessage(text, sender){

    const chat = document.getElementById("messages")

    const row = document.createElement("div")
    row.classList.add("message-row")

    const bubble = document.createElement("div")
    bubble.classList.add("message")

    const avatar = document.createElement("div")
    avatar.classList.add("avatar")

    if(sender === "user"){

        row.classList.add("user-row")

        bubble.classList.add("user")

        avatar.classList.add("user-avatar")
        avatar.innerText="🙂"

        row.appendChild(bubble)
        row.appendChild(avatar)

    }else{

        bubble.classList.add("ai")

        avatar.classList.add("ai-avatar")
        avatar.innerText="🤖"

        row.appendChild(avatar)
        row.appendChild(bubble)
    }

    bubble.innerText=text

    chat.appendChild(row)

    chat.scrollTop = chat.scrollHeight
}

function showTyping(){

    const chat=document.getElementById("messages")

    const row=document.createElement("div")
    row.classList.add("message-row")
    row.id="typing"

    const avatar=document.createElement("div")
    avatar.classList.add("avatar","ai-avatar")
    avatar.innerText="🤖"

    const bubble=document.createElement("div")
    bubble.classList.add("message","ai","typing")
    bubble.innerText="AI is typing..."

    row.appendChild(avatar)
    row.appendChild(bubble)

    chat.appendChild(row)

    chat.scrollTop=chat.scrollHeight
}

function removeTyping(){

    const typing=document.getElementById("typing")

    if(typing){
        typing.remove()
    }
}

function sendMessage(){

    const input=document.getElementById("messageInput")

    let message=input.value

    if(message.trim()!==""){
        addMessage(message,"user")
}

    input.value=""

    showTyping()

    fetch("/chat/",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            message:message
        })
    })

    .then(response=>response.json())

    .then(data=>{

        removeTyping()

        addMessage(data.reply,"ai")

    })
}


/* ENTER KEY SEND */
document.getElementById("messageInput")
.addEventListener("keypress",function(e){

    if(e.key==="Enter"){
        sendMessage()
    }

})