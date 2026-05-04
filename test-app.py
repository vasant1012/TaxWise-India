import dash
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

app = dash.Dash(__name__)
server = app.server


# -----------------------------
# Tax Slab Definitions
# -----------------------------
def get_new_slabs():
    return [
        (0, 400000, 0.00),
        (400000, 800000, 0.05),
        (800000, 1200000, 0.10),
        (1200000, 1600000, 0.15),
        (1600000, 2000000, 0.20),
        (2000000, 2400000, 0.25),
        (2400000, np.inf, 0.30),
    ]


def get_old_slabs():
    return [
        (0, 300000, 0.00),
        (300000, 600000, 0.05),
        (600000, 900000, 0.10),
        (900000, 1200000, 0.15),
        (1200000, 1500000, 0.20),
        (1500000, np.inf, 0.30),
    ]


# -----------------------------
# Tax Engine
# -----------------------------
def compute_tax(income, slabs):
    rows = []
    total_tax = 0

    for lower, upper, rate in slabs:
        if income > lower:
            taxable = min(income, upper) - lower
            tax = taxable * rate
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
app.layout = html.Div(
    [
        html.H2("Income Tax & Take-Home Simulator (India)"),
        html.Div(
            [
                html.Label("Gross Salary"),
                dcc.Input(id="gross", type="number", value=2691096),
                html.Br(),
                html.Label("Tax Regime"),
                dcc.Dropdown(
                    id="regime",
                    options=[
                        {"label": "NEW (FY 2026-27)", "value": "NEW"},
                        {"label": "OLD", "value": "OLD"},
                    ],
                    value="NEW",
                ),
                html.Br(),
                html.Label("PF (%)"),
                dcc.Slider(id="pf", min=0, max=20, step=1, value=12),
                html.Br(),
                html.Label("Other Monthly Deductions"),
                dcc.Input(id="other", type="number", value=2000),
            ],
            style={"width": "25%", "display": "inline-block",
                   "verticalAlign": "top"},
        ),
        html.Div(
            [
                html.H4("Outputs"),
                html.Div(id="summary"),
                dcc.Graph(id="bar-chart"),
                dcc.Graph(id="line-chart"),
            ],
            style={"width": "70%", "display": "inline-block"},
        ),
    ]
)


# -----------------------------
# Callback
# -----------------------------
@app.callback(
    [
        Output("summary", "children"),
        Output("bar-chart", "figure"),
        Output("line-chart", "figure"),
    ],
    [
        Input("gross", "value"),
        Input("regime", "value"),
        Input("pf", "value"),
        Input("other", "value"),
    ],
)
def update(gross, regime, pf_rate, other):

    standard_deduction = 75000
    taxable_income = gross - standard_deduction

    slabs = get_new_slabs() if regime == "NEW" else get_old_slabs()

    df, base_tax, cess, final_tax = compute_tax(taxable_income, slabs)

    # Monthly take-home
    monthly_gross = gross / 12
    pf = monthly_gross * (pf_rate / 100)
    monthly_tax = final_tax / 12
    net = monthly_gross - pf - monthly_tax - other

    summary = html.Div(
        [
            html.P(f"Taxable Income: ₹{taxable_income:,.0f}"),
            html.P(f"Base Tax: ₹{base_tax:,.0f}"),
            html.P(f"Cess: ₹{cess:,.0f}"),
            html.P(f"Final Tax: ₹{final_tax:,.0f}"),
            html.P(f"Monthly Take Home: ₹{net:,.0f}"),
        ]
    )

    # Bar chart
    fig_bar = px.bar(df, x="Slab", y="Tax",
                     title="Tax per Slab", text_auto=True)

    # Income vs tax curve
    incomes = np.arange(5_00_000, 40_00_000, 1_00_000)
    taxes = []

    for inc in incomes:
        slabs_temp = get_new_slabs() if regime == "NEW" else get_old_slabs()
        _, _, _, ft = compute_tax(inc - standard_deduction, slabs_temp)
        taxes.append(ft)

    df_curve = pd.DataFrame({"Income": incomes, "Tax": taxes})
    fig_line = px.line(df_curve, x="Income", y="Tax", title="Income vs Tax")

    return summary, fig_bar, fig_line


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run_server(debug=False)
