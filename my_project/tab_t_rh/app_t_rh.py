from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from my_project.utils import (
    generate_chart_name,
    title_with_tooltip,
    summary_table_tmp_rh_tab,
)
from my_project.template_graphs import heatmap, yearly_profile, daily_profile
import pandas as pd
from global_scheme import dropdown_names

from app import app, cache, TIMEOUT


def layout_t_rh():
    return html.Div(
        className="container-col full-width",
        children=[
            html.Div(
                className="container-row full-width align-center justify-center",
                children=[
                    html.H4(
                        className="text-next-to-input", children=["Select a variable: "]
                    ),
                    dcc.Dropdown(
                        id="dropdown",
                        className="dropdown-t-rh",
                        options=[
                            {
                                "label": "Dry bulb temperature",
                                "value": dropdown_names["Dry bulb temperature"],
                            },
                            {
                                "label": "Relative humidity",
                                "value": dropdown_names["Relative humidity"],
                            },
                        ],
                        value=dropdown_names["Dry bulb temperature"],
                    ),
                ],
            ),
            html.Div(
                className="container-col",
                children=[
                    html.Div(
                        children=title_with_tooltip(
                            text="Yearly chart",
                            tooltip_text=None,
                            id_button="yearly-chart-label",
                        ),
                    ),
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="yearly-chart"),
                    ),
                    html.Div(
                        children=title_with_tooltip(
                            text="Daily chart",
                            tooltip_text=None,
                            id_button="daily-chart-label",
                        ),
                    ),
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="daily"),
                    ),
                    html.Div(
                        children=title_with_tooltip(
                            text="Heatmap chart",
                            tooltip_text=None,
                            id_button="heatmap-chart-label",
                        ),
                    ),
                    dcc.Loading(
                        type="circle",
                        children=html.Div(id="heatmap"),
                    ),
                    html.Div(
                        children=title_with_tooltip(
                            text="Descriptive statistics",
                            tooltip_text="count, mean, std, min, max, and percentiles",
                            id_button="table-tmp-rh",
                        ),
                    ),
                    dbc.Row(
                        align="center",
                        justify="center",
                        id="table-tmp-hum",
                    ),
                ],
            ),
        ],
    )


@app.callback(
    Output("yearly-chart", "children"),
    [Input("global-local-radio-input", "value"), Input("dropdown", "value")],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
# @code_timer
def update_yearly_chart(global_local, dd_value, df, meta):
    df = pd.read_json(df, orient="split")

    if dd_value == dropdown_names["Dry bulb temperature"]:
        dbt_yearly = yearly_profile(df, "DBT", global_local)
        dbt_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

        return dcc.Graph(
            config=generate_chart_name("tdb_yearly_t_rh", meta),
            figure=dbt_yearly,
        )
    else:
        rh_yearly = yearly_profile(df, "RH", global_local)
        rh_yearly.update_layout(xaxis=dict(rangeslider=dict(visible=True)))

        return dcc.Graph(
            config=generate_chart_name("rh_yearly_t_rh", meta),
            figure=rh_yearly,
        )


@app.callback(
    Output("daily", "children"),
    [Input("global-local-radio-input", "value"), Input("dropdown", "value")],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
# @code_timer
def update_daily(global_local, dd_value, df, meta):
    df = pd.read_json(df, orient="split")

    if dd_value == dropdown_names["Dry bulb temperature"]:
        return dcc.Graph(
            config=generate_chart_name("tdb_daily_t_rh", meta),
            figure=daily_profile(df, "DBT", global_local),
        )
    else:
        return dcc.Graph(
            config=generate_chart_name("rh_daily_t_rh", meta),
            figure=daily_profile(df, "RH", global_local),
        )


@app.callback(
    Output("heatmap", "children"),
    [Input("global-local-radio-input", "value"), Input("dropdown", "value")],
    [State("df-store", "data"), State("meta-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
# @code_timer
def update_heatmap(global_local, dd_value, df, meta):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    if dd_value == dropdown_names["Dry bulb temperature"]:
        return dcc.Graph(
            config=generate_chart_name("tdb_heatmap_t_rh", meta),
            figure=heatmap(df, "DBT", global_local),
        )
    else:
        return dcc.Graph(
            config=generate_chart_name("rh_heatmap_t_rh", meta),
            figure=heatmap(df, "RH", global_local),
        )


@app.callback(
    Output("table-tmp-hum", "children"),
    [Input("dropdown", "value")],
    [State("df-store", "data")],
)
@cache.memoize(timeout=TIMEOUT)
def update_table(dd_value, df):
    """Update the contents of tab three. Passing in general info (df, meta)."""
    df = pd.read_json(df, orient="split")
    return summary_table_tmp_rh_tab(df, dd_value)
