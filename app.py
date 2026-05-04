import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, State
import pandas as pd
import numpy as np
# import plotly.express as px

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    title="Income Tax Simulator India",
)


server = app.server


# -----------------------------
# Tax Engine
# -----------------------------
def compute_tax(income, slabs):
    rows = []
    total_tax = 0

    for lower, upper, rate in slabs:
        if income > lower:
            taxable = min(income, upper) - lower
            tax = round(taxable * rate, 2)
        else:
            taxable = 0
            tax = 0

        if upper == np.inf:
            slab_label = f"{int(lower / 100000)}L - ∞L"
        else:
            slab_label = f"{int(lower / 100000)}L - {int(upper / 100000)}L"

        rows.append(
            {
                "Slab": slab_label,
                "Taxable": taxable,
                "Rate": rate,
                "Tax": tax,
            }
        )

        total_tax += tax

    cess = total_tax * 0.04
    final_tax = total_tax + cess

    return pd.DataFrame(rows), total_tax, cess, final_tax


# -----------------------------
# Layout
# -----------------------------
app.layout = dbc.Container(
    [
        # Header
        html.Div(
            [
                html.H2("Income Tax & Take-Home Simulator"),
                html.P("FY 2026-27 | New Tax Regime Calculator"),
            ],
            style={
                "textAlign": "center",
                "color": "#ffffff",
                "marginBottom": "20px",
            },
        ),

        # Input Card
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Input(
                                    id="basic",
                                    type="number",
                                    placeholder="Basic Salary",
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                dbc.Input(
                                    id="other",
                                    type="number",
                                    placeholder="Other Components",
                                ),
                                md=4,
                            ),
                            dbc.Col(
                                dbc.Input(
                                    id="deductions",
                                    type="number",
                                    placeholder="Other Deductions",
                                ),
                                md=4,
                            ),
                        ],
                        className="g-3",
                    ),

                    html.Br(),

                    dbc.Button(
                        "Calculate",
                        id="calculate-btn",
                        n_clicks=0,
                        className="w-100",
                        style={
                            "backgroundColor": "#63365d",
                            "color": "#ffffff",
                            "border": "none",
                            "fontWeight": "600",
                        },
                    ),
                ]
            ),
            style={
                "borderRadius": "12px",
                "boxShadow": "0px 4px 12px rgba(0,0,0,0.1)",
                "marginBottom": "20px",
            },
        ),

        # Output Section
        html.Div(id="take-home-output"),
    ],
    fluid=True,
    style={
        "backgroundColor": "#63365d",
        "minHeight": "100vh",
        "padding": "30px",
    },
)


# -----------------------------
# Callback
# -----------------------------
@app.callback(
    Output("take-home-output", "children"),
    Input("calculate-btn", "n_clicks"),
    State("basic", "value"),
    State("other", "value"),
    State("deductions", "value"),
)
def update(n_clicks, basic, other_allowances, deductions):

    if not n_clicks:
        return ""

    try:
        basic = float(basic or 0)
        other_allowances = float(other_allowances or 0)
        deductions = float(deductions or 0)
    except ValueError:
        return "Invalid input. Please enter numeric values."

    gross = basic + other_allowances

    standard_deduction = 75000
    taxable_income = gross - standard_deduction

    slabs = [
        (0, 400000, 0.00),
        (400000, 800000, 0.05),
        (800000, 1200000, 0.10),
        (1200000, 1600000, 0.15),
        (1600000, 2000000, 0.20),
        (2000000, 2400000, 0.25),
        (2400000, np.inf, 0.30),
    ]

    df, base_tax, cess, final_tax = compute_tax(taxable_income, slabs)

    # PF (more realistic capped version)
    monthly_basic = basic / 12
    pf = min(monthly_basic * 0.12, 15000) * 12

    total_deductions = pf + final_tax + deductions
    net = (gross - total_deductions) / 12

    summary = dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Small("Taxable Income"),
                            html.H4(f"₹{taxable_income:,.0f}",
                                    style={"color": "#63365d"}),
                        ],
                        md=2,
                    ),
                    dbc.Col(
                        [
                            html.Small("Base Tax"),
                            html.H4(f"₹{base_tax:,.0f}", style={
                                "color": "#c62828"}),
                        ],
                        md=2,
                    ),
                    dbc.Col(
                        [
                            html.Small("Cess"),
                            html.H4(f"₹{cess:,.0f}", style={
                                    "color": "#ff8f00"}),
                        ],
                        md=2,
                    ),
                    dbc.Col(
                        [
                            html.Small("Final Tax"),
                            html.H4(f"₹{final_tax:,.0f}",
                                    style={"color": "#c62828"}),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            html.Small("Monthly Take Home"),
                            html.H4(f"₹{net:,.0f}", style={
                                    "color": "#2e7d32"}),
                        ],
                        md=3,
                    ),
                ],
                className="g-4",
            )
        ),
        style={
            "borderRadius": "12px",
            "backgroundColor": "#ffffff",
            "boxShadow": "0px 4px 10px rgba(0,0,0,0.1)",
            "marginBottom": "20px",
            "padding": "10px",
        },
    )

    table = dbc.Card(
        dbc.CardBody(
            dbc.Table.from_dataframe(
                df,
                striped=True,
                bordered=False,
                hover=True,
                responsive=True,
                style={
                    "fontSize": "14px",
                    "textAlign": "center",
                },
            )
        ),
        style={
            "borderRadius": "12px",
            "backgroundColor": "#ffffff",
            "boxShadow": "0px 4px 10px rgba(0,0,0,0.1)",
        },
    )

    return html.Div([summary, table])


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=False)
