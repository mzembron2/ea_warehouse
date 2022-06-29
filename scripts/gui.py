from warehouse import Warehouse
from block import Block
from evolutionary_algorithm import EvolutionaryAlgorithm
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import os
import json

DIRNAME = os.path.dirname(__file__)
FILENAME_BLOCKS = os.path.join(DIRNAME, '../data/blocks.csv')
FILENAME_SETTINGS = os.path.join(DIRNAME, '../data/settings.json')

class Gui():

    """
        Simple GUI made with Streamlit python library.

        Allows the user to change algorithm parameters, add blocks, and
        most importantly,  running the algorithm and viewing the solution.

    """
    def __init__(self):
        self.blocks = self.load_data()
        self.settings = self.load_settings()

    def button_add_block_callback(self):
        st.text("Available blocks: ")
        self.blocks = self.load_data()
        try:
            if(self.x_length_input != "" and self.y_length_input != "" and
            float(self.x_length_input)>0 and float(self.y_length_input) > 0):

                new_element = {
                    'x_origin': [8],
                    'y_origin': [8],
                    'x_length': [float(self.x_length_input)],
                    'y_length': [float(self.y_length_input)]
                }
                self.blocks = pd.concat([self.blocks, pd.DataFrame(data = new_element)],
                    ignore_index=True)
        except ValueError:
            print("Not an int!")
        self.prepare_fig()
        self.add_elements_to_plot()
        st.plotly_chart(self.fig)
        self.save_blocks()


    def button_update_settings_callback(self):
        self.load_settings()
        self.update_settings_parameter(self.warehouse_x_input, "warehouse_x")
        self.update_settings_parameter(self.warehouse_y_input,"warehouse_y")
        self.update_settings_parameter(self.population_input, "population")
        self.update_settings_parameter(self.iterations_input, "iterations")
        self.update_settings_parameter(self.crossover_input, "crossover")
        self.save_settings_to_json()


    def update_settings_parameter(self, parameter, parameter_name):
        if(parameter != ""):
            if(parameter_name != "crossover"):
                try:
                    int_param = int(parameter)
                    if(int_param >0):
                        self.settings[parameter_name] = int_param
                    else:
                        print("This parameter cannot be lower than 0!")
                except ValueError:
                    print("Not an int!")
            else:
                if(str(parameter).lower() == "yes"):
                    self.settings["crossover"] = True

                elif (str(parameter).lower() == "no"):
                    self.settings["crossover"] = False
                
                else: 
                    print("Answear to use crossover must be yes or no!")

    def _ea_button_callback(self):
        self.load_settings()
        wh_y = self.settings["warehouse_y"]
        wh_x = self.settings["warehouse_x"]
        population = self.settings["population"]
        iterations = self.settings["iterations"]
        crossover = self.settings["crossover"]
        st.text("Running with settings: wh size: %ix%i, population size: %i, max iterations: %i, crossover: %s"
            %(wh_x, wh_y, population, iterations, str(crossover)))
        base_wh = Warehouse(wh_y, wh_x)
        for area in self.settings["unavailable"]:
            if(type(area) == list):
                base_wh.set_unavailable_area(area[0], area[1], area[2], area[3])
            else:
                print("Wrong format unavailable area!")
        ea = EvolutionaryAlgorithm(population_size= population,
            iterations_number = iterations, use_crossover = crossover,
            warehouse= base_wh, p_c = 0.5)

        wh = ea.run()
        self.display_warehouse(wh)

    def load_data(self):
        blocks = pd.read_csv(FILENAME_BLOCKS)
        return blocks 
    
    def load_settings(self):
        json_file = open(FILENAME_SETTINGS)
        self.settings = json.load(json_file)
    
    def save_settings_to_json(self):
        with open(FILENAME_SETTINGS, 'w') as json_file:
            json.dump(self.settings, json_file)

    def display_warehouse(self, warehouse: Warehouse):
        st.text("Optimal warehouse setup: ")
        (rows, cols) = np.shape(warehouse.warehouse_matrix)
        self.prepare_fig(rows, cols)
        self.add_blocks_to_plot(warehouse)
        self.add_unavailable_area_to_plot(warehouse)
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
        st.markdown("# Evolutionary Algorithm")
        self.button = st.button('Run evolution', on_click=self._ea_button_callback)

        st.markdown("# Settings section")
        self.load_settings()
        wh_y = self.settings["warehouse_y"]
        wh_x = self.settings["warehouse_x"]
        population = self.settings["population"]
        iterations = self.settings["iterations"]
        crossover = self.settings["crossover"]
        crossover_yes_no = "yes" if crossover  else "no"

        st.markdown("## Parameters")
        self.warehouse_x_input = st.text_input("warehouse x length (current: %i)"%
        wh_x)
        self.warehouse_y_input = st.text_input("warehouse y length (current: %i)"%
        wh_y)
        self.population_input = st.text_input("population size (current: %i)"%
        population)
        self.iterations_input = st.text_input("Maximum iterations (current: %i)"%
        iterations)
        self.crossover_input = st.text_input("Use crossover: yes/no (current: %s)"%
        crossover_yes_no)
        self.button = st.button('Update parameters', on_click=self.button_update_settings_callback)

        st.markdown("## Add block")
        self.x_length_input = st.text_input("Block x length")
        self.y_length_input = st.text_input("Block y length")
        self.button = st.button('Insert new block', on_click=self.button_add_block_callback)

    def add_blocks_to_plot(self, warehouse: Warehouse):
        for block_index in warehouse.blocks_in_warehouse:
            current_block = warehouse.blocks_dict[block_index]
            x_origin = current_block.x_origin
            y_origin = current_block.y_origin
            x_len = current_block.x_length
            y_len = current_block.y_length

            self.fig.add_shape(type="rect",
                x0=y_origin, y0=-x_origin, x1=y_origin +
                    y_len , y1=-(x_origin + x_len),
                editable = True,
                line=dict(color="RoyalBlue"),
                fillcolor="LightSkyBlue"
            )

    def add_unavailable_area_to_plot(self, warehouse: Warehouse):
        for unavailable_area in warehouse.unavailable_area_list:
            x_origin = unavailable_area.x_origin
            y_origin = unavailable_area.y_origin
            x_len = unavailable_area.x_length
            y_len = unavailable_area.y_length

            self.fig.add_shape(type="rect", 
                x0=y_origin, y0=-x_origin, x1=y_origin +
                    y_len , y1=-(x_origin + x_len),
                line=dict(color="Red"),
                fillcolor="grey",
            )
        self.fig.update_shapes(dict(xref='x', yref='y'))

    def add_elements_to_plot(self):
        for index, row in self.blocks.iterrows():
            self.fig.add_shape(type="rect",
                x0=row['y_origin'], y0=-row['x_origin'], x1=row['y_origin'] +
                    row['y_length'] , y1= -(row['x_origin'] + row['x_length']),
                line=dict(color="RoyalBlue"),
                editable = True,
                fillcolor="LightSkyBlue"
            )
        self.fig.update_shapes(dict(xref='x', yref='y'))
    
    def main(self):
        self.prepare_widgets()
        

