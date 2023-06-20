# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:20:10 2023

@author: sadeghi.a
"""
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_dependency_graph():
    # Open file dialog to select the Excel file
    file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
    if file_path:
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Create an empty graph
        G = nx.DiGraph()

        # Recursive function to add nodes and edges to the graph with weights
        def add_dependencies(dependent, dependencies, weight):
            for dependency in dependencies:
                dependency_parts = dependency.split('.')
                last_dependency = dependency_parts[-1]
                G.add_edge(dependent, last_dependency, weight=weight)
                add_dependencies(last_dependency, df.loc[df['Policy.name'].str.startswith(dependency + '.')]['Policy.name'].tolist(), weight - 1)

        # Iterate over the rows of the DataFrame
        for index, row in df.iterrows():
            dependent = row['Policy.name']
            dependencies = df.loc[df['Policy.name'].str.startswith(dependent + '.')]['Policy.name'].tolist()
            dependency_parts = dependent.split('.')
            last_dependent = dependency_parts[-1]
            G.add_node(last_dependent, subset=len(dependency_parts))
            add_dependencies(last_dependent, dependencies, len(dependency_parts))

        # Create a layout hierarchy
        pos = nx.multipartite_layout(G, subset_key='subset', align='vertical')

        # Create a figure and canvas
        fig, ax = plt.subplots(figsize=(12, 8))
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()

        # Draw the graph on the canvas
        nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=10, edge_color='gray', arrows=True, ax=ax)
        ax.set_title('Dependency Graph')

        # Update the canvas
        canvas.draw()

# Create the GUI
root = tk.Tk()

# Function to handle button click
def on_button_click():
    generate_dependency_graph()

# Create a button to depict the graph
button = tk.Button(root, text="Depict Graph", command=on_button_click)
button.pack(pady=10)

# Run the GUI main loop
root.mainloop()
