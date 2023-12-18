import dash
from dash import dcc, html, Dash
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

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

# 
df['shots']=(df['shots']-df['shots'].min())/(df['shots'].max()-df['shots'].min())
df['passes']=(df['passes']-df['passes'].min())/(df['passes'].max()-df['passes'].min())
df['goals']=(df['goals']-df['goals'].min())/(df['goals'].max()-df['goals'].min())
df['tackles']=(df['tackles']-df['tackles'].min())/(df['tackles'].max()-df['tackles'].min())
df['touches']=(df['touches']-df['touches'].min())/(df['touches'].max()-df['touches'].min())
df['passes_received']=(df['passes_received']-df['passes_received'].min())/(df['passes_received'].max()-df['passes_received'].min())
df['blocks']=(df['blocks']-df['blocks'].min())/(df['blocks'].max()-df['blocks'].min())
df['assists']=(df['assists']-df['assists'].min())/(df['assists'].max()-df['assists'].min())

# initialising the app 
app = dash.Dash(__name__)

# creating categories for the radar graph 
categories = ['shots', 'goals', 'tackles', 'blocks', 'touches', 'received passes', 'passes', 'assists']

# creating figure 
fig = go.Figure()

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )),
    showlegend=False
)

app.layout = html.Div([
    dcc.Graph(id='spider', figure=fig),
    html.Label('Team A:'),
    dcc.Dropdown(id='teamA_dd',
                 options=[{'label': team, 'value': team} for team in df['team'].unique()],
                 ),
    html.Label('Team B:'),
    dcc.Dropdown(id='teamB_dd',
                 options=[{'label': team, 'value': team} for team in df['team'].unique()],
                 ),
    html.Label('Select attributes for violin plots:'),
    dcc.Checklist(
        id='attribute_checklist',
        options=[{'Label': attr, 'value': attr} for attr in categories],
        value=categories
    ),
    dcc.Graph(id='violin_plot')
])

# Callback function for spider plots
@app.callback(
    Output('spider', 'figure'),
    [Input('teamA_dd', 'value'), Input('teamB_dd', 'value')]
)
def update_radar_chart(selected_teamA, selected_teamB):
    teamA_data = df[df['team'] == selected_teamA]
    teamB_data = df[df['team'] == selected_teamB]

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
        name='Team A'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[avg_shotsB, avg_goalsB, avg_tacklesB, avg_blocksB, avg_touchesB, avg_rec_passesB, avg_passesB, avg_assistsB],
        theta=categories,
        fill='toself',
        name='Team B'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            )),
        showlegend=False
    )
    return fig

# Callback function for violin plots
@app.callback(
    Output('violin_plot', 'figure'),
    [Input('teamA_dd', 'value'), Input('teamB_dd', 'value'), Input('attribute_checklist', 'value')]
)
def update_violin_plot(selected_teamA, selected_teamB, selected_attributes):
    teamA_data = df[df['team'] == selected_teamA]
    teamB_data = df[df['team'] == selected_teamB]

    fig2 = go.Figure()
    for attribute in selected_attributes:



    return fig2


# run the app
if __name__ == '__main__':
    app.run_server(debug=False)
