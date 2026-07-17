import streamlit as st
import streamlit.components.v1 as components


def show_chat_component():
    st.markdown(
        """
        <style>
            #chat-btn { position: fixed; bottom: 24px; right: 24px; width: 52px; height: 52px; border-radius: 50%; background: #33E6B3; border: none; cursor: pointer; box-shadow: 0 4px 16px rgba(51,230,179,0.4); display: flex; align-items: center; justify-content: center; z-index: 999999; }
            #chat-window { position: fixed; bottom: 88px; right: 24px; width: 320px; background: #1e2130; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); z-index: 999998; display: none; flex-direction: column; overflow: hidden; font-family: sans-serif; }
            #chat-window.open { display: flex; }
            #chat-header { background: #33E6B3; color: #0e1117; padding: 12px 16px; display: flex; align-items: center; justify-content: space-between; font-weight: 600; }
            #chat-messages { padding: 14px; flex: 1; overflow-y: auto; max-height: 260px; display: flex; flex-direction: column; gap: 10px; background: #0e1117; }
            .msg { max-width: 80%; padding: 8px 12px; border-radius: 16px; font-size: 13px; }
            .msg.bot { background: #1e2130; border: 1px solid #2e3250; color: #e0e0e0; align-self: flex-start; }
            .msg.user { background: #33E6B3; color: #0e1117; align-self: flex-end; }
            #chat-input-row { display: flex; padding: 10px 12px; border-top: 1px solid #2e3250; gap: 8px; background: #1e2130; }
            #chat-input { flex: 1; border: 1px solid #2e3250; border-radius: 20px; padding: 7px 14px; font-size: 13px; background: #0e1117; color: #e0e0e0; }
            #send-btn { background: #33E6B3; border: none; border-radius: 50%; width: 34px; height: 34px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        </style>

        <button id="chat-btn" title="Messaging">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="#0e1117"><path d="M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2z"/></svg>
        </button>

        <div id="chat-window">
            <div id="chat-header">
                Direktkontakt
                <button id="close-btn" style="background:none; border:none; cursor:pointer;">&#x2715;</button>
            </div>
            <div id="chat-messages">
                <div class="msg bot">Diese Chat-Funktion ermöglicht dir den direkten Kontakt zu deinem zuständigen Sachbearbeiter/in bei der Arbeitsagentur.</div>
            </div>
            <div id="chat-input-row">
                <input id="chat-input" type="text" placeholder="Nachricht schreiben…" />
                <button id="send-btn"><svg viewBox="0 0 24 24" width="16" height="16" fill="#0e1117"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg></button>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # JavaScript
    components.html(
        """
        <script>
            const d = window.parent.document;
            const btn = d.getElementById('chat-btn');
            const win = d.getElementById('chat-window');
            const closeBtn = d.getElementById('close-btn');
            const input = d.getElementById('chat-input');
            const sendBtn = d.getElementById('send-btn');
            const messages = d.getElementById('chat-messages');

            btn.onclick = () => win.classList.toggle('open');
            closeBtn.onclick = () => win.classList.remove('open');

            function addMessage(text, type) {
                const div = document.createElement('div');
                div.className = 'msg ' + type;
                div.innerHTML = text; // Erlaubt Zeilenumbrüche
                messages.appendChild(div);
                messages.scrollTop = messages.scrollHeight;
            }

            function send() {
                const text = input.value.trim();
                if (!text) return;
                addMessage(text, 'user');
                input.value = '';
                setTimeout(() => addMessage('Vielen Dank! Deine Nachricht wurde an den zuständigen Sachbearbeiter weitergeleitet.', 'bot'), 600);
            }

            sendBtn.onclick = send;
            input.onkeydown = (e) => { if (e.key === 'Enter') send(); };
        </script>
        """,
        height=0,
    )
