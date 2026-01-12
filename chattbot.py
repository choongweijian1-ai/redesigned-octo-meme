import json
import random
import streamlit as st

# Load intents.json
with open("intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

intents = data["intents"]

# find fallback intent
noanswer_intent = next(i for i in intents if i["tag"] == "noanswer")

def get_bot_response(user_text: str) -> str:
    user_text = user_text.lower()

    pattern_list = []
    for intent in intents:
        for pattern in intent["patterns"]:
            pattern_list.append((pattern.lower(), intent))

    pattern_list.sort(key=lambda x: len(x[0]), reverse=True)

    for pattern_lower, intent in pattern_list:
        if (
            pattern_lower and (
                user_text == pattern_lower or
                pattern_lower in user_text or
                user_text in pattern_lower
            )
        ):
            return random.choice(intent["responses"])

    return random.choice(noanswer_intent["responses"])


# ---------------- STREAMLIT UI ----------------

st.title("AI Intents Chatbot 🤖")

st.write("Type a message below and the bot will respond using your intents.json!")

# chat log stored in session_state
if "chat" not in st.session_state:
    st.session_state.chat = []

# user input
user_input = st.text_input("Your message:", key="input_box")

if st.button("Send"):
    if user_input.strip() != "":
        bot_reply = get_bot_response(user_input)

        st.session_state.chat.append(("You", user_input))
        st.session_state.chat.append(("Bot", bot_reply))

# display chat history
for speaker, message in st.session_state.chat:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
