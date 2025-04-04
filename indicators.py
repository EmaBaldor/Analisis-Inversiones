import pandas as pd
import numpy as np

def calcular_indicadores(ticker, data):

    # Convertir datos a DataFrame para facilidad de manejo
    data = pd.DataFrame(data)
    data["Date"] = pd.to_datetime(data["Date"])  # Asegurar que la fecha es tipo datetime
    data.set_index("Date", inplace=True)  # Usar la fecha como índice

    data["EMA_50"] = data["Close"].ewm(span=50, adjust=False).mean()
    
    # Calcular los promedios móviles
    data["SMA_50"] = data["Close"].rolling(window=50).mean()
    data["SMA_200"] = data["Close"].rolling(window=200).mean()

    # Calcular el RSI
    # Calculamos la diferencia de precios entre días consecutivos
    delta = data["Close"].diff()
    # Calculamos ganancias y pérdidas
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    # Promedio exponencial (EMA)
    gain_avg = pd.Series(gain).ewm(span=14, adjust=False).mean()
    loss_avg = pd.Series(loss).ewm(span=14, adjust=False).mean()
    # Índice de fuerza relativa (RS)
    rs = np.where(loss_avg == 0, 0, gain_avg / loss_avg)
    # RSI final
    data["RSI"] = 100 - (100 / (1 + rs))

    # Calcular el MACD
    short_ema = data["Close"].ewm(span=12, adjust=False).mean()
    long_ema = data["Close"].ewm(span=26, adjust=False).mean()
    data["MACD"] = short_ema - long_ema
    data["Signal"] = data["MACD"].ewm(span=9, adjust=False).mean()
    data["Histograma"] = data["MACD"] - data["Signal"]

    # Usamos una ventana de 20 días por defecto para la media móvil
    data["SMA_20"] = data["Close"].rolling(window=20).mean()

    # Calcular la desviación estándar
    data["STD_20"] = data["Close"].rolling(window=20).std()

    # Banda superior y banda inferior
    data["Banda_Superior"] = data["SMA_20"] + (2 * data["STD_20"])
    data["Banda_Inferior"] = data["SMA_20"] - (2 * data["STD_20"])

    # Identificar señales de compra y venta para cada indicador
    data["Compra_Precio"] = (
        data["MACD"] > data["Signal"]) & (data["RSI"] < 30)
    data["Venta_Precio"] = (data["MACD"] < data["Signal"]) & (data["RSI"] > 70)

    # Identificar las señales de cruce de las medias móviles
    data["Compra_SMA"] = (data["SMA_50"] > data["SMA_200"]) & (
        data["SMA_50"].shift(1) <= data["SMA_200"].shift(1))
    data["Venta_SMA"] = (data["SMA_50"] < data["SMA_200"]) & (
        data["SMA_50"].shift(1) >= data["SMA_200"].shift(1))

    # Señales para RSI: Compra cuando RSI < 30 (sobreventa), Venta cuando RSI > 70 (sobrecompra)
    data["Compra_RSI"] = data["RSI"] < 30
    data["Venta_RSI"] = data["RSI"] > 70

    # Señales de Compra y Venta MACD (detectando cruces)
    data["Compra_MACD"] = (data["MACD"] > data["Signal"]) & (data["MACD"].shift(1) <= data["Signal"].shift(1))
    data["Venta_MACD"] = (data["MACD"] < data["Signal"]) & (data["MACD"].shift(1) >= data["Signal"].shift(1))

    # Señales de compra y venta Bollinger
    data["Compra_Bollinger"] = data["Close"] < data["Banda_Inferior"]
    data["Venta_Bollinger"] = data["Close"] > data["Banda_Superior"]

    # Media móvil del volumen
    data["Vol_SMA"] = data["Volume"].rolling(window=20).mean()

    # Señales: compra si el volumen actual es mucho mayor que el promedio y el precio sube
    data["Compra_Volumen"] = (data["Volume"] > 1.5 * data["Vol_SMA"]) & (data["Close"] > data["Open"])

    # Señal de venta: mucho volumen con vela bajista
    data["Venta_Volumen"] = (data["Volume"] > 1.5 * data["Vol_SMA"]) & (data["Close"] < data["Open"])


    return data
