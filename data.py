import yfinance as yf
import datetime
import os
import json



# Función para obtener los datos de una acción desde Yahoo Finance
def get_stock_data(ticker, years, filename="stock_data.json"):
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Verificar si el archivo existe antes de hacer la consulta
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                saved_data = json.load(file)
                # Verificar si el ticker está en los datos guardados
                if ticker in saved_data:
                    ticker_data = saved_data[ticker]
                    # Asegurarse de que la fecha guardada coincida con la fecha de hoy
                    if (ticker_data.get("date") == today_date) & (ticker_data.get("years") > years):
                        print("Usando datos guardados de hoy.")
                        data_filtered = filter_data_by_years(ticker_data["data"], years)
                        return data_filtered

            except json.JSONDecodeError:
                print("Error al leer el JSON, se generará uno nuevo.")

    # Si no hay datos de hoy, consultamos Yahoo Finance
    print("Consultando nuevos datos de Yahoo Finance...")
    end_date = today_date
    start_date = (datetime.datetime.now() - datetime.timedelta(days=years * 365)).strftime('%Y-%m-%d') #max 10 años

    # Descargar datos desde Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date)

    # Resetear el índice y convertir fechas a string
    data_reset = data.reset_index()

    # Convertir todas las claves y valores a tipos compatibles con JSON
    stock_data = []
    for row in data_reset.to_dict(orient='records'):
        clean_row = {}
        for k, v in row.items():
            if isinstance(k, tuple):  # Si la clave es una tupla, convertir a string limpio
                k = k[0]  # Tomar solo el primer valor de la tupla
            clean_row[k] = v.isoformat() if isinstance(v, datetime.datetime) else v
        stock_data.append(clean_row)

    # Agregar el ticker a los datos antes de guardarlos
    ticker_data = {
        "ticker": ticker,
        "date": today_date,
        "years": years,
        "data": stock_data
    }

    # Si el archivo ya existe, agregar o actualizar los datos del ticker
    if os.path.exists(filename):
        with open(filename, 'r') as file_read:
            try:
                saved_data = json.load(file_read)
            except json.JSONDecodeError:
                saved_data = {}

        # Agregar o actualizar los datos del ticker
        saved_data[ticker] = ticker_data
    else:
        saved_data = {ticker: ticker_data}

    # Guardar los datos completos en el archivo JSON
    with open(filename, 'w') as file:
        json.dump(saved_data, file, indent=4)

    return stock_data

def filter_data_by_years(data, years):
    """
    Filtra los datos de una acción por el rango de años especificado.
    """
    today = datetime.datetime.now()
    start_date = today - datetime.timedelta(days=years * 365)
    
    # Convertir las fechas a objetos datetime y filtrar los datos
    filtered_data = [
        item for item in data if datetime.datetime.fromisoformat(item['Date']) >= start_date
    ]
    return filtered_data