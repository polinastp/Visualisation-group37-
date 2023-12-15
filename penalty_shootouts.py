import numpy as np
import pandas as pd
import seaborn as sns
import plotly as py
import plotly_express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt
import folium
from folium import plugins


from plotly.offline import iplot
import os
import base64



# from plotly.offline import init_notebook_mode, iplot
import os
import base64

# from plotly.offline import init_notebook_mode, iplot
import os
import base64

df = pd.read_csv('FIFA DataSet/Data/FIFA World Cup Penalty Shootouts/WorldCupShootouts.csv')


def show_shots(df, x, y, size, size_max, hover_name, hover_data, color, title):
    fig = px.scatter(df,
                     x=x,
                     y=y,
                     size=size,
                     size_max=size_max,
                     color=color,
                     hover_name=hover_name,
                     hover_data=hover_data,
                     range_x=(0, 900),
                     range_y=(581, 0),
                     width=900,
                     height=581,
                     labels={x: '', y: ''})

    image_filename = "Image/goal.png"
    plotly_logo = base64.b64encode(open(image_filename, 'rb').read())
    fig.update_layout(xaxis_showgrid=False,
                      yaxis_showgrid=False,
                      xaxis_showticklabels=False,
                      yaxis_showticklabels=False,
                      title=title,
                      images=[dict(
                          source='data:image/png;base64,{}'.format(plotly_logo.decode()),
                          xref="paper", yref="paper",
                          x=0, y=1,
                          sizex=1, sizey=1,
                          xanchor="left",
                          yanchor="top",
                          sizing='stretch',
                          layer="below")])
    fig.show()


shot_coords = {
    1: [216, 150],
    2: [448, 150],
    3: [680, 150],
    4: [216, 250],
    5: [448, 250],
    6: [680, 250],
    7: [216, 350],
    8: [448, 350],
    9: [680, 350]
}

df_target = df[df.OnTarget == 1]

df_target['Zone_x'] = df_target['Zone'].apply(lambda x: shot_coords[int(x)][0])
df_target['Zone_y'] = df_target['Zone'].apply(lambda x: shot_coords[int(x)][1])

df_zone = pd.DataFrame(df_target.groupby(['Zone', 'Zone_x', 'Zone_y']).size()).reset_index()
df_zone.rename(columns={0: 'Number of Shots'}, inplace=True)

show_shots(df_zone, 'Zone_x', 'Zone_y', 'Number of Shots', 70, 'Zone', ['Zone', 'Number of Shots'], 'Number of Shots',
           'Shot Location (On Target Shots)')
