from re import X
import pandas as pd
import streamlit as st
# import plotly.express as px
import plotly.graph_objects as go
from gui import Gui


st.config.dataFrameSerialization = "arrow"
if __name__ == "__main__":
    gui = Gui()
    gui.main()