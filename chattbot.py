import json
import random
import re
import streamlit as st

# Load intents.json
with open("intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

intents = data["intents"]

# find fallback intent
noanswer_intent = next(i for i in intents if i["tag"] == "noanswer")

def normalize(text: str) -> str:
    text = text.lower().strip()
    # Replace punctuation with spaces
    text = re.sub(r"[^\w\s]", " ", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text

def matches(user_text: str, pattern: str) -> bool:
    user_text = normalize(user_text)
    pattern = normalize(pattern)

    if not pattern:
        return False

    # Single word: match whole word only
    if " " not in pattern:
        return re.search(rf"\b{re.escape(pattern)}\b", user_text) is not None

    # Multi-word phrase: match whole phrase with flexible spacing
    phrase_re = r"\b" + r"\s+".join(map(re.escape, pattern.split())) + r"\b"
    return re.search(phrase_re, user_text) is not None

def get_bot_response(user_text: str) -> str:
    pattern_list = []
    for intent in intents:
        for pattern in intent["patterns"]:
            pattern_list.append((pattern, intent))

    # Longer patterns first (more specific wins)
    pattern_list.sort(key=lambda x: len(x[0]), reverse=True)

    for pattern, intent in pattern_list:
        if matches(user_text, pattern):
            return intent["responses"][0]  # fixed response

    return random.choice(noanswer_intent["responses"])

# ---------------- STREAMLIT UI ----------------

st.title("AI Intents Chatbot 🤖")
st.write("Type a message below and the bot will respond using your intents.json!")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Your message:", key="input_box")

if st.button("Send"):
    if user_input.strip():
        bot_reply = get_bot_response(user_input)
        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("Bot", bot_reply))

for speaker, message in st.session_state.chat:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
