from dash import html, dcc
import json

# Leer los tickers desde el archivo JSON
with open("tickers.json", "r") as file:
    tickers_list = json.load(file)

tickers_list.sort()

layout = html.Div([
    html.Div(  # Barra lateral
        className="sidebar",
        children=[
            html.Label("Selecciona un Ticker:", className="label"),
            dcc.Dropdown(
                id='ticker-dropdown',
                options=[{'label': f'{ticker}', 'value': ticker} for ticker in tickers_list],
                value='MELI',  # Valor inicial
                clearable=False,
                className="dropdown"
            ),

            html.Label("Años de datos:", className="label"),
            dcc.Input(id='years-input', type='number', min=1, value=1, max=5, debounce=True, className="input"),

            html.Label("Indicadores:", className="label"),
            dcc.Checklist(
            id='indicator-checklist',
            options=[
                {'label': 'EMA_50', 'value': 'EMA'},
                {'label': 'Bollinger Bands', 'value': 'Bollinger'},
                {'label': 'SMA_50 y SMA_200', 'value': 'SMA'}
            ],
            className="checklist"
        ),

            # Información sobre los indicadores
            html.Div([
                html.H4("Información Indicadores", className="info-title"),
                dcc.Markdown("""
                **SMA (Simple Moving Average):**  
                - SMA_50: Promedio móvil de 50 días  
                - SMA_200: Promedio móvil de 200 días  
                 Tendencia alcista cuando el SMA 50 está por encima del SMA 200.

                **Bollinger Bands:**  
                 Volatilidad del precio  
                 - Banda superior SOBRECOMPRA  
                 - Banda inferior SOBREVENTA  
                 - SMA 20: línea central de soporte o resistencia  
                 - Bandas estrechas: baja volatilidad y posible ruptura futura.  

                **RSI (Relative Strength Index):**  
                 Fuerza de una tendencia  
                - Venta RSI > 70 (Sobrecompra)  
                - Compra RSI < 30 (Sobreventa)  

                **MACD (Moving Average Convergence Divergence):**  
                - Señal de compra cuando cruza hacia arriba  
                - Señal de venta cuando cruza hacia abajo  
                """, className="indicator-info")
            ], className="info-box")
        ]
    ),

    # Contenido principal (gráfico)
    html.Div([
        dcc.Graph(id='stock-graph', className="graph-container")
    ], className="main-content")
], className="container")
