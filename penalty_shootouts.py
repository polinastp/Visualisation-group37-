import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import pandas as pd
import plotly.express as px

app = dash.Dash()


if __name__ == '__main__':
    df = pd.read_csv('Dataset/WorldCupShootouts.csv')

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

    fig = px.scatter(df_zone, x='Zone_x', y='Zone_y', size='Number of Shots', size_max=70, color='Zone',
                     hover_name='Zone', hover_data=['Zone', 'Number of Shots'],
                     range_x=(0, 900), range_y=(581, 0),
                     labels={'Zone_x': '', 'Zone_y': ''},
                     title='Number of Shots - Shot Location (On Target Shots)')

    image_filename = "Image/goal.png"
    plotly_logo = base64.b64encode(open(image_filename, 'rb').read())
    fig.update_layout(xaxis_showgrid=False,
                      yaxis_showgrid=False,
                      xaxis_showticklabels=False,
                      yaxis_showticklabels=False,
                      images=[dict(
                          source='data:image/png;base64,{}'.format(plotly_logo.decode()),
                          xref="paper", yref="paper",
                          x=0, y=1,
                          sizex=1, sizey=1,
                          xanchor="left",
                          yanchor="top",
                          sizing='stretch',
                          layer="below")])

    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])
    app.run_server(debug=False)
