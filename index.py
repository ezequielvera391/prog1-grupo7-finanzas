import getpass
import random

## DATOS DEL SISTEMA

## Para el primer MVP vamos a tener un único usuario harcodeado, solo vamos a implementar el login
# Lista de usuarios, los usarios tienen las siguientes propiedades:
# - id: string (debe ser único y autogenerado)
# - name: string (debe ser único)
# - password: string
# - age: int - con propositos de métricas de la aplicación
# - genre: "M" | "F" | "X" - con propositos de métricas de la aplicación
# - role: "admin" | "user" - para definir si accede o no a las métricas de sistema

users = [
    {
        "id":"1", 
        "name": "admin", 
        "password": "1234", 
        "age": 20, 
        "genre": "M", 
        "role": "admin" 
    },
]

## Ingresos y egresos, van a tener la misma interfaz
# hay lista de ingresos y de egresos, y tienen las siguientes propiedades
# - id: string (debe ser único)
# - amount: number
# - category: categorias (vamos a definir un listado fijo de categorias de ingreso y de egreso)
# - date: "dd/mm/yyyy" (pueden ingresarse fechas que no sean la actual)
# - user: string (se debe guardar automaticamente con el valor del nombre o el id del usuario que realice la carga)
# Ejemplo de valor correcto para un ingreso o egreso: entidad = { "id": "1", "amount": 1800.0, "category": "Other", "date": "08/06/2025", "user": "admin" }


incomes = []
income_categories = ["Salario", "Regalo", "Otros"]
expenses = []
expense_categories = ["Supermercado", "Vivienda", "Transporte", "Otros"]

# ABM INGRESOS
def insertIncome(income):
    '''
    Este método recibe un ingreso, se asegura que sea un ingreso válido
    y lo inserta en la lista de ingresos
    '''
    if income.get("amount") <= 0:
        return False
    
    incomes.append(income)
    return True


def updateIncome(income):
    '''
    Este método recibe un ingreso, se asegura que sea un ingreso válido y que exista en la lista de ingresos
    reemplaza el ingreso anterior con el nuevo
    '''
    for i in range(len(incomes)):
        if incomes[i].get("id") == income.get("id"):
            incomes[i] = income
            return True
    return False

def deleteIncome(income):
    '''
    Este método recibe el id de un ingreso, se asegura que exista en la lista de ingresos
    elimina el ingreso correspondiente al id
    '''
    for i in range(len(incomes)):
        if incomes[i].get("id") == income.get("id"):
            incomes.pop(i)
            return True
    return False
    

def getIncomesByUser(username):
    '''
    Este método recibe el nombre de un usuario y busca en la lista todos los incomes que hayan sido ingresados por ese usuario
    '''
    found_incomes = []
    for income in incomes:
        if income.get("user") == username:
            found_incomes.append(income)
    return found_incomes


# ABM EGRESOS
def insertExpenses(expense):
    '''
        Este método recibe un egreso, se asegura que sea un egreso válido
        y lo inserta en la lista de egresos
    '''
    if expense.get("amount") <= 0:
        return False
    
    expenses.append(expense)
    return True
    

def updateExpenses(expense):
    '''
    Este método recibe un egreso, se asegura que sea un egreso válido y que exista en la lista de egresos
    reemplaza el egreso anterior con el nuevo
    '''
    for i in range(len(expenses)):
        if expenses[i].get("id") == expense.get("id"):
            expenses[i] = expense
            return True
    return False

def deleteExpenses(expense):
    '''
    Este método recibe el id de un egreso, se asegura que exista en la lista de egreso
    elimina el egreso correspondiente al id
    '''
    for i in range(len(expenses)):
        if expenses[i].get("id") == expense.get("id"):
            expenses.pop(i)
            return True
    return False

def getExpensesByUser(username):
    '''
    Este método recibe el nombre de un usuario y busca en la lista todos los egresos que hayan sido ingresados por ese usuario
    '''
    found_expenses = []
    for expense in expenses:
        if expense.get("user") == username:
            found_expenses.append(expense)
    return found_expenses

# AUTH
def login(username, password):
    '''
    Este método recibe un nombre de usuario y una contraseña, 
    busca el usuario que coincida con ese nombre y luego verifica que la contraseña coincida
    - Devuelve un booleano que indica si se pudo autenticar o no
    '''
    for user in users:
        if user.get("name") == username and user.get("password") == password:
            return True
    return False


def getUser(username):
    '''
    Este método recibe un nombre de usuario y busca en la lista de usuarios si existe este usuario
    devuelve -1 en caso de no encontrarlo
    '''
    for user in users:
        if user["username"] == username:
            return user
    return -1

## Utils
def get_menu_option(message, options):
    '''
    Muestra un menú con las opciones dadas y devuelve el índice elegido.
    - message: título del menú
    - options: lista de strings con las opciones
    '''
    print(f"\n{message}")
    for i in range(len(options)):
        print(f"{i+1}. {options[i]}")
        
    choice = 0
    while choice < 1 or choice > len(options):
        choice_str = input("Seleccione una opción: ")
        if choice_str.isdigit():
            choice = int(choice_str)
        if choice < 1 or choice > len(options):
            print("Opción inválida, intente de nuevo.")

    return choice

def input_float(message):
    """
    Pide un número decimal al usuario y valida hasta que se ingrese correctamente.
    """
    value = None
    while value is None:
        user_input = input(message)
        if user_input.replace(".", "", 1).isdigit(): # si tiene punto lo toma igual como un numero porque elimina un . para la validacion
            value = float(user_input)
        else:
            print("Error: debe ingresar un número válido.")
    return value

def input_non_empty(message):
    """
    Pide un string no vacío.
    """
    value = ""
    while not value.strip():
        value = input(message)
        if not value.strip():
            print("Error: no puede estar vacío.")
    return value

def input_date(message):
    """
    Pide una fecha en formato dd/mm/yyyy.
    """
    date_str = ""
    is_valid = False
    while not is_valid:
        date_str = input(message)
        parts = date_str.split("/")
        if len(parts) == 3:
            day_str, month_str, year_str = parts[0], parts[1], parts[2]

            if day_str.isdigit() and month_str.isdigit() and year_str.isdigit():
                day = int(day_str)
                month = int(month_str)
                year = int(year_str)

                if 1 <= day <= 31 and 1 <= month <= 12 and year > 1900:
                    is_valid = True

        if not is_valid:
            print("Error: la fecha debe tener formato dd/mm/yyyy válido.")

    return date_str



def main():
    '''
    Función principal del programa
    '''
    print("Bienvenido al sistema de finanzas.")
    username = input("Ingrese nombre de usuario: ")
    password = getpass.getpass("Ingrese contraseña: ")

    isLogged = login(username, password)
    while not isLogged:
        print("Error en las credenciales")
        username = input("Ingrese nombre de usuario: ")
        password = getpass.getpass("Ingrese contraseña: ")
        isLogged = login(username, password)

    print("resultado: Auteticacion exitosa")
    # Se muestra menú principal


#### INICIO DE PROGRAMA
main()