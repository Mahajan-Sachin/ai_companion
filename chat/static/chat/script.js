/* ───────────────────────────────────────────
   Typewriter queue — smooths out fast Groq tokens
   Chars are released at CHAR_DELAY_MS intervals
   so the response always feels naturally typed,
   even if Groq delivers everything in <1 second.
─────────────────────────────────────────── */

const CHAR_DELAY_MS = 18          // ~55 chars/sec — natural fast typing
const charQueue     = []
let   renderTimer   = null
let   streamDone    = false
let   activeBubble  = null


function enqueueChars(bubble, text) {
    activeBubble = bubble
    for (const char of text) {
        charQueue.push(char)
    }
    // start the timer only if it isn't already running
    if (!renderTimer) {
        renderTimer = setInterval(flushQueue, CHAR_DELAY_MS)
    }
}

function flushQueue() {
    if (charQueue.length === 0) {
        // if streaming from server is also done, clean up
        if (streamDone && activeBubble) {
            clearInterval(renderTimer)
            renderTimer  = null
            removeCursor(activeBubble)
            activeBubble = null
            streamDone   = false
        }
        return
    }
    const char   = charQueue.shift()
    const cursor = activeBubble.querySelector(".stream-cursor")
    activeBubble.insertBefore(document.createTextNode(char), cursor)
    document.getElementById("messages").scrollTop =
        document.getElementById("messages").scrollHeight
}


/* ── Static message helper (used for user bubbles) ── */

function addMessage(text, sender) {

    const chat   = document.getElementById("messages")
    const row    = document.createElement("div")
    row.classList.add("message-row")

    const bubble = document.createElement("div")
    bubble.classList.add("message")

    const avatar = document.createElement("div")
    avatar.classList.add("avatar")

    if (sender === "user") {
        row.classList.add("user-row")
        bubble.classList.add("user")
        avatar.classList.add("user-avatar")
        avatar.innerText = "🙂"
        row.appendChild(bubble)
        row.appendChild(avatar)
    } else {
        bubble.classList.add("ai")
        avatar.classList.add("ai-avatar")
        avatar.innerText = "🤖"
        row.appendChild(avatar)
        row.appendChild(bubble)
    }

    bubble.innerText = text
    chat.appendChild(row)
    chat.scrollTop = chat.scrollHeight
}


/* ── Streaming bubble ── */

function createStreamingBubble() {

    const chat   = document.getElementById("messages")
    const row    = document.createElement("div")
    row.classList.add("message-row")

    const avatar = document.createElement("div")
    avatar.classList.add("avatar", "ai-avatar")
    avatar.innerText = "🤖"

    const bubble = document.createElement("div")
    bubble.classList.add("message", "ai")

    const cursor = document.createElement("span")
    cursor.classList.add("stream-cursor")
    cursor.innerText = "▋"
    bubble.appendChild(cursor)

    row.appendChild(avatar)
    row.appendChild(bubble)
    chat.appendChild(row)
    chat.scrollTop = chat.scrollHeight

    return bubble
}

function removeCursor(bubble) {
    const cursor = bubble.querySelector(".stream-cursor")
    if (cursor) cursor.remove()
}


/* ── Main send (async streaming) ── */

async function sendMessage() {

    const input   = document.getElementById("messageInput")
    const message = input.value
    input.value   = ""

    if (message.trim() !== "") {
        addMessage(message, "user")
    }

    // reset queue state for new message
    charQueue.length = 0
    streamDone       = false
    if (renderTimer) {
        clearInterval(renderTimer)
        renderTimer = null
    }

    const aiBubble = createStreamingBubble()

    try {
        const response = await fetch("/chat/stream/", {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ message: message })
        })

        const reader  = response.body.getReader()
        const decoder = new TextDecoder()
        let   buffer  = ""

        while (true) {
            const { done, value } = await reader.read()
            if (done) break

            buffer += decoder.decode(value, { stream: true })
            const lines = buffer.split("\n")
            buffer = lines.pop()  // hold incomplete last line

            for (const line of lines) {
                if (!line.startsWith("data: ")) continue
                const data = line.slice(6)
                if (data === "[DONE]") break
                const token = JSON.parse(data)
                enqueueChars(aiBubble, token)  // ← queue, don't render instantly
            }
        }

    } catch (err) {
        // stop queue and show error
        clearInterval(renderTimer)
        renderTimer = null
        charQueue.length = 0
        removeCursor(aiBubble)
        aiBubble.innerText = "⚠️ Error getting response."
        return
    }

    // signal queue that server is done — cursor removed after last char renders
    streamDone = true
    // if queue already empty, clean up immediately
    if (charQueue.length === 0 && renderTimer === null) {
        removeCursor(aiBubble)
        streamDone   = false
        activeBubble = null
    }
}


/* ── Enter key support ── */
document.getElementById("messageInput")
    .addEventListener("keypress", function (e) {
        if (e.key === "Enter") sendMessage()
    })