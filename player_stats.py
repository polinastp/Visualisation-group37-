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

app.layout = html.Div([
    dcc.Graph(id='spider', figure=fig),
    html.Label('Team A:', style={'font-weight': 'bold'}),
    dcc.Dropdown(id='teamA_dd',
                 options=[{'label': team, 'value': team} for team in df['team'].unique()],
                 ),
    html.Label('Team B:', style={'font-weight': 'bold'}),
    dcc.Dropdown(id='teamB_dd',
                 options=[{'label': team, 'value': team} for team in df['team'].unique()],
                 ),
    html.Label('Select attributes for violin plots:', style={'font-weight': 'bold'}),
    dcc.Checklist(
        id='attribute_checklist',
        options=[{'label': attr, 'value': attr} for attr in categories],
                 ),
    dcc.Graph(id='violin_plot')
])

# Callback function for spider plots
@app.callback(
    Output('spider', 'figure'),
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
        name='Team A'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[avg_shotsB, avg_goalsB, avg_tacklesB, avg_blocksB, avg_touchesB, avg_rec_passesB, avg_passesB, avg_assistsB],
        theta=categories,
        fill='toself',
        line_color='orange',
        marker_color='lightcoral',
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
    if not selected_attributes:
        return make_subplots(rows=1, cols=1)

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
        title='Violin plots for selected attributes',
        xaxis=dict(title='Team'),
        yaxis=dict(title='Attribute Value'),
        showlegend=True,
        width=len(selected_attributes) * 500
    )

    return fig2


# run the app
if __name__ == '__main__':
    app.run_server(debug=False)
