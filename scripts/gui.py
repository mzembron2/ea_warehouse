from warehouse import Warehouse
from block import Block
from evolutionary_algorithm import EvolutionaryAlgotihm
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import copy
import os
import random

DIRNAME = os.path.dirname(__file__)
FILENAME_BLOCKS = os.path.join(DIRNAME, '../data/blocks.csv')

class Gui():
    def __init__(self):
        self.color_list = ["Red", "Green", "Blue", "Yellow", "RoyalBlue", "LightSkyBlue",
        "aliceblue", "lime", "orange", "purple", "dimgray", "navy", "white", "indigo"  ]
        self.blocks = self.load_data()

    def button_callback(self):
        st.write(self.blocks.shape[0])
        st.write(self.x_origin_input + " " + self.x_length_input + " " +
            self.y_origin_input + " " + self.y_length_input)
        new_element = {
            'x_origin': float(self.x_origin_input),
            'y_origin': float(self.y_origin_input),
            'x_length': float(self.x_length_input),
            'y_length': float(self.y_length_input)
        }
        self.blocks = self.blocks.append(new_element, ignore_index=True)
        self.add_elements_to_plot()
        st.plotly_chart(self.fig)
        st.write(self.blocks.shape[0])
        self.save_blocks()

    def ea_button_callback(self):
        ea = EvolutionaryAlgotihm(population_size=20, iterations_number=2000, use_crossover=True)
        wh = ea.run()
        self.display_warehouse(wh)

    def load_data(self):
        blocks = pd.read_csv(FILENAME_BLOCKS)
        return blocks 
    
    def display_warehouse(self, warehouse: Warehouse):
        (rows, cols) = np.shape(warehouse.warehouse_matrix)
        self.prepare_fig(rows, cols)
        self.add_blocks_to_plot(warehouse)
        st.plotly_chart(self.fig)

    def save_blocks(self):
        self.blocks.to_csv(FILENAME_BLOCKS, index = False)

    def prepare_fig(self, rows_max = 10, cols_max = 10):
        self.fig = go.Figure()
        self.fig.add_trace(go.Scatter())
        # Set axes properties
        self.fig.update_xaxes(range=[0, rows_max])
        self.fig.update_yaxes(range=[-cols_max, 0])
    
    def prepare_widgets(self):
        self.x_origin_input = st.text_input("x_origin")
        self.x_length_input = st.text_input("x_length")
        self.y_origin_input = st.text_input("y_origin")
        self.y_length_input = st.text_input("y_length")
        self.button = st.button('Insert new block', on_click=self.button_callback)

    def add_blocks_to_plot(self, warehouse: Warehouse):
        for block_index in warehouse.blocks_in_warehouse:
            current_block = warehouse.blocks_dict[block_index]
            x_origin = current_block.x_origin
            y_origin = current_block.y_origin
            x_len = current_block.x_length
            y_len = current_block.y_length

            self.fig.add_shape(type="rect", name = str(block_index),
                x0=y_origin, y0=-x_origin, x1=y_origin +
                    y_len , y1=-(x_origin + x_len),
                editable = True,
                line=dict(color="RoyalBlue"),
                fillcolor=self.color_list[random.randint(0, len(self.color_list)-1)],
            )
        self.fig.update_shapes(dict(xref='x', yref='y'))

    def add_elements_to_plot(self):
        for index, row in self.blocks.iterrows():
            self.fig.add_shape(type="rect",
                x0=row['x_origin'], y0=row['y_origin'], x1=row['x_origin'] +
                    row['x_length'] , y1=row['y_origin'] + row['y_length'],
                line=dict(color="RoyalBlue"),
                fillcolor=self.color_list[random.randint(0, len(self.color_list)-1)],
            )
        self.fig.update_shapes(dict(xref='x', yref='y'))
    
    def main(self):
        # self.prepare_fig()
        # self.prepare_widgets()
        # Add shapes
        # self.add_elements_to_plot()
        # self.chart = st.plotly_chart(self.fig)
        self.button = st.button('Run evolution', on_click=self.ea_button_callback)

