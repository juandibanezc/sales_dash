# Import required libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from utils import *
import warnings
import copy
warnings.filterwarnings("ignore")

# Multi-dropdown options
from controls import STORE_ID, ITEM_LEVEL, ITEM_APPLICATION

app = dash.Dash(__name__)

# Create controls
store_id_options = [{'label': str(STORE_ID[store_id]), 'value': str(store_id)}
                  for store_id in STORE_ID]

item_level_options = [{'label': str(ITEM_LEVEL[item_level]), 'value': str(item_level)}
                  for item_level in ITEM_LEVEL]

item_application_options = [{'label': str(ITEM_APPLICATION[item_app]), 'value': str(item_app)}
                  for item_app in ITEM_APPLICATION]

# Load data
df = pd.read_pickle('cleanCustomerData.pkl')
daterange = pd.date_range(start='2020',end='2022',freq='D')[:-1]

# Create global chart template
layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
)

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            'Reporte de ventas',
                        ),
                        html.H4(
                            'Desempeño comercial',
                        )
                    ],
                    className='six columns',
                    style = {}
                ),
                html.Div(
                    html.P(
                    ),
                    className='four columns',
                ),
                html.Div(
                    html.Img(
                        src="https://uploads-ssl.webflow.com/60889585823a4675257be336/60907966556fcae07e3e3064_datavalue-Logo-01-p-800.png",
                        className='seven columns'
                    ),
                    style = {'display': 'flex','justify-content': 'right'},
                    className='four columns'
                )
            ],
            id="header",
            className='row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'Filtrar por fecha de la transacción:',
                            className="control_label"
                        ),
                        dcc.RangeSlider(
                            id='month_slider',
                            updatemode = 'mouseup',
                            min = unix_time_millis(min(salesPerMonth(df))),
                            max = unix_time_millis(max(salesPerMonth(df))),
                            value = [unix_time_millis(min(salesPerMonth(df))),
                                        unix_time_millis(max(salesPerMonth(df)))],
                            
                            className="dcc_control"
                        ),
                        html.Div(
                            id='output-container-range-slider',
                            className="control_label"
                        ),
                        html.P(
                            'Filtrar por tienda:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='store_ids',
                            options=store_id_options,
                            multi=True,
                            value=list(STORE_ID.keys()),
                            className="dcc_control"
                        ),
                        html.P(
                            'Filtrar por nivel de producto:',
                            className="control_label"
                        ),
                        dcc.Dropdown(
                            id='item_levels',
                            options=item_level_options,
                            multi=True,
                            value=list(ITEM_LEVEL.keys()),
                            className="dcc_control"
                        ),
                        html.P(
                            'Filtrar por aplicación del producto:',
                            className="control_label"
                        ),
                        dcc.RadioItems(
                            id='item_app_selector',
                            options=[
                                {'label': 'Todos ', 'value': 'todos'},
                                {'label': 'Escoger ', 'value': 'escoger'}
                            ],
                            value='todos',
                            labelStyle={'display': 'inline-block'},
                            className="dcc_control"
                        ),
                        dcc.Dropdown(
                            id='item_apps',
                            options=item_application_options,
                            multi=True,
                            value=list(ITEM_APPLICATION.keys()),
                            className="dcc_control"
                        ),
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            id="sales_text",
                                            className="info_text"
                                        ),
                                        html.P("Ventas totales")
                                    ],
                                    id="sales",
                                    className="pretty_container",
                                    style={'width':160}
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H6(
                                                    id="clientsText",
                                                    className="info_text"
                                                ),
                                                html.P("Numero de clientes")
                                            ],
                                            id="clients",
                                            className="pretty_container",
                                            style={'width':160}
                                        ),
                                        html.Div(
                                            [
                                                html.H6(
                                                    id="ticketsText",
                                                    className="info_text"
                                                ),
                                                html.P("Numero de tickets")
                                            ],
                                            id="tickets",
                                            className="pretty_container",
                                            style={'width':160}
                                        ),
                                        html.Div(
                                            [
                                                html.H6(
                                                    id="meanTicketText",
                                                    className="info_text"
                                                ),
                                                html.P("Ticket promedio")
                                            ],
                                            id="meanTicket",
                                            className="pretty_container",
                                            style={'width':160}
                                        ),
                                    ],
                                    id="tripleContainer",
                                )
                            ],
                            id="infoContainer",
                            className="row"
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='sales_graph',
                                )
                            ],
                            id="salesGraphContainer",
                            className="pretty_container"
                        )
                    ],
                    id="rightCol",
                    className="eight columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [
                html.Div(
                            [
                                dcc.Graph(
                                    id='itemGroup_graph',
                                    style={'width': 750, 'height': 350}
                                )
                                
                            ],
                            id="itemGroupGraphContainer",
                            className="pretty_container",
                            style={"align":"center","align-text": "center", "justify-content": "center"}
                ),
                html.Div(
                            [
                                dcc.Graph(
                                    id='businessUnit_graph',
                                    style={'width': 360, 'height':350}
                                )
                            ],
                            id="businessUnitGraphContainer",
                            className="pretty_container",
                            style={"align":"center","align-text": "center", "justify-content": "center"}
                )
            ],
            id="graphContainer",
            className="row"
        )
    ] 
)

# Create callbacks
@app.callback(Output('aggregate_data', 'data'),
              [Input('store_ids', 'value'),
               Input('item_levels', 'value'),
               Input('item_apps', 'value'),
               Input('month_slider', 'value')])
def update_production_text(store_ids, item_levels, item_apps, month_slider):

    dff = filter_dataframe(df, store_ids, item_levels, item_apps, month_slider[0], month_slider[1])
    sales, customers, tickets, meanTicket = fetch_aggregate(dff)
    print('{0} and {1}'.format(sales, customers))
    data = [human_format(sales),human_format(customers), human_format(tickets), human_format(meanTicket)]
    return data

# Selectors -> data text
@app.callback(Output('sales_text', 'children'),
              [Input('aggregate_data', 'data')])
def update_sales_text(data):
    return "$" + data[0]

@app.callback(Output('clientsText', 'children'),
              [Input('aggregate_data', 'data')])
def update_clients_text(data):
    return data[1]


@app.callback(Output('ticketsText', 'children'),
              [Input('aggregate_data', 'data')])
def update_tickets_text(data):
    return data[2]

@app.callback(Output('meanTicketText', 'children'),
              [Input('aggregate_data', 'data')])
def update_mean_tickets_text(data):
    return "$" + data[3]

# Radio -> multi (itemApplications)
@app.callback(Output('item_apps', 'value'),
              [Input('item_app_selector', 'value')])
def display_status(selector):
    if selector == 'todos':
        return list(ITEM_APPLICATION.keys())
    else:
        return []

# Selectors -> sales graph
@app.callback(Output('sales_graph', 'figure'),
              [Input('store_ids', 'value'),
               Input('item_levels', 'value'),
               Input('item_apps', 'value'),
               Input('month_slider', 'value')])
def make_sales_figure(store_ids, item_levels, item_apps, month_slider):

    layout_sales = copy.deepcopy(layout)

    dff = filter_dataframe(df, store_ids, item_levels, item_apps, 1577836800, 1633046400)
    dff_month = dff.groupby(['yearMonth']).sum().reset_index(drop=False)
    
    s = dt.datetime.utcfromtimestamp(month_slider[0]).strftime('%Y-%m-%d')
    e = dt.datetime.utcfromtimestamp(month_slider[1]).strftime('%Y-%m-%d')
   
    colors = []
    for i in dff_month.yearMonth.to_list():
        if i >= pd.to_datetime(s) and i <= pd.to_datetime(e):
            colors.append('rgb(123, 199, 255)')
        else:
            colors.append('rgba(123, 199, 255, 0.2)')

    data = [
        dict(
            type='bar',
            x=dff_month["yearMonth"],
            y=dff_month["value"],
            name='Mensuales',
            marker=dict(
                color=colors
            ),
        ),
        dict(
            type='line',
            x=dff_month["yearMonth"],
            y=dff_month["value"],
            name='Mensuales',
            markers = True,
            line = dict(color='rgb(35,41,68)')
        )
    ]  
       
    layout_sales['title'] = 'Ventas totales por mes'
    layout_sales['dragmode'] = 'select'
    layout_sales['showlegend'] = False
    layout_sales['autosize'] = True
    layout_sales['margin'] = dict(
        l=50,
        r=30,
        b=40,
        t=40,
        pad = 10
    )

    figure = dict(data=data, layout=layout_sales)
    return figure

# Selectors -> itemGroup graph
@app.callback(Output('itemGroup_graph', 'figure'),
              [Input('store_ids', 'value'),
               Input('item_levels', 'value'),
               Input('item_apps', 'value'),
               Input('month_slider', 'value')])
def make_itemGroup_figure(store_ids, item_levels, item_apps, month_slider):

    dff = filter_dataframe(df, store_ids, item_levels, item_apps, month_slider[0], month_slider[1])
    df_itemGroup = dff.groupby(['itemGroup']).sum().reset_index(drop=False).sort_values(["value"], ascending=True)
    data = [
        dict(
            type='bar',
            x=df_itemGroup.value,
            y=df_itemGroup.itemGroup,
            orientation='h',
        )]
    layout_sales = {}
    layout_sales['title'] = 'Ventas totales por grupo de productos'
    layout_sales['autosize'] = True
    layout_sales['automargin'] = True
    layout_sales['plot_bgcolor'] = "#F9F9F9"
    layout_sales['paper_bgcolor'] = "#F9F9F9"
    layout_sales['margin'] = dict(
        l=220,
        r=30,
        b=40,
        t=40,
        pad = 10
    )
    layout_sales['hovermode'] = "closest"

    figure = dict(data=data, layout=layout_sales)

    return figure

#Selectors -> businessUnit graph
@app.callback(Output('businessUnit_graph', 'figure'),
              [Input('store_ids', 'value'),
               Input('item_levels', 'value'),
               Input('item_apps', 'value'),
               Input('month_slider', 'value')])
def make_itemBusinessUnit_figure(store_ids, item_levels, item_apps, month_slider):

    layout_sales = copy.deepcopy(layout)

    dff = filter_dataframe(df, store_ids, item_levels, item_apps, month_slider[0], month_slider[1])
    df_businessUnit = dff.groupby(['businessUnit']).sum().reset_index(drop=False).sort_values(["value"], ascending=True)
    
    data = [
        dict(
            type='pie',
            labels=df_businessUnit.businessUnit,
            values=df_businessUnit.value, 
            hole=.6,
        )]

    layout_sales['title'] = 'Porcentaje de ventas por<br>unidad de negocio'
    layout_sales['margin'] = dict(t=80)
                            
        
    figure = dict(data=data, layout=layout_sales)

    return figure

@app.callback(Output('output-container-range-slider', 'children'),
              [Input('month_slider', 'value')])
def update_label(month_slider):
    
    s = dt.datetime.utcfromtimestamp(month_slider[0]).strftime('%Y-%m-%d')
    e = dt.datetime.utcfromtimestamp(month_slider[1]).strftime('%Y-%m-%d')
    
    return 'Has seleccionado: [ {0} , {1} ]'.format(s,e)

# Main
if __name__ == '__main__':
    app.server.run(port=8057, debug=True)
