import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from collections import Counter

darkly = 'https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/darkly/bootstrap.min.css'
app = dash.Dash(__name__, external_stylesheets= [darkly])

# import data
df = pd.read_csv('Twitter_Vaccine.csv')

# get the counts of positive, negative, and neutral tweets for the line graph
unique_dates = df['Dates'].unique()
pos, neg, neut = [],[],[]
for date in unique_dates:
  dff = df.copy()
  dff = dff[dff['Dates'] == date]
  n = len(dff)
  pos.append(sum(dff['Label'] == 'Positive')/n)
  neg.append(sum(dff['Label'] == 'Negative')/n)
  neut.append(sum(dff['Label'] == 'Neutral')/n)
data = {'Positive': pos, 'Negative': neg, 'Neutral': neut, 'Dates': unique_dates}
new_df = pd.DataFrame(data)

# create overall line plot
fig = px.line(new_df, x = 'Dates', y = ['Positive','Negative','Neutral'], color_discrete_map = {'Positive':'green','Negative':'red','Neutral':'blue'})
fig.update_layout(title = 'Change in Sentiment Over Time',
    yaxis_title = "Percent of Tweets")


app.layout = html.Div([
    dbc.Row(
        [dbc.Col(html.H1('Twitter Sentiment Analysis for Covid-19 Vaccine', style = {'text align':'center'}), width = 6),
        dbc.Col(dcc.Dropdown(id = 'select_date',
                                    options = [
                                               {'label':'12/14/2020','value':'12/14/2020'},
                                               {'label':'12/15/2020','value':'12/15/2020'},
                                               {'label':'12/16/2020','value':'12/16/2020'},
                                               {'label':'12/17/2020','value':'12/17/2020'},
                                               {'label':'12/18/2020','value':'12/18/2020'},
                                               {'label':'12/19/2020','value':'12/19/2020'},
                                               {'label':'12/20/2020','value':'12/20/2020'},
                                               {'label':'12/21/2020','value':'12/21/2020'},
                                               {'label':'12/22/2020','value':'12/22/2020'},
                                    ],
                                    value = '12/14/2020',
                                    style = {'color': '#212121'}))
                                    ]),
    dbc.Row(
        [dbc.Col(dcc.Graph(id = 'bar_plot', figure = {}), width = 6),
        dbc.Col(dcc.Graph(id = 'scatter_plot', figure = {}), width = 6)
        ]),
    html.Br(),
    dbc.Row(
        [dbc.Col(dcc.Graph(id = 'line_plot', figure = fig))
        ])
])

@app.callback(
    [Output(component_id = 'bar_plot', component_property = 'figure'),
    Output(component_id = 'scatter_plot', component_property = 'figure')],
    [Input(component_id = 'select_date', component_property = 'value')]
)
def update_graph(option_selected):
    # copy df and filter by date selected
    dff = df.copy()
    dff = dff[dff['Dates'] == option_selected]

    # get the frequencies of positive, negative, and neutral tweets
    pos = sum(dff['Label'] == 'Positive')
    neg = sum(dff['Label'] == 'Negative')
    neut = sum(dff['Label'] == 'Neutral')
    data = {'Label': ['Negative','Neutral','Positive'], 'Counts': [neg,neut,pos]}
    new_df = pd.DataFrame(data)

    # create a bar plot
    fig1 = px.bar(new_df, x = 'Label', y = 'Counts', color = 'Label', color_discrete_map = {'Positive':'green','Negative':'red','Neutral':'blue'})
    fig1.update_layout(
        title = 'Number of Negative, Neutral, and Positive tweets for {}'.format(option_selected),
        xaxis_title = "Polarity Label",
        yaxis_title = "Number of Tweets"
    )

    # create scatter plot
    fig2 = px.scatter(dff, x = 'Polarity', y = 'Subjectivity', color = 'Label', color_discrete_map = {'Positive':'green','Negative':'red','Neutral':'blue'})
    fig2.update_layout(
        title = 'Visualizing Polarity versus Subjectivity of Tweets for {}'.format(option_selected),
    )

    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)