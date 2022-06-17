from re import X
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import os
import random

DIRNAME = os.path.dirname(__file__)
FILENAME_BLOCKS = os.path.join(DIRNAME, '../data/blocks.csv')

class Gui():
    def __init__(self):
        self.color_list = ["Red", "Green", "Blue", "Yellow", "RoyalBlue", "LightSkyBlue"]
        self.blocks = self.load_data()

    # @staticmethod
    def button_callback(self):
        st.write(self.blocks.shape[0])
        st.write(self.x_origin_input + " " + self.x_length_input + " " + self.y_origin_input + " " + self.y_length_input)
        new_element = {
            'x_origin': float(self.x_origin_input),
            'y_origin': float(self.y_origin_input),
            'x_length': float(self.x_length_input),
            'y_length': float(self.y_length_input)
        }
        self.blocks = self.blocks.append(new_element, ignore_index=True)
        self.add_elements()
        st.plotly_chart(self.fig)
        st.write(self.blocks.shape[0])
        self.save_blocks()

    def load_data(self):
        blocks = pd.read_csv(FILENAME_BLOCKS)
        return blocks 
    
    def save_blocks(self):
        self.blocks.to_csv(FILENAME_BLOCKS, index = False)

    def prepare_fig(self):
        self.fig = go.Figure()
        self.fig.add_trace(go.Scatter())
        # Set axes properties
        self.fig.update_xaxes(range=[self.blocks["x_origin"].min()-1, self.blocks["x_origin"].max()+self.blocks["x_length"].max()])
        self.fig.update_yaxes(range=[self.blocks["y_origin"].min()-1, self.blocks["y_origin"].max()+self.blocks["y_length"].max()])
    
    def prepare_widgets(self):
        self.x_origin_input = st.text_input("x_origin")
        self.x_length_input = st.text_input("x_length")
        self.y_origin_input = st.text_input("y_origin")
        self.y_length_input = st.text_input("y_length")
        self.button = st.button('Insert new block', on_click=self.button_callback)
    
    def add_elements(self):
        for row in self.blocks.iterrows():
            self.fig.add_shape(type="rect",
                x0=row[1][0], y0=row[1][1], x1=row[1][0] + row[1][2], y1=row[1][1] + row[1][3],
                line=dict(color="RoyalBlue"),
                fillcolor=self.color_list[random.randint(0, len(self.color_list)-1)],
            )
        self.fig.update_shapes(dict(xref='x', yref='y'))
    
    def main(self):
        self.prepare_fig()
        self.prepare_widgets()
        # Add shapes
        self.add_elements()
        self.chart = st.plotly_chart(self.fig)

