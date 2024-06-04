import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import json

def load_data(filepath):
    """ Load data from a JSON file. """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)['result']['rows']
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")
        return []

def display_data(flow_type, token_price):
    """ Display data for the selected flow type and calculate USD value. """
    display_text = ""
    filtered_data = [item for item in data if item['flow'] == flow_type or flow_type == "All"]
    for item in filtered_data:
        qty = float(item['token_qty'])
        usd_value = qty * token_price
        display_text += f"Flow: {item['flow']}\nQuantity: {qty}\nUSD Value: ${usd_value:.2f}\n\n"
    text_area.config(state=tk.NORMAL)
    text_area.delete('1.0', tk.END)
    text_area.insert(tk.END, display_text)
    text_area.config(state=tk.DISABLED)

def on_select(event):
    """ Handle selection from combo box. """
    flow = combo_box.get()
    display_data(flow, token_price)

def visualize_all_data(token_price):
    """ Visualize all data in a bar chart. """
    flows = [item['flow'] for item in data]
    quantities = [float(item['token_qty']) * token_price for item in data]
    ax.clear()  # Clear the existing bars
    ax.bar(flows, quantities, color=plt.cm.Paired(range(len(flows))))
    ax.set_ylabel('USD Value')
    ax.set_title('Token Flow USD Values')
    ax.set_xticklabels(flows, rotation=45, ha="right")
    canvas.draw()

# Load data and set the token price
data_filepath = '/Users/gedizucar/Desktop/dune_data.json'
token_price = 2.16  # Update as needed
data = load_data(data_filepath)

# Create main window
window = tk.Tk()
window.title("Token Data Viewer")

# Prepare the Matplotlib figure
fig = Figure(figsize=(8, 4))
ax = fig.add_subplot(111)

# Create the canvas to embed the figure
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a frame for drop-down and text display
frame = tk.Frame(window)
frame.pack(fill=tk.X)

# Create drop-down menu for flow types
all_flows = ['All'] + sorted(set(item['flow'] for item in data))
combo_box = ttk.Combobox(frame, values=all_flows, state='readonly')
combo_box.current(0)  # Set to 'All'
combo_box.pack(side=tk.LEFT, padx=5, pady=5)
combo_box.bind("<<ComboboxSelected>>", on_select)

# Scrolled Text Area for output
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, height=10, state='disabled')
text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Initial visualization of all data
visualize_all_data(token_price)

window.mainloop()
