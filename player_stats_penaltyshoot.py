import dash
from dash import dcc, html, Dash
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

# read csv files into dataframes
df1 = pd.read_csv('Dataset/player_shooting.csv')
df2 = pd.read_csv('Dataset/player_defense.csv')
df3 = pd.read_csv('Dataset/player_possession.csv')
df4 = pd.read_csv('Dataset/player_passing.csv')

# select specific columns from each dataframe
cols_df1 = ['player', 'team', 'position', 'age', 'shots', 'goals']
cols_df2 = ['player', 'tackles', 'blocks']
cols_df3 = ['player', 'touches', 'passes_received']
cols_df4 = ['player', 'passes', 'assists']

# merge dataframes 
merged_df = pd.merge(df1[cols_df1], df2[cols_df2], on='player', how='right')
merged_df = pd.merge(merged_df, df3[cols_df3], on='player', how='right')
merged_df = pd.merge(merged_df, df4[cols_df4], on='player', how='right')

# cleaning of the dataframe from null values by filling in with 0 
df = merged_df.fillna(0)
df_st = df.copy()

# 
df_st['shots']=(df_st['shots']-df_st['shots'].min())/(df_st['shots'].max()-df_st['shots'].min())
df_st['passes']=(df_st['passes']-df_st['passes'].min())/(df_st['passes'].max()-df_st['passes'].min())
df_st['goals']=(df_st['goals']-df_st['goals'].min())/(df_st['goals'].max()-df_st['goals'].min())
df_st['tackles']=(df_st['tackles']-df_st['tackles'].min())/(df_st['tackles'].max()-df_st['tackles'].min())
df_st['touches']=(df_st['touches']-df_st['touches'].min())/(df_st['touches'].max()-df_st['touches'].min())
df_st['passes_received']=(df_st['passes_received']-df_st['passes_received'].min())/(df_st['passes_received'].max()-df_st['passes_received'].min())
df_st['blocks']=(df_st['blocks']-df_st['blocks'].min())/(df_st['blocks'].max()-df_st['blocks'].min())
df_st['assists']=(df_st['assists']-df_st['assists'].min())/(df_st['assists'].max()-df_st['assists'].min())


df_x = pd.read_csv('Dataset/WorldCupShootouts.csv')
df_x = df_x.dropna()
df_vis2 = df_x.copy()
df_vis2['Number of goals'] = 1
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
df_target = df_x[df_x.OnTarget == 1]
df_target['Zone_x'] = df_target['Zone'].apply(lambda x: shot_coords[int(x)][0])
df_target['Zone_y'] = df_target['Zone'].apply(lambda x: shot_coords[int(x)][1])

df_zone = pd.DataFrame(df_target.groupby(['Zone', 'Zone_x', 'Zone_y']).size()).reset_index()
df_zone.rename(columns={0: 'Number of Shots Scored'}, inplace=True)

#Df for OffTarget shots for every zone (Shots that didnt result in a goal)
df_Offtarget = df_x[df_x.OnTarget == 0]
df_Offtarget['Zone_x'] = df_Offtarget['Zone'].apply(lambda x: shot_coords[int(x)][0])
df_Offtarget['Zone_y'] = df_Offtarget['Zone'].apply(lambda x: shot_coords[int(x)][1])

df_zone1 = pd.DataFrame(df_Offtarget.groupby(['Zone','Zone_x', 'Zone_y']).size()).reset_index()
df_zone1.rename(columns = {0:'Number of OffShots'}, inplace= True)

#Merging the columns with number of Shots made versus number of shots missed on df_zone
#THE df_zone1 has no values for zone 5 and 8 because all the shots made in that zone was successful and thus there is no data for the unsuccessful shots for that particular zone
# df_zone = pd.merge(df_zone, df_zone1[['Zone', 'Number of OffShots']], on="Zone")

# Figure for On target Shots
fig1 = px.scatter(df_zone, x='Zone_x', y='Zone_y', color='Number of Shots Scored', hover_data=['Number of Shots Scored'],
                 range_x=(0, 900), range_y=(750, 0),
                 labels={'Zone_x': '', 'Zone_y': ''},
                 title='Goals Made Per Zone', color_continuous_scale='reds')

fig1.update_traces(marker={'size': 45})

image_filename = "Image/goal.png"
plotly_logo = base64.b64encode(open(image_filename, 'rb').read())
fig1.update_layout(xaxis_showgrid=False,
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

# initialising the app 
app = dash.Dash(__name__)

# creating categories for the radar graph 
categories = ['shots', 'goals', 'tackles', 'blocks', 'touches', 'passes_received', 'passes', 'assists']

# creating figure 
fig = go.Figure()

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )),
    showlegend=False
)

app.layout = html.Div([html.Div([
    html.H5("Visualization Project Group 37", style={"fontSize": 20}),
    html.Div(id="intro", children="This Dashboard helps coaches and players of the upcoming World Cup 2026."),
    html.Hr(style={'margin-top': '5px', 'margin-bottom': '15px'}),  # Add a horizontal line
    html.Div([
        html.P("Select two teams for comparison", style={'font-weight': 'bold'}),
        dcc.Dropdown(id='teamA_dd',
                     options=[{'label': team, 'value': team} for team in df['team'].unique()],
                     ),
        dcc.Dropdown(id='teamB_dd',
                     options=[{'label': team, 'value': team} for team in df['team'].unique()],
                     ),
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'middle'}),
    dcc.Graph(id='spider', figure=fig, style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'middle'}),

    html.Div([
        html.P("Select the attributes for comparison", style={'font-weight': 'bold'}),
        dcc.Checklist(id='attribute_checklist',
                      options=[{'label': attr, 'value': attr} for attr in categories]
                      ),
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'middle'}),
    dcc.Graph(id='violin_plot', figure=fig, style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'middle'}),
    html.Div([
        html.P("Select the team", style={'font-weight': 'bold'}),
        dcc.Dropdown(id='mydropdown',
                 options=[{'label': team, 'value': team} for team in df_x['Team'].unique()],
                 value='FRA'),
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'middle'}),
    dcc.Graph(id="myfig", figure=fig, style={'width': '80%', 'display': 'inline-block', 'verticalAlign': 'middle'}),
    html.Div(style={'width': '20%', 'display': 'inline-block'}),
    dcc.Graph(id="bar_chart", style={'width': '80%', 'display': 'inline-block'}),
])
])


# Callback function for spider plots
@app.callback(
    Output('spider', 'figure'), #Output('titel', 'value'),
    [Input('teamA_dd', 'value'), Input('teamB_dd', 'value')]
)
def update_radar_chart(selected_teamA, selected_teamB):
    teamA_data = df_st[df_st['team'] == selected_teamA]
    teamB_data = df_st[df_st['team'] == selected_teamB]

    # team A  mean statistics  
    avg_passesA = teamA_data['passes'].mean()
    avg_goalsA = teamA_data['goals'].mean()
    avg_shotsA = teamA_data['shots'].mean()
    avg_tacklesA = teamA_data['tackles'].mean()
    avg_blocksA = teamA_data['blocks'].mean()
    avg_touchesA = teamA_data['touches'].mean()
    avg_assistsA = teamA_data['assists'].mean()
    avg_rec_passesA = teamA_data['passes_received'].mean()

    # team B mean statistics 
    avg_passesB = teamB_data['passes'].mean()
    avg_goalsB = teamB_data['goals'].mean()
    avg_shotsB = teamB_data['shots'].mean()
    avg_tacklesB = teamB_data['tackles'].mean()
    avg_blocksB = teamB_data['blocks'].mean()
    avg_touchesB = teamB_data['touches'].mean()
    avg_assistsB = teamB_data['assists'].mean()
    avg_rec_passesB = teamB_data['passes_received'].mean()

    # creating figure 
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[avg_shotsA, avg_goalsA, avg_tacklesA, avg_blocksA, avg_touchesA, avg_rec_passesA, avg_passesA, avg_assistsA],
        theta=categories,
        fill='toself',
        line_color='blue',
        marker_color='lightblue',
        name=f'{selected_teamA}'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[avg_shotsB, avg_goalsB, avg_tacklesB, avg_blocksB, avg_touchesB, avg_rec_passesB, avg_passesB, avg_assistsB],
        theta=categories,
        fill='toself',
        line_color='orange',
        marker_color='lightcoral',
        name=f'{selected_teamB}'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            )
        ),
        title=dict(
            text='Radar Chart for comparison of different attributes amongst two teams',
            font=dict(
                size=18,
                color='black',
            ),
            x=0.5,
        ),
        showlegend=True,
    )

    return fig

# Callback function for violin plots
@app.callback(
    Output('violin_plot', 'figure'),
    [Input('teamA_dd', 'value'), Input('teamB_dd', 'value'), Input('attribute_checklist', 'value')]
)
def update_violin_plot(selected_teamA, selected_teamB, selected_attributes):
    if not selected_attributes:
        empty_fig = make_subplots(rows=1, cols=1)
        empty_fig.update_layout(
            title=dict(
                text='Violin plots of selected attributes',
                font=dict(
                    size=18,
                    color='black',
                ),
                x=0.5,
            ),
            yaxis=dict(title='Attribute Value'),
            showlegend=False,
        )
        return empty_fig

    teamA_data = df[df['team'] == selected_teamA]
    teamB_data = df[df['team'] == selected_teamB]

    fig2 = make_subplots(rows=1, cols=len(selected_attributes), subplot_titles=selected_attributes)

    for i, attribute in enumerate(selected_attributes, start=1):
        fig2.add_trace(go.Violin(
            x=[selected_teamA] * len(teamA_data),
            y=teamA_data[attribute],
            box_visible=True,
            line_color='blue',
            name=f'Team A - {attribute}',
            marker_color='lightblue'
        ), row=1, col=i)

        fig2.add_trace(go.Violin(
            x=[selected_teamB] * len(teamB_data),
            y=teamB_data[attribute],
            box_visible=True,
            line_color='orange',
            name=f'Team B - {attribute}',
            marker_color='lightcoral'
        ), row=1, col=i)

    fig2.update_layout(
        title=dict(
            text='Violin plots of selected attributes',
            font=dict(
                size=18,
                color='black',
            ),
            x=0.5,
        ),
        yaxis=dict(title='Attribute Value'),
        showlegend=False,
        width=len(selected_attributes) * 500
    )

    return fig2

@app.callback(Output("myfig", 'figure'),
              [Input('mydropdown', 'value')])
def update_plot(selected_team):
    filtered_df = df_x[df_x['Team'] == selected_team]
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
                              title=dict(
                                  text=f'Goals Made per Zone By - {selected_team}',
                                  font=dict(
                                      size=18,
                                      color='black',
                                  ),
                                  x=0.5
                              ),
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

@app.callback(
    Output('bar_chart', 'figure'),
    [Input('mydropdown', 'value')])
def update_bar_chart(selected_team):
    team_data = df_vis2[df_vis2['Team'] == selected_team]
    df_bar = pd.DataFrame(team_data.groupby('Zone')['Number of goals'].sum().reset_index())

    fig2 = px.bar(df_bar, x='Zone', y='Number of goals')

    fig2.update_layout(
        title=dict(
            text=f'Bar Chart of Number of goals per zone by - {selected_team}',
            font=dict(
                size=18,
                color='black',
            ),
            x=0.5
        ))

    return fig2

# run the app
if __name__ == '__main__':
    app.run_server(debug=False)