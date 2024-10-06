import streamlit as st
import leafmap.foliumap as leafmap
import time
import ollama

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""
st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("Interactive Map with Chatbot")

# Use columns to adjust layout
col1, col2 = st.columns([3, 1])  # La prima colonna è più grande (mappa), la seconda è più piccola (chatbot)

with col1:
    # Map section
    m = leafmap.Map(minimap_control=True)
    m.add_basemap("OpenTopoMap")
    m.to_streamlit(height=500)

with col2:
    # Chatbot section
    def stream_data(text):
        delay = 0.1  # Imposta un ritardo per il flusso dei dati
        output = ""  # Mantiene il testo completo che stiamo costruendo
        for word in text.split():
            output += word + " "
            st.write(output)  # Aggiorna dinamicamente il contenuto della chat
            time.sleep(delay)

    # Input per il prompt (istruzione)
    instruction = st.chat_input("Ask Emiscan")

    if instruction:
        # Visualizza l'input dell'utente
        with st.chat_message("user"):
            st.write(instruction)

        # Elaborazione del prompt
        with st.spinner("Thinking ..."):
            try:
                result = ollama.chat(model="francescomassa/emiscanmk2", messages=[{
                    "role": "user",
                    "content": instruction,
                }])
                response = result["message"]["content"]  # Assumendo che il campo esista
            except Exception as e:
                st.error(f"Error: {e}")
                response = None

        # Mostra la risposta del chatbot, se esiste
        if response:
            stream_data(response)
