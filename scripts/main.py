import streamlit as st
from gui import Gui


    # The main file of the application - to run it, just type in
    # scripts directory: `streamlit run main.py`


st.config.dataFrameSerialization = "arrow"
if __name__ == "__main__":
    gui = Gui()
    gui.main()