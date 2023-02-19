import pandas as pd
import dash
from dash import dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
from dash import html
import dash_bootstrap_components as dbc
import datetime as dt



df_time_based_info = pd.read_csv('time_based_video_data_.csv')
df = pd.read_csv('video_data.csv')
external_stylesheets = [dbc.themes.ZEPHYR]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Div(html.H4('METRICS OF YOUTUBE CHANNELS'),
                     ), width={'size': 3}, style={'margin-left': '20px',
                                                  'margin-top': '10px'}
        ),
        dbc.Col(
            html.Div([
                dcc.DatePickerRange(
                    start_date=df_time_based_info['date'].min(),
                    end_date=df_time_based_info['date'].max(),
                    id='date_selector',
                    display_format='DD-MM-YYYY'),

            ]), width={'size': 3}, className='component-style'
        ),
        dbc.Col([
            html.Div([dcc.Dropdown(
                    options=[{'label': x, 'value': x} for x in df['title'].unique()],
                    value='Служебное огнестрельное оружие в работе охранника. Травмат. | дудл видео для бизнеса',
                    placeholder="Select a video",
                    id='title_selector',
                    multi=False,
                    className='component-style'
                        ),
            ])
        ]),
    dbc.Row([
        dbc.Col([
                html.Div([dcc.Graph(id='views', className='indicator-style')],
                         ),

                ], width={'size': 3}
                ),
        dbc.Col(html.Div([dcc.Graph(id='hours', className='indicator-style'),
                          ],
                         ),
                width={'size': 2}
                ),
        dbc.Col(html.Div([dcc.Graph(id='likes', className='indicator-style'),
                          ],
                         ),
                width={'size': 2}
                ),
        dbc.Col(html.Div([dcc.Graph(id='subscribers', className='indicator-style'),
                          ],
                         ),
                width={'size': 2}
                ),
        dbc.Col(html.Div([dcc.Graph(id='card_clicks', className='indicator-style'),
                          ]
                         ),
                width={'size': 3}
                ),
    ], className={}
                ),
    dbc.Row([dcc.Graph(id='plot')]),

    dbc.Row([
            dbc.Col([
                html.Div([dcc.Graph(id='funnel', config={'displayModeBar': False})],
                         ),
                    ], width={'size': 6}
                ),
            dbc.Col([
                    html.Div([
                        dbc.Row([
                            dbc.Card(
                                dbc.CardBody([
                                    html.Div("Attention", style={
                                        'background-color': '#1ca087',
                                        'text-align': 'center',
                                        'font-size': '30px',
                                    }),
                                    html.Div([dcc.Graph(id='views_difference', className='card-style')]),
                                            ])
                            ), ]),
                        dbc.Row([
                            dbc.Card(
                                dbc.CardBody([
                                    html.Div("Interest", style={
                                        'background-color': '#5cae5d',
                                        'text-align': 'center',
                                        'font-size': '30px',
                                    }),
                                    html.Div([dcc.Graph(id='hours_difference', className='card-style')]),
                                    html.Div(children=[html.H4("Total Watch Time hours"),
                                                       html.H4(id='total_watch_time')], className='card-div'),
                                    html.Div(children=[html.H4("Average Watch Time"),
                                                       html.H4(id='average_watch_time')], className='card-div'),
                                    html.Div(children=[html.H4("Likes/Views %"),
                                                       html.H4(id='likes_ratio')], className='card-div')
                                ]),
                            )]),
                        dbc.Row(
                            [dbc.Card(
                                dbc.CardBody([
                                    html.Div("Desire", style={
                                        'background-color': '#a8b223',
                                        'text-align': 'center',
                                        'font-size': '30px',
                                    }),
                                    html.Div([dcc.Graph(id='subscribers_gained', className='card-style')]),
                                    html.Div(children=[html.H4("Subscribers/Views %"),
                                                       html.H4(id='subscribers_views')], className='card-div'),
                                    html.Div(children=[html.H4("Comments/Views %"),
                                                       html.H4(id='comments_views')], className='card-div'),
                                ]

                                )
                            )

                            ]
                        ),
                        dbc.Row(
                            [dbc.Card(
                                dbc.CardBody([
                                    html.Div("Action", style={
                                        'background-color': '#ffa600',
                                        'text-align': 'center',
                                        'font-size': '30px',
                                    }),
                                    html.Div([dcc.Graph(id='clicks_difference', className='card-style')]),
                                    html.Div(children=[html.H4("Clicks/Views %"),
                                                       html.H4(id='clicks_views')], className='card-div'),
                                ])
                            )]
                        )
                        ])
            ], width={'size': 6}, style={'margin-top': '30px'}
            ),
    ]
    ),

    ])
])


@app.callback([
    Output(component_id='views', component_property='figure'),
    Output(component_id='hours', component_property='figure'),
    Output(component_id='likes', component_property='figure'),
    Output(component_id='subscribers', component_property='figure'),
    Output(component_id='card_clicks', component_property='figure'),
    Output(component_id='plot', component_property='figure'),
    Output(component_id='views_difference', component_property='figure'),
    Output(component_id='hours_difference', component_property='figure'),
    Output(component_id='total_watch_time', component_property='children'),
    Output(component_id='average_watch_time', component_property='children'),
    Output(component_id='likes_ratio', component_property='children'),
    Output(component_id='subscribers_gained', component_property='figure'),
    Output(component_id='subscribers_views', component_property='children'),
    Output(component_id='comments_views', component_property='children'),
    Output(component_id='clicks_difference', component_property='figure'),
    Output(component_id='clicks_views', component_property='children'),
            ],
    [
    Input(component_id='date_selector', component_property='start_date'),
    Input(component_id='date_selector', component_property='end_date')
    ],
              )
def filtered_dashboard(start_date, end_date):
    time_delta = (dt.datetime.strptime(end_date, "%Y-%m-%d").date()
                  - dt.datetime.strptime(start_date, "%Y-%m-%d").date()).days
    time_based_df = df_time_based_info.sort_values(by='date')
    time_based_df['views_period_ago'] = time_based_df['views'].shift(time_delta)
    time_based_df['minutes_period_ago'] = time_based_df['estimatedMinutesWatched'].shift(time_delta)
    time_based_df['subscribers_period_ago'] = time_based_df['subscribersGained'].shift(time_delta)
    time_based_df['clicks_period_ago'] = time_based_df['cardClicks'].shift(time_delta)
    time_based_df = time_based_df[(time_based_df['date'] >= start_date) & (time_based_df['date'] <= end_date)]
    fig_plot = px.line(time_based_df, x='date', y=time_based_df.columns[[2, 10]], height=300)
    fig_plot.update_layout(
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
        orientation="h",
        yanchor="top",
        entrywidth=300,
        y=1,
        xanchor="left",
        x=0.02,
        ),
        legend_font={'size': 19, 'family': 'Optima, sans-serif'},
        legend_title=None,

    )
    fig_plot.update_xaxes(visible=True, title=None, tickfont_size=22, tickfont_family='Optima, sans-serif')
    fig_plot.update_yaxes(visible=True, title=None, tickfont_size=22, tickfont_family='Optima, sans-serif')
    views = go.Figure(go.Indicator(value=time_based_df['views'].sum(),
                                   title={'text': "Views",
                                          'font': {'size': 20}},
                                   number={'font': {'size': 50}},
                                   )
                      )
    hours = go.Figure(go.Indicator(value=round(time_based_df['estimatedMinutesWatched'].sum() / 60, 0),
                                   title={'text': "Total Watch Time hours",
                                          'font': {'size': 20}},
                                   number={'font': {'size': 50}}
                                   )
                      )
    likes = go.Figure(go.Indicator(value=time_based_df['likes'].sum(),
                                   title={'text': "Video Likes Added",
                                          'font': {'size': 20}},
                                   number={'font': {'size': 50}}
                                   )
                      )
    subscribers = go.Figure(go.Indicator(value=time_based_df['subscribersGained'].sum(),
                                         title={'text': "User Subscriptions Added",
                                                'font': {'size': 20}},
                                         number={'font': {'size': 50}}
                                   )
                      )
    card_clicks = go.Figure(go.Indicator(value=time_based_df['cardClicks'].sum(),
                                         title={'text': "Info Card Clicks",
                                                'font': {'size': 20}},
                                         number={'font': {'size': 50}}
                                   )
                      )

    views_difference = go.Figure(go.Indicator(value=(time_based_df['views'].sum() - time_based_df['views_period_ago'].sum()),
                                              title={'text': "Views PoP", 'font': {'size': 20}},
                                              number={'font': {'size': 50}},
                                              mode="number+delta",
                                              delta={'reference': time_based_df['views'].sum(),
                                                     'relative': True,
                                                     'position': "bottom",
                                                     "valueformat": ".0%"}
                                   )
                      )

    hours_difference = go.Figure(go.Indicator(value=(
            (time_based_df['estimatedMinutesWatched'].sum() - time_based_df['minutes_period_ago'].sum()) / 60),
                                              title={'text': "Hours watched PoP",
                                                     'font': {'size': 20}},
                                              number={'font': {'size': 50}},
                                              mode="number+delta",
                                              delta={'reference': time_based_df['estimatedMinutesWatched'].sum() / 60,
                                                     'relative': True,
                                                     'position': "bottom", "valueformat": ".0%"}
                                   )
                      )

    total_watch_time = round(time_based_df['estimatedMinutesWatched'].sum() / 60, 0)
    average_watch_time = round(
        (time_based_df['estimatedMinutesWatched'].sum() / time_based_df['estimatedMinutesWatched'].count()), 0)
    average_watch_time = str(dt.timedelta(seconds=average_watch_time))
    likes_ratio = round(time_based_df['likes'].sum() / time_based_df['views'].sum() * 100, 2)

    subscribers_difference = go.Figure(go.Indicator(value=(
            time_based_df['subscribersGained'].sum() - time_based_df['subscribers_period_ago'].sum()),
                                              title={'text': "Subscribers Gained PoP",
                                                     'font': {'size': 20}},
                                              number={'font': {'size': 50}},
                                              mode="number+delta",
                                              delta={'reference': time_based_df['subscribersGained'].sum(),
                                                     'relative': True,
                                                     'position': "bottom",
                                                     "valueformat": ".0%"}
                                   )
                      )
    subscribers_views = round(time_based_df['subscribersGained'].sum() / time_based_df['views'].sum() * 100, 2)
    subscribers_comments = round(time_based_df['comments'].sum() / time_based_df['views'].sum() * 100, 2)

    clicks_difference = go.Figure(go.Indicator(value=(
            time_based_df['cardClicks'].sum() - time_based_df['clicks_period_ago'].sum()),
                                              title={'text': "Clicks PoP",
                                                     'font': {'size': 20}},
                                              number={'font': {'size': 50}},
                                              mode="number+delta",
                                              delta={'reference': time_based_df['cardClicks'].sum(),
                                                     'relative': True,
                                                     'position': "bottom",
                                                     "valueformat": ".0%"}
                                   )
                      )
    clicks_views = round(time_based_df['cardClicks'].sum() / time_based_df['views'].sum() * 100, 2)

    return views, hours, likes, subscribers, card_clicks, fig_plot, views_difference, hours_difference, \
        total_watch_time, average_watch_time, likes_ratio, subscribers_difference, subscribers_views, \
        subscribers_comments, clicks_difference, clicks_views


@app.callback(
    Output(component_id='funnel', component_property='figure'),
    [
    Input(component_id='title_selector', component_property='value'),
    ],
              )
def filtered_dashboard(value):
    filtered_df = df[df['title'] == value]

    funnel = go.Figure(go.Funnel(y=["Views", "Hours watched", "Subscribers", "CardClicks"],
                                 x=[filtered_df['views'].sum(),
                                   round(filtered_df['estimatedMinutesWatched'].sum() / 60, 0),
                                   filtered_df['subscribersGained'].sum(),
                                   filtered_df['cardClicks'].sum()
                                   ],
                                 textinfo="value+percent initial",
                                 textposition="outside",
                                 opacity=0.65,
                                 marker={"color": ["#1ca087", "#5cae5d", "#a8b223", "#ffa600"]},
                                 connector={"line": {"color": "royalblue", "width": 1}},
                              )
                       )
    funnel.update_layout(
        autosize=True,
        height=1200,
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, r=0, b=0, l=0),
        )
    funnel.update_yaxes(visible=False, title=None)
    funnel.update_traces(textfont_size=22, textfont_family='Optima, sans-serif')

    return funnel


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=18273, debug=True)
