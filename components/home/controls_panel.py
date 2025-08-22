import streamlit as st

def render_controls(col, indicators, update_pilots):
    """
    Render the left column controls for selecting SUMI indicators.

    Args:
        col (st.column): Streamlit column object (col1).
        indicators (dict): Dictionary of SUMI indicators.
        update_pilots (callable): Function to update the pilots based on selection.
    """
    with col:
        st.write("\n\n")
        
        # Header
        st.markdown('<h5 class="umi-title">Urban Mobility Indices</h5>', unsafe_allow_html=True)

        # Callback for button click
        def update_sumi(sumi):
            st.session_state['impact_area'] = None
            st.session_state["selected_sumi"] = sumi
            st.session_state.legend = sumi
            update_pilots()

        # Render a button for each SUMI category
        sumis = list(indicators.keys())
        for sumi in sumis:
            # Format string nicely
            sumi_string = sumi.replace("_", " ").title()
            st.button(sumi_string, on_click=update_sumi, args=(sumi,))
