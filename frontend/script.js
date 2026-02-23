// ✅ CHANGE THIS if your backend runs on another port
const API_BASE = "http://127.0.0.1:5000"; // Flask example
// const API_BASE = "http://127.0.0.1:8000"; // FastAPI example

const chatEl = document.getElementById("chat");
const inputEl = document.getElementById("input");
const btnSend = document.getElementById("btnSend");
const btnClear = document.getElementById("btnClear");
const toastEl = document.getElementById("toast");

const STORAGE_KEY = "offline_chatbot_history_v1";

function toast(msg) {
  toastEl.textContent = msg;
  toastEl.classList.add("show");
  setTimeout(() => toastEl.classList.remove("show"), 1800);
}

function nowTime() {
  const d = new Date();
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function addMessage(role, text, meta = "") {
  const wrap = document.createElement("div");
  wrap.className = `msg ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  const metaEl = document.createElement("div");
  metaEl.className = "meta";
  metaEl.textContent = meta || nowTime();

  wrap.appendChild(bubble);
  wrap.appendChild(metaEl);
  chatEl.appendChild(wrap);
  chatEl.scrollTop = chatEl.scrollHeight;

  return wrap; // ✅ return node so we can update it (typing loader)
}

function addTypingMessage() {
  const wrap = document.createElement("div");
  wrap.className = "msg bot";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  // ✅ animated typing dots
  bubble.innerHTML = `
    <span class="typing">
      <span class="dot"></span>
      <span class="dot"></span>
      <span class="dot"></span>
    </span>
  `;

  const metaEl = document.createElement("div");
  metaEl.className = "meta";
  metaEl.textContent = " ";

  wrap.appendChild(bubble);
  wrap.appendChild(metaEl);
  chatEl.appendChild(wrap);
  chatEl.scrollTop = chatEl.scrollHeight;

  return wrap;
}

function setBusy(isBusy) {
  btnSend.disabled = isBusy;
  inputEl.disabled = isBusy;
  btnClear.disabled = isBusy;
}

function loadHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const items = JSON.parse(raw);
    if (!Array.isArray(items)) return;
    items.forEach(m => addMessage(m.role, m.text, m.meta));
  } catch {
    // ignore
  }
}

function saveToHistory(role, text) {
  const meta = nowTime();
  const entry = { role, text, meta };

  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const items = raw ? JSON.parse(raw) : [];
    const safe = Array.isArray(items) ? items : [];
    safe.push(entry);

    // keep last 200 messages max
    const trimmed = safe.slice(-200);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmed));
  } catch {
    // ignore
  }
}

function clearChat() {
  chatEl.innerHTML = "";
  localStorage.removeItem(STORAGE_KEY);
  toast("Chat cleared ✅");
}

function autoGrowTextarea() {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 140) + "px";
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  inputEl.value = "";
  autoGrowTextarea();

  addMessage("user", text);
  saveToHistory("user", text);

  // ✅ typing loader message (animated)
  const typingNode = addTypingMessage();

  setBusy(true);

  // ✅ 15s timeout so it never hangs forever
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 15000);

  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!res.ok) {
      const t = await res.text();
      throw new Error(`HTTP ${res.status}: ${t}`);
    }

    const data = await res.json();

    // ✅ Your backend returns: { status, response, timestamp }
    const reply = data.response ?? "No response field found.";

    // remove typing loader
    typingNode?.remove();

    addMessage("bot", reply);
    saveToHistory("bot", reply);

  } catch (err) {
    clearTimeout(timeoutId);

    typingNode?.remove();

    addMessage("bot", "⚠️ Server not responding (timeout). Check backend.");
    saveToHistory("bot", "Timeout / backend issue.");
    toast("Timeout after 15s ⚠️");
    console.error(err);

  } finally {
    setBusy(false);
    inputEl.focus();
  }
}

// Events
btnSend.addEventListener("click", sendMessage);
btnClear.addEventListener("click", clearChat);

inputEl.addEventListener("input", autoGrowTextarea);

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Init
loadHistory();
inputEl.focus();
autoGrowTextarea();