import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Dataset Loading - Freedom
Freedom = pd.read_csv("Cleanest_Freedom.csv")

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
                     template='simple_white')
    return fig

# Dataset Loading - Self Immolation
Selfimmo = pd.read_csv("Cleaned_selfimmo.csv")
Selfimmo = Selfimmo.rename(columns={'Incident': 'Province'})
Selfimmo = Selfimmo[Selfimmo['Year'] >= 2013]

# Layout for the entire app
app.layout = html.Div([
    html.H1("Freedom In Tibet", style={'text-align': 'center', 'font-size': '2.5em'}),
    html.Div([
        dcc.Tabs(id='tabs', value='tab-home', children=[
            dcc.Tab(label='Overview', value='tab-home'),
            dcc.Tab(label='Freedom Visualization', value='tab-freedom'),
            dcc.Tab(label='Self Immolation Visualization', value='tab-self-immolation'),
        ], vertical=True, style={'height': '100vh', 'width': '20%', 'position': 'fixed', 'font-size': '1.5em'}),
    ]),
    html.Div(id='tabs-content', style={'width': '75%', 'float': 'right', 'margin-left': '40px', 'padding-top': '20px'}),
])

# Overview content
overview_content = html.Div([
    html.H2("Overview", style={'font-size': '2em'}),
    html.P(
        "Tibet, a region situated on the Tibetan Plateau in Asia, has a rich cultural and historical heritage. Over the years, Tibet has faced significant challenges, particularly concerning political and cultural freedom, largely influenced by geopolitical issues. The complexities surrounding Tibet's freedom involve historical, cultural, and political dimensions, with global concerns about human rights violations. "
        "One of the contentious issues is China's presence in Tibet, which has led to reports of restrictions on religious practices, censorship, and limitations on cultural autonomy. The struggle for freedom and autonomy in Tibet is a global concern, drawing attention to issues of human rights and the preservation of Tibetan culture and identity.",
        style={'font-size': '1.2em'}
    ),
    html.P(
        "The international community has expressed concerns about the lack of political and cultural freedoms in Tibet, emphasizing the need for dialogue and diplomatic solutions to address these challenges. The situation in Tibet continues to evolve, with ongoing efforts to raise awareness and advocate for the protection of human rights and freedom in the region. "
        "The issue of self-immolation in Tibet is a tragic and alarming aspect of the struggle for freedom. Self-immolation involves individuals, often monks and nuns, setting themselves on fire as a form of protest against perceived injustices, restrictions on religious practices, and the suppression of Tibetan culture. These acts are extreme and desperate measures to draw attention to the challenges faced by Tibetans.",
        style={'font-size': '1.2em'}
    ),
    html.P(
        "The self-immolation incidents have been concentrated in Tibetan areas and are often linked to grievances against Chinese policies. The individuals who undertake self-immolation often leave behind messages expressing their concerns about freedom, human rights abuses, and the desire for cultural and religious autonomy. "
        "The international community has responded to these incidents with expressions of concern and calls for a peaceful resolution to the issues facing Tibet. These acts of self-immolation highlight the severity of the challenges faced by Tibetans and the urgency of addressing underlying causes to ensure the protection of human rights and freedom in the region.",
        style={'font-size': '1.2em'}
    ),
    html.Div([
        html.Img(src="/assets/Tibet_map.png", style={'width': '45%', 'display': 'inline-block'}),
        html.Img(src="/assets/selfimmo.png", style={'width': '45%', 'display': 'inline-block', 'margin-left': '10px'}),
    ], style={'text-align': 'center'}),
])

# Define callback to update the content based on the selected tab
@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def update_tab(selected_tab):
    if selected_tab == 'tab-home':
        return overview_content
    elif selected_tab == 'tab-freedom':
        return html.Div([
            html.H2("Freedom In Tibet Visualization", style={'font-size': '2em'}),
            html.P(
                "Explore visualizations related to freedom in Tibet. The graphs provide insights into scores, trends, "
                "and comparisons among countries. Use the dropdown to select the year of interest.",
                style={'font-size': '1.2em'}
            ),
            dcc.Dropdown(
                id='year-dropdown-freedom',
                options=[{'label': str(year), 'value': year} for year in Freedom['Year'].unique()],
                value=Freedom['Year'].max(),
                multi=False,
                style={'width': '50%', 'font-size': '1.2em'}
            ),
            dcc.Graph(id='freedom-scatter-plot'),
            dcc.Graph(id='freedom-line-plot'),
            dcc.Graph(id='border-issues-line-plot'),
        ])
    elif selected_tab == 'tab-self-immolation':
        return html.Div([
            html.H2("Self Immolation Incidents Visualization", style={'font-size': '2em'}),
            html.P(
                "Explore visualizations related to self-immolation incidents in Tibet. The graphs provide insights into "
                "incidents by province, age group, and monk status. Use the dropdown to select the year of interest.",
                style={'font-size': '1.2em'}
            ),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year} for year in Selfimmo['Year'].unique()],
                value=Selfimmo['Year'].max(),
                multi=False,
                style={'width': '50%', 'font-size': '1.2em'}
            ),
            dcc.Graph(id='bar-by-province'),
            dcc.Graph(id='bar-by-age-group'),
            dcc.Graph(id='bar-by-monk_status'),
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
                       template='simple_white')
    border_issues_fig = px.line(border_issues, x='Year', y='Total', color='Country/Territory',
                                title='Countries Related to Border Issues Over Time',
                                labels={'Total': 'Total Score', 'Country/Territory': 'Country/Territory'},
                                template='simple_white')
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
                  template='simple_white')
    fig2 = px.bar(filtered_data, x='age_groups', color='Gender', facet_col='Year',
                  title=f'Number of Incidents by Age Group and Gender in {selected_year}',
                  labels={'age_groups': 'Age Group', 'Gender': 'Gender'},
                  template='simple_white')
    fig3 = px.bar(filtered_data, x='Monk_Status', color='Monk_Status',
                  title=f'Number of Incidents by Monks vs Non Monks in {selected_year}',
                  labels={'Monk_Status': 'Monk Status'},
                  template='simple_white')

    return fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
