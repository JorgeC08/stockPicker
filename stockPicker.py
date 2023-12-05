import sys
import csv


# Funcion para cargar el file
def load_data(filename):
    # Lista para almacenar las acciones
    stocks = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        # Saltar encabezado, parece que moodle tiene uno
        next(reader)
        # Identificar cada columna del csv file
        for row in reader:
            # Se crea una lista de listas el cual contiene los datos de cada accion
            stock = {
                'name': row[0],
                'price': float(row[1]),
                '1m': float(row[2]),
                '6m': float(row[3]),
                '1y': float(row[4]),
                '5y': float(row[5])
            }

            stocks.append(stock)
    return stocks


# Funcion para seleccionar las acciones
def stock_picker(filename, amount, timeframe):
    stocks = load_data(filename)

    # Calcular el Return Of Investment (ROI) para cada accion
    for stock in stocks:
        stock['roi'] = stock[timeframe] / stock['price']

    # Ordenar las acciones por ROI de mayor a menor, reverse=True debido a que por default los ordena de menor a mayor
    # La funcion lambda se utiliza para ordenar la lista de diccionarios
    stocks.sort(key=lambda stock: stock['roi'], reverse=True)

    # Lista para almacenar las acciones seleccionadas
    portfolio = []

    # Dinero restante para invertir
    investment_remaining = amount

    # Variable para saber si se puede seguir comprando y asi evitar usar break
    continuarComprando = True

    # Para cada accion en la lista ordenada
    for stock in stocks:
        # Comprobando que el monto restante sea suficiente para comprar la accion
        if continuarComprando and investment_remaining >= stock['price']:
            portfolio.append(stock['name'])
            investment_remaining -= stock['price']

        elif continuarComprando and investment_remaining < stock['price']:
            # Si no es suficiente, calcular la fraccion de la accion que se puede comprar
            fraction = investment_remaining / stock['price']
            portfolio.append("{:.2f} {}".format(fraction, stock['name']))
            continuarComprando = False  # Terminar el ciclo porque no podemos comprar mas acciones, asi nos salimos del bucle en moodle too sin errores :D

    return portfolio


if __name__ == "__main__":
    # Para correr el codigo desde el terminal usar el siguiente comando:
    # python ./stockPicker.py stocks.csv 300 1m // 300 es el monto a invertir y 1m es el periodo de tiempo
    if len(sys.argv) > 1:
        # Para leer los datos desde el command line
        filename = sys.argv[1]
        amount = float(sys.argv[2])
        timeframe = sys.argv[3]

        # Imprimir los stocks seleccionados
        print(stock_picker(filename, amount, timeframe))