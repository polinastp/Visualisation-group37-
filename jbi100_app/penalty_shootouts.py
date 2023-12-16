import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import pandas as pd
import plotly.express as px

df = pd.read_csv('Dataset/WorldCupShootouts.csv')
df = df.dropna()

shot_coords = {
    1: [216, 250],
    2: [448, 250],
    3: [680, 250],
    4: [216, 450],
    5: [448, 450],
    6: [680, 450],
    7: [216, 690],
    8: [448, 690],
    9: [680, 690]
}

#Df for OnTarget Shots for every zone (Goals)
df_target = df[df.OnTarget == 1]
df_target['Zone_x'] = df_target['Zone'].apply(lambda x: shot_coords[int(x)][0])
df_target['Zone_y'] = df_target['Zone'].apply(lambda x: shot_coords[int(x)][1])

df_zone = pd.DataFrame(df_target.groupby(['Zone', 'Zone_x', 'Zone_y']).size()).reset_index()
df_zone.rename(columns={0: 'Number of Shots Scored'}, inplace=True)

#Df for OffTarget shots for every zone (Shots that didnt result in a goal)
df_Offtarget = df[df.OnTarget == 0]
df_Offtarget['Zone_x'] = df_Offtarget['Zone'].apply(lambda x: shot_coords[int(x)][0])
df_Offtarget['Zone_y'] = df_Offtarget['Zone'].apply(lambda x: shot_coords[int(x)][1])

df_zone1 = pd.DataFrame(df_Offtarget.groupby(['Zone','Zone_x', 'Zone_y']).size()).reset_index()
df_zone1.rename(columns = {0:'Number of OffShots'}, inplace= True)

#Merging the columns with number of Shots made versus number of shots missed on df_zone
#THE df_zone1 has no values for zone 5 and 8 because all the shots made in that zone was successful and thus there is no data for the unsuccessful shots for that particular zone
# df_zone = pd.merge(df_zone, df_zone1[['Zone', 'Number of OffShots']], on="Zone")

# Figure for On target Shots
fig = px.scatter(df_zone, x='Zone_x', y='Zone_y', color='Number of Shots Scored', hover_data=['Number of Shots Scored'],
                 range_x=(0, 900), range_y=(750, 0),
                 labels={'Zone_x': '', 'Zone_y': ''},
                 title='Goals Made Per Zone', color_continuous_scale='reds')

fig.update_traces(marker={'size': 45})

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
                      sizex=1, sizey=1.5,
                      xanchor="left",
                      yanchor="top",
                      sizing='stretch',
                      layer="below")])




#Creating Dashboard
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="myfig", figure=fig),
    dcc.Dropdown(id='mydropdown',
                 options=[{'label': team, 'value': team} for team in df['Team'].unique()],
                 value='FRA')
])


@app.callback(Output("myfig", 'figure'),
              [Input('mydropdown', 'value')])
def update_plot(selected_team):
    filtered_df = df[df['Team'] == selected_team]
    df_target = filtered_df[filtered_df.OnTarget == 1]
    df_target['Zone_x'] = df_target['Zone'].apply(lambda x: shot_coords[int(x)][0])
    df_target['Zone_y'] = df_target['Zone'].apply(lambda x: shot_coords[int(x)][1])

    df_zone = pd.DataFrame(df_target.groupby(['Zone', 'Zone_x', 'Zone_y']).size()).reset_index()
    df_zone.rename(columns={0: 'Number of Shots Scored'}, inplace=True)

    updated_fig = px.scatter(df_zone, x='Zone_x', y='Zone_y', color='Number of Shots Scored',
                             hover_data=['Number of Shots Scored'],
                             range_x=(0, 900), range_y=(750, 0),
                             labels={'Zone_x': '', 'Zone_y': ''},
                             title=f'Goals Made per Zone By - {selected_team}', color_continuous_scale='reds')

    updated_fig.update_traces(marker={'size': 45})
    updated_fig.update_layout(xaxis_showgrid=False,
                              yaxis_showgrid=False,
                              xaxis_showticklabels=False,
                              yaxis_showticklabels=False,
                              images=[dict(
                                  source='data:image/png;base64,{}'.format(plotly_logo.decode()),
                                  xref="paper", yref="paper",
                                  x=0, y=1,
                                  sizex=1, sizey=1.5,
                                  xanchor="left",
                                  yanchor="top",
                                  sizing='stretch',
                                  layer="below")])

    return updated_fig


if __name__ == '__main__':
    app.run_server(debug=False)
