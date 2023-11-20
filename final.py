import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Dataset Loading - Freedom
Freedom = pd.read_csv("/Users/dhekha/PycharmProjects/Programming_Language/Freedom_in_Tibet/Cleanest_Freedom.csv")

border_issues = Freedom[Freedom['Country/Territory'].isin(["Philippines", "Vietnam", "Japan", "Nepal", "Bhutan",
                                                           "India", "Indonesia", "Malaysia", "Laos", "South Korea",
                                                           "North Korea", "Mongolia", "Myanmar", "Tibet", "Singapore",
                                                           "Brunei"])]

# Function to create an interactive plot with Plotly
def create_plotly_plot(year_filter):
    filtered_data = Freedom.query(f"Year == {year_filter}").nsmallest(10, 'Total')

    fig = px.scatter(filtered_data, x='Country/Territory', y='Total', color='Status',
                     title=f'Lowest 10 countries in {year_filter}',
                     labels={'Total': 'Total Score', 'Country/Territory': 'Country/Territory'},
                     template='plotly_dark')
    return fig

# Dataset Loading - Self Immolation
Selfimmo = pd.read_csv("/Users/dhekha/PycharmProjects/Programming_Language/Freedom_in_Tibet/Cleanest_selfimmo.csv")
Selfimmo = Selfimmo.rename(columns={'Incident': 'Province'})
Selfimmo = Selfimmo[Selfimmo['Year'] >= 2013]

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Layout for both visualizations on one page
app.layout = html.Div(style={'color': 'black', 'padding': '10px', 'text-align': 'center'}, children=[
    html.H1("Combined Visualization Dashboard"),

    # Section for Freedom in Tibet Visualization
    html.Div([
        dcc.Dropdown(
            id='year-dropdown-freedom',
            options=[{'label': str(year), 'value': year} for year in Freedom['Year'].unique()],
            value=Freedom['Year'].max(),  # Set the initial value to the latest year
            multi=False,
            style={'width': '50%'}
        ),
        dcc.Graph(id='freedom-scatter-plot'),
        dcc.Graph(id='freedom-line-plot'),
        dcc.Graph(id='border-issues-line-plot'),
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

    # Section for Self Immolation Incidents Visualization
    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in Selfimmo['Year'].unique()],
            value=Selfimmo['Year'].max(),  # Set the initial value to the latest year
            multi=False,
            style={'width': '50%'}
        ),
        html.Div([
            dcc.Graph(id='bar-by-province'),
            dcc.Graph(id='bar-by-age-group'),
        ], style={'display': 'flex'}),
        html.Div([
            dcc.Graph(id='bar-by-monk_status'),
            dcc.Graph(id='bar-by-current_status'),
        ], style={'display': 'flex'}),
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
])

# Callbacks to update graphs based on the selected year for Freedom page
@app.callback(
    [Output('freedom-scatter-plot', 'figure'),
     Output('freedom-line-plot', 'figure'),
     Output('border-issues-line-plot', 'figure')],
    [Input('year-dropdown-freedom', 'value')]
)
def update_graphs_freedom(selected_year):
    scatter_fig = create_plotly_plot(selected_year)
    set_lowest_10 = Freedom.query(f"Year == {selected_year}").nsmallest(10, 'Total')
    top_10_countries = set_lowest_10['Country/Territory']
    line_graph = Freedom[Freedom['Country/Territory'].isin(top_10_countries)]
    line_fig = px.line(line_graph, x='Year', y='Total', color='Country/Territory',
                       title='Lowest 10 Countries Over Time',
                       labels={'Total': 'Total Score', 'Country/Territory': 'Country/Territory'},
                       template='plotly_dark')
    border_issues_fig = px.line(border_issues, x='Year', y='Total', color='Country/Territory',
                                title='Countries Related to Border Issues Over Time',
                                labels={'Total': 'Total Score', 'Country/Territory': 'Country/Territory'},
                                template='plotly_dark')
    return scatter_fig, line_fig, border_issues_fig

# Callbacks to update graphs based on the selected year for Self Immolation page
@app.callback(
    [Output('bar-by-province', 'figure'),
     Output('bar-by-age-group', 'figure'),
     Output('bar-by-monk_status', 'figure')],
    [Input('year-dropdown', 'value')])
def update_graphs(selected_year):
    filtered_data = Selfimmo[Selfimmo['Year'] == selected_year]
    fig1 = px.bar(filtered_data, x='Province', color='Province',
                  title=f'Incidents by Province in {selected_year}',
                  labels={'Province': 'Province', 'Year': 'Year'},
                  template='plotly_dark')
    fig2 = px.bar(filtered_data, x='age_groups', color='Gender', facet_col='Year',
                  title=f'Number of Incidents by Age Group and Gender in {selected_year}',
                  labels={'age_groups': 'Age Group', 'Gender': 'Gender'},
                  template='plotly_dark')
    fig3 = px.bar(filtered_data, x='Monk_Status', color='Monk_Status',
                  title=f'Number of Incidents by Monks vs Non Monks in {selected_year}',
                  labels={'Monk_Status': 'Monk Status'},
                  template='plotly_dark')

    return fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
