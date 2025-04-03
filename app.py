from server import app
from layout import layout

app.title = "Análisis de Acciones"
app.layout = layout

# Importa los callbacks después de definir 'app'
import callbacks

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
