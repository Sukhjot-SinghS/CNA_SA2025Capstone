# 🚗 Dynamic Parking Pricing – Real-Time AI with Pathway
Welcome to the Dynamic Parking Pricing repository!
This project delivers robust, real-time parking price optimization using live data streams, interpretable models, and modern dashboards—all powered by the Pathway AI simulation engine.
# LIVE PLOTTING (not Static graphs)
# ✨ Features at a Glance
Live Data Streaming: Real-time ingestion and processing of parking lot data.

### Two Dynamic Models:

### Model 1: Simple, interpretable baseline pricing.

### Model 2: Advanced, demand-driven pricing with contextual features.

Interactive Dashboards: Beautiful, live-updating visualizations for up to 14 lots.

Extensible & Production-Ready: Easy to adapt, scale, and deploy.

# 🛠️ Tech Stack
![image](https://github.com/user-attachments/assets/7b3833bb-9f6e-488e-8c55-d10c9a535a08)
# 🏗️ Architecture Diagram
![image](https://github.com/user-attachments/assets/e302f2af-0308-4b77-bd50-3f8aee4d3eb7)


# 📚 Project Workflow
### 1. Data Preparation
Load parking data from CSV or real-time feed.

Ensure all columns are present; fill defaults if missing.

Combine date and time to a single timestamp.

Sort by lot and timestamp for streaming.

### 2. Pathway Streaming Pipeline
Define schema for all features.

Stream data using Pathway’s replay or real-time connectors.

### 3. Model 1: Baseline Linear Pricing
Formula:
#### Price = BasePrice + α × (Occupancy / Capacity)

Stateless, interpretable, and robust.

Output: price per lot, per timepoint.

### 4. Model 2: Demand-Based Dynamic Pricing
#### Demand Function:
#### Demand = α × (Occupancy / Capacity) + β × QueueLength - γ × TrafficLevel + δ × IsSpecialDay + ε × VehicleTypeWeight

#### Price Calculation:
#### NormDemand = clip((Demand - 0.5)/3, 0, 1)
#### Price = BasePrice × (1 + λ × NormDemand) (clamped between 0.5x and 2x base price)

Fully interpretable and streaming-safe.

### 5. Live Visualization
Panel+Bokeh dashboards for each lot (up to 14, each with a unique color).

Hover tooltips for all features and computed price.

Auto-updating as new data streams in.


# 📊 Live Dashboard Example
Each lot’s price evolution is shown in a real-time, interactive plot.

Up to 14 lots, each color-coded.

Hover for full feature breakdown per price point.

# 📝 Usage
### Prepare your data:
Ensure all formats are fine and sound ,timestamps etc .

### Run the Pathway pipeline:
Stream data and compute prices in real time.

### Launch the dashboard:
Monitor every lot’s price and demand signal, live.

# 📦 Extensibility & Customization
Tune model weights to fit your business logic or empirical findings.

Add new features (e.g., weather, competitor prices) by updating the schema and demand function.

### Scale to production:
Pathway’s streaming and dashboard stack is cloud-ready and supports real-time deployments.
