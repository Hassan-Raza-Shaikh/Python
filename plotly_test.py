import plotly.graph_objects as go
import numpy as np

# Define the differential equation: dy/dx = f(x, y)
# Example: dy/dx = x + y
def f(x, y):
    return x + y

# Create a grid of points
grid_size = 20
x_range = np.linspace(-3, 3, grid_size)
y_range = np.linspace(-3, 3, grid_size)
X, Y = np.meshgrid(x_range, y_range)

# Create empty lists to store the coordinates for the line segments
line_x = []
line_y = []

# Calculate the slope at each point and create the line segments
for i in range(grid_size):
    for j in range(grid_size):
        x = X[i, j]
        y = Y[i, j]
        slope = f(x, y)
        
        # Determine the length and angle of the line segment
        # We'll use a small constant length for all segments
        segment_length = 0.2
        dx = segment_length * np.cos(np.arctan(slope))
        dy = segment_length * np.sin(np.arctan(slope))

        # Add the start and end points of the line segment to the lists
        # None is used to separate individual line segments in Plotly's scatter trace
        line_x.append(x - dx / 2)
        line_x.append(x + dx / 2)
        line_x.append(None)
        
        line_y.append(y - dy / 2)
        line_y.append(y + dy / 2)
        line_y.append(None)

# Create a single Scatter trace with mode='lines'
fig = go.Figure(data=go.Scatter(
    x=line_x,
    y=line_y,
    mode='lines',
    line=dict(color='darkblue', width=1)
))

# Update the layout for a better look and feel
fig.update_layout(
    title='Interactive Slope Field for $dy/dx = x + y$',
    xaxis_title='x',
    yaxis_title='y',
    xaxis_range=[-3, 3],
    yaxis_range=[-3, 3],
    autosize=False,
    width=600,
    height=600,
    margin=dict(t=50, b=50, l=50, r=50)
)

# Show the plot
fig.show()
