from server import app  # Importa desde server.py
from dash import Input, Output
import plotly.graph_objects as go
from data import get_stock_data
from indicators import calcular_indicadores

@app.callback(
    Output('stock-graph', 'figure'),
    [Input('ticker-dropdown', 'value'),  # Nuevo Dropdown en vez del input
     Input('years-input', 'value'),
     Input('indicator-checklist', 'value')]
)
def update_graph(ticker, anios, selected_indicators):

    if selected_indicators is None:
        selected_indicators = []  # Asegura que sea una lista y no None

    stock_data = get_stock_data(ticker, anios)  # Obtener los datos

    if not stock_data:
        return go.Figure()

    data = calcular_indicadores(ticker, stock_data)

    # Crear la figura del gráfico de velas
    fig = go.Figure()

    # Agregar el gráfico de velas japonesas
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=ticker
    ))

    # Agregar EMA de 50 días
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["EMA_50"],
        mode="lines",
        name="EMA_50",
        line=dict(color="purple", width=2, dash="solid"),  # Línea punteada morada
        visible=True if "EMA" in selected_indicators else "legendonly"
    ))

    # Agregar SMA de 50 días
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["SMA_50"],
        mode="lines",
        name="SMA 50",
        line=dict(color="blue", width=1.5),
        visible=True if "SMA" in selected_indicators else "legendonly"
    ))

    # Agregar SMA de 200 días
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["SMA_200"],
        mode="lines",
        name="SMA 200",
        line=dict(color="orange", width=1.5),
        visible=True if "SMA" in selected_indicators else "legendonly"
    ))

    # Subgráfico 2: RSI (eje y2)
    fig.add_trace(go.Scatter(x=data.index, y=data["RSI"], mode='lines',
                  name="RSI (14 días)", line=dict(color='green'), yaxis="y2"))
    fig.add_trace(go.Scatter(x=data.index, y=[70]*len(data), mode='lines',
                  name="Sobrecompra (70)", line=dict(color='red', dash='dash'), yaxis="y2"))
    fig.add_trace(go.Scatter(x=data.index, y=[30]*len(data), mode='lines',
                  name="Sobreventa (30)", line=dict(color='red', dash='dash'), yaxis="y2"))

    # Señales de Compra RSI
    fig.add_trace(go.Scatter(
        x=data.index[data["Compra_RSI"]],
        y=data["RSI"][data["Compra_RSI"]],
        mode="markers", name="Compra RSI",
        marker=dict(color="lime", size=8, symbol="triangle-up"),
        yaxis="y2"
    ))

    # Señales de Venta RSI
    fig.add_trace(go.Scatter(
        x=data.index[data["Venta_RSI"]],
        y=data["RSI"][data["Venta_RSI"]],
        mode="markers", name="Venta RSI",
        marker=dict(color="crimson", size=8, symbol="triangle-down"),
        yaxis="y2"
    ))

    # Subgráfico 3: MACD (eje y3)
    fig.add_trace(go.Scatter(
        x=data.index, y=data["MACD"], mode='lines', name="MACD", line=dict(color='blue'), yaxis="y3"))
    fig.add_trace(go.Scatter(x=data.index, y=data["Signal"], mode='lines', name="Signal", line=dict(
        color='orange'), yaxis="y3"))
    fig.add_trace(go.Bar(x=data.index, y=data["Histograma"], name="Histograma", marker=dict(
        color='gray'), yaxis="y3"))

    # Señales de Compra MACD
    fig.add_trace(go.Scatter(
        x=data.index[data["Compra_MACD"]],
        y=data["MACD"][data["Compra_MACD"]],
        mode="markers", name="Compra MACD",
        marker=dict(color="cyan", size=8, symbol="triangle-up"),
        yaxis="y3"
    ))

    # Señales de Venta MACD
    fig.add_trace(go.Scatter(
        x=data.index[data["Venta_MACD"]],
        y=data["MACD"][data["Venta_MACD"]],
        mode="markers", name="Venta MACD",
        marker=dict(color="magenta", size=8, symbol="triangle-down"),
        yaxis="y3"
    ))

    # Agregar Bollinger Bands pero desactivadas inicialmente
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Banda_Superior'],
        mode='lines',
        name="Banda Superior",
        line=dict(color='red', dash='dot'),
        visible="legendonly" if "Bollinger" not in selected_indicators else True
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Banda_Inferior'],
        mode='lines',
        name="Banda Inferior",
        line=dict(color='red', dash='dot'),
        visible="legendonly" if "Bollinger" not in selected_indicators else True
    ))

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['SMA_20'],
        mode='lines',
        name="SMA 20",
        line=dict(color='rgba(0, 128, 255, 0.5)', width=1.5),
        visible="legendonly" if "Bollinger" not in selected_indicators else True
    ))

    # Señales de Compra Bollinger
    fig.add_trace(go.Scatter(
        x=data.index[data["Compra_Bollinger"]],
        y=data["Close"][data["Compra_Bollinger"]],
        mode="markers", name="Compra Bollinger",
        marker=dict(color="yellow", size=8, symbol="triangle-up"),
        visible="legendonly" if "Bollinger" not in selected_indicators else True
    ))

    # Señales de Venta Bollinger
    fig.add_trace(go.Scatter(
        x=data.index[data["Venta_Bollinger"]],
        y=data["Close"][data["Venta_Bollinger"]],
        mode="markers", name="Venta Bollinger",
        marker=dict(color="purple", size=8, symbol="triangle-down"),
        visible="legendonly" if "Bollinger" not in selected_indicators else True
    ))

    # Subgráfico 4: Volumen
    fig.add_trace(go.Bar(
        x=data.index,
        y=data["Volume"],
        name="Volumen",
        marker=dict(color='rgba(128, 128, 255, 0.6)'),
        yaxis="y4"
    ))

    # Media móvil del volumen
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Vol_SMA"],
        mode="lines",
        name="Volumen Promedio",
        line=dict(color='orange', dash='dot'),
        yaxis="y4"
    ))

    # Señales de compra por volumen
    fig.add_trace(go.Scatter(
        x=data.index[data["Compra_Volumen"]],
        y=data["Volume"][data["Compra_Volumen"]],
        mode="markers",
        name="Compra Volumen",
        marker=dict(color="lime", size=8, symbol="triangle-up"),
        yaxis="y4"
    ))

    # Señales de venta por volumen
    fig.add_trace(go.Scatter(
        x=data.index[data["Venta_Volumen"]],
        y=data["Volume"][data["Venta_Volumen"]],
        mode="markers",
        name="Venta Volumen",
        marker=dict(color="crimson", size=8, symbol="triangle-down"),
        yaxis="y4"
    ))

    fig.update_layout(
        title=f'Análisis de {ticker} ({anios} años)',
        xaxis=dict(title='Fecha'),
        yaxis=dict(title='Precio', domain=[0.7, 1]),
        yaxis2=dict(title='RSI', domain=[0.45, 0.65], anchor="x"),
        yaxis3=dict(title='MACD', domain=[0.25, 0.4], anchor="x"),
        yaxis4=dict(title='Volumen', domain=[0, 0.2], anchor="x"),
        template='plotly_dark',
        showlegend=True,
        xaxis_rangeslider_visible=False,
        height=690  # Podés ajustar esto a gusto
    )


    return fig
