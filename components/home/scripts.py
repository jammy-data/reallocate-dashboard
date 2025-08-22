import streamlit as st
import streamlit.components.v1 as components

def render_scripts():
    """
    Include custom JS scripts in the app.
    """
    components.html("""
    <script>
        function sendMessage(sumi) {
            const streamlitInput = window.parent.document.querySelector("input[pilots-testid='stTextInput']");
            streamlitInput.value = sumi;
            streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
        }
    </script>
    """, height=200)
