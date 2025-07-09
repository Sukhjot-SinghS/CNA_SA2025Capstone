# pip install panel bokeh pandas --quiet
import numpy as np
import pandas as pd
from datetime import datetime
import panel as pn
from bokeh.plotting import figure
from bokeh.palettes import Category20
# Load and prepare data
google_drive_url = 'https://drive.google.com/file/d/1RqHF3zphAFOtYZgReDJUxEFweOiVAxqP/view?usp=sharing'
file_id = google_drive_url.split('/')[-2]
download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
df = pd.read_csv(download_url)

df['Timestamp'] = pd.to_datetime(df['LastUpdatedDate'] + ' ' + df['LastUpdatedTime'],
                                 format='%d-%m-%Y %H:%M:%S')
df = df.sort_values(['SystemCodeNumber', 'Timestamp']).reset_index(drop=True)

def calculate_flexible_stateful_pricing(df, base_price=10.0, alpha=0.5, min_price=5.0, max_price=50.0):
    df['Date'] = df['Timestamp'].dt.date
    df_sorted = df.sort_values(['SystemCodeNumber', 'Date', 'Timestamp']).copy()
    df_sorted['price'] = 0.0
    prev_prices = {}
    for idx, row in df_sorted.iterrows():
        lot = row['SystemCodeNumber']
        date = row['Date']
        occupancy = row['Occupancy']
        capacity = row['Capacity']
        key = (lot, date)
        if key not in prev_prices:
            current_price = base_price + alpha * (occupancy / capacity)
        else:
            prev_price = prev_prices[key]
            current_price = prev_price + alpha * (occupancy / capacity)
        current_price = max(min_price, min(current_price, max_price))
        current_price = round(current_price, 2)
        prev_prices[key] = current_price
        df_sorted.at[idx, 'price'] = current_price
    return df_sorted

df = calculate_flexible_stateful_pricing(df)
pn.extension('tabulator')

unique_lots = df['SystemCodeNumber'].unique()
palette = Category20[max(3, min(len(unique_lots), 20))]

def get_color(idx):
    return palette[idx % len(palette)]

# Create a live plot for each lot using Panel's streaming and periodic callback
panels = []
for idx, lot in enumerate(unique_lots):
    lot_df = df[df['SystemCodeNumber'] == lot].copy()
    lot_df = lot_df.sort_values('Timestamp')
    color = get_color(idx)
    p = figure(
        height=400,
        width=800,
        title=f"Live Stateful Pricing Model (Lot: {lot})",
        x_axis_type="datetime",
    )
    renderer_line = p.line([], [], line_width=2, color=color, legend_label=str(lot))
    renderer_circle = p.circle([], [], size=6, color=color, legend_label=str(lot))
    p.legend.click_policy = "hide"

    # Panel DataFrame widget for live updates
    stream = pn.widgets.DataFrame(lot_df[['Timestamp', 'price']], width=800, height=100)
    
    # Periodic callback to simulate live updates
    def update_plot(event=None, lot_df=lot_df, renderer_line=renderer_line, renderer_circle=renderer_circle, stream=stream):
        # Simulate streaming by incrementally revealing data
        current_length = len(renderer_line.data_source.data['x'])
        if current_length < len(lot_df):
            new_x = list(lot_df['Timestamp'][:current_length+1])
            new_y = list(lot_df['price'][:current_length+1])
            renderer_line.data_source.data = {'x': new_x, 'y': new_y}
            renderer_circle.data_source.data = {'x': new_x, 'y': new_y}
            stream.value = lot_df[['Timestamp', 'price']][:current_length+1]
    
    cb = pn.state.add_periodic_callback(update_plot, period=90, count=len(lot_df))
    panels.append(pn.Column(p, stream))

dashboard = pn.Tabs(*[(str(lot), panel) for lot, panel in zip(unique_lots, panels)])
dashboard.servable()

