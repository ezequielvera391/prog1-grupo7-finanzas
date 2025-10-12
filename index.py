from db import (
    ensure_db_files,
    income_categories, 
    expense_categories,
    incomes_insert, 
    incomes_update, 
    incomes_delete, 
    incomes_by_user, 
    expenses_insert, 
    expenses_update, 
    expenses_delete, 
    expenses_by_user, 
)
import getpass
import random

## DATOS DEL SISTEMA

## BASE DE DATOS
## Defino acá el path para los distintos archivos que van a representar las colecciones de mi base de datos

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


# ABM INGRESOS
def insertIncome(income):
    '''
    Este método recibe un ingreso de tipo dict
    y lo inserta en la lista de ingresos a través de un 
    En caso de una funcion de db.py
    Devuelve True en caso de éxito, False en caso de error
    '''
    ok, _ = incomes_insert(income)
    return ok


def updateIncome(income):
    '''
    Este método recibe un ingreso de tipo dict
    Realiza el update a ravés de una funcion de db.py
    Reemplaza el ingreso anterior con el nuevo
    Devuelve True en caso de éxito, False en caso de error
    '''
    ok, _ = incomes_update(income)
    return ok

def deleteIncome(income):
    '''
    Este método recibe un income de tipo dict, 
    Extrae el id y borra en base de datos el valor de income que coincida con ese id
    Esto lo hace a través de una funcion de db.py
    Devuelve True en caso de éxito, False en caso de error
    '''
    income_id = income.get("id")
    ok, _ = incomes_delete(income_id)
    return ok
    

def getIncomesByUser(username):
    '''
    Este método recibe el nombre de un usuario de tipo str
    Usa una función de db.py que busca todos los incomes pertenecientes a ese usuario
    Devuelve una lista de incomes, si el usuario no existe o no tiene incomes devuelve una lista vacia
    '''
    return incomes_by_user(username)


# ABM EGRESOS
def insertExpenses(expense):
    '''
    Este método recibe un egreso de tipo dict
    y lo inserta en la base de datos a través de una función de db.py.
    Devuelve True en caso de éxito, False en caso de error.
    '''
    ok, _ = expenses_insert(expense)
    return ok
    

def updateExpenses(expense):
    '''
    Este método recibe un egreso de tipo dict.
    Realiza el update a través de una función de db.py,
    reemplazando el egreso anterior con el nuevo (mismo id).
    Devuelve True en caso de éxito, False en caso de error.
    '''
    ok, _ = expenses_update(expense)
    return ok

def deleteExpenses(expense):
    '''
    Este método recibe un egreso de tipo dict,
    extrae el id y borra en base de datos el egreso que coincida con ese id,
    utilizando una función de db.py.
    Devuelve True en caso de éxito, False en caso de error.
    '''
    expense_id = expense.get("id")
    ok, _ = expenses_delete(expense_id)
    return ok

def getExpensesByUser(username):
    '''
    Este método recibe el nombre de usuario de tipo str.
    Usa una función de db.py que busca todos los egresos pertenecientes a ese usuario.
    Devuelve una lista de egresos; si el usuario no existe o no tiene egresos,
    devuelve una lista vacía.
    '''
    return expenses_by_user(username)
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
        if user["name"] == username:
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

def choose_category(categories):
    """
    Muestra un menú para elegir una categoría de la lista y devuelve el string elegido.
    """
    idx = get_menu_option("Elija una categoría", categories)
    return categories[idx - 1]



## Metricas
def convert_to_tuple(date_str):
    '''
    Convierte un string "dd/mm/yyyy" en una tupla (day, month, year) de enteros.
    - Si la fecha no tiene el formato correcto o valores fuera de rango, devuelve None.
    '''
    parts = date_str.split("/")
    if len(parts) != 3:
        return None

    day_str, month_str, year_str = parts[0], parts[1], parts[2]

    if (not day_str.isdigit()) or (not month_str.isdigit()) or (not year_str.isdigit()):
        return None

    day = int(day_str)
    month = int(month_str)
    year = int(year_str)

    if day < 1 or day > 31:
        return None
    if month < 1 or month > 12:
        return None
    if year <= 1900:
        return None
    
    return (day, month, year)


def calculate_monthly_savings(username, month, year):
    '''
    -Calcula el ahorro (ingresos - egresos) del usuario `username`
    para el mes `month` y año `year`.
    - Devuelve float (positivo/negativo/0.0).
    '''
    total_in = 0.0
    for inc in incomes_by_user(username):
        parsed = convert_to_tuple(inc.get("date"))
        if parsed and (parsed[1], parsed[2]) == (month, year):
            total_in = total_in + float(inc.get("amount", 0.0))

    total_out = 0.0
    for exp in  expenses_by_user(username):
        parsed = convert_to_tuple(exp.get("date"))
        if parsed and (parsed[1], parsed[2]) == (month, year):
            total_out = total_out + float(exp.get("amount", 0.0))

    return total_in - total_out


def percent_change_in_savings(username, month1, year1, month2, year2):
    '''
    Calcula el porcentaje de aumento/disminución del ahorro
    entre el período (month1, year1) y (month2, year2).
    - Fórmula: ((s2 - s1) / |s1|) * 100
    - Si s1 == 0.0 y s2 == 0.0 -> devuelve 0.0
    - Si s1 == 0.0 y s2 != 0.0 -> devuelve None 
    - Devuelve float (porcentaje) o None si no se puede calcular.
    '''
    s1 = calculate_monthly_savings(username, month1, year1)
    s2 = calculate_monthly_savings(username, month2, year2)

    if s1 == 0.0 and s2 == 0.0:
        return 0.0

    if s1 == 0.0:
        return None

    s1_abs = s1 if s1 >= 0 else -s1

    pct = ((s2 - s1) / s1_abs) * 100.0
    return pct



def average_expense_by_category(username, month, year):
    """
    Calcula el porcentaje de gasto por categoría para un usuario.
    - Proceso:
        1. Filtra egresos del usuario para el mes/año dados
        2. Agrupa por categoría y acumula el total por categoría
        3. Calcula porcentaje = (suma_categoria / total_gastos) * 100
    
    Devuelve el porcentaje que representa cada categoría del total de gastos.
    """
    category_totals = {}
    total_expenses = 0.0
        
    for exp in expenses_by_user(username):
        parsed = convert_to_tuple(exp.get("date"))
        if parsed:
            if (parsed[1] == month and parsed[2] == year):
                cat = exp.get("category", "otros")
                amount = exp.get("amount")
                if cat in category_totals:
                    category_totals[cat] = category_totals[cat] + amount
                else:
                    category_totals[cat] = amount
                total_expenses += amount
    
    percentages = {}
    if total_expenses > 0:
        for category in category_totals:
            percentages[category] = (category_totals[category] / total_expenses) * 100.0

    return percentages 


### Menus
def incomes_menu(current_username):
    options = [
        "Agregar ingreso",
        "Actualizar ingreso",
        "Eliminar ingreso",
        "Listar todos mis ingresos",
        "Volver"
    ]

    selected = 0
    while selected != len(options):
        selected = get_menu_option("Menú de Ingresos", options)

        # Crear
        if selected == 1:
            income_id = str(random.randint(1000, 9999))
            amount = input_float("Ingrese el monto: ")
            category = choose_category(income_categories)
            date = input_date("Ingrese la fecha en formato (dd/mm/yyyy): ")
            income = {
                "id": income_id,
                "amount": amount,
                "category": category,
                "date": date,
                "user": current_username
            }
            ok = insertIncome(income)
            print("Ingreso agregado." if ok else "No se pudo agregar el ingreso (amount debe ser mayor a 0).")
        # Actualizar
        elif selected == 2:
            income_id = input_non_empty("ID del ingreso a actualizar: ")
            amount = input_float("Nuevo ingreso: ")
            category = choose_category(income_categories)
            date = input_date("Nueva fecha (dd/mm/yyyy): ")
            income = {
                "id": income_id,
                "amount": amount,
                "category": category,
                "date": date,
                "user": current_username
            }
            ok = updateIncome(income)
            print("Ingreso actualizado." if ok else "No se encontró el ingreso para actualizar.")
        # Eliminar
        elif selected == 3:
            income_id = input_non_empty("ID del income a eliminar: ")
            ok = deleteIncome({"id": income_id})
            print("Ingreso eliminado." if ok else "No se encontró el ingreso para eliminar.")
        # Listar
        elif selected == 4:
            items = getIncomesByUser(current_username)
            if not items:
                print("No hay ingresos para este usuario.")
            else:
                print("\nIngresos del usuario actual:")
                for i in range(len(items)):
                    it = items[i]
                    print(f"- [{it['id']}] {it['date']} | {it['category']} | {it['amount']}")

        elif selected == 5:
            print("Volviendo al menú principal...")

def expenses_menu(current_username):
    options = [
        "Agregar egreso",
        "Actualizar egreso",
        "Eliminar egreso",
        "Listar todos mis egresos",
        "Volver"
    ]

    selected = 0
    while selected != len(options):
        selected = get_menu_option("Menú de Egresos", options)

        # Crear
        if selected == 1:
            expense_id = str(random.randint(1000, 9999))
            amount = input_float("Ingrese el monto: ")
            category = choose_category(expense_categories)
            date = input_date("Ingrese la fecha en formato (dd/mm/yyyy): ")
            expense = {
                "id": expense_id,
                "amount": amount,
                "category": category,
                "date": date,
                "user": current_username
            }
            ok = insertExpenses(expense)
            if ok:
                print("Egreso agregado.")
            else:
                print("No se pudo agregar el egreso (amount debe ser mayor a 0).")

        # Actualizar
        elif selected == 2:
            expense_id = input_non_empty("ID del egreso a actualizar: ")
            amount = input_float("Nuevo monto: ")
            category = choose_category(expense_categories)
            date = input_date("Nueva fecha (dd/mm/yyyy): ")
            expense = {
                "id": expense_id,
                "amount": amount,
                "category": category,
                "date": date,
                "user": current_username
            }
            ok = updateExpenses(expense)
            if ok:
                print("Egreso actualizado.")
            else:
                print("No se encontró el egreso para actualizar.")

        # Eliminar
        elif selected == 3:
            expense_id = input_non_empty("ID del egreso a eliminar: ")
            ok = deleteExpenses({"id": expense_id})
            if ok:
                print("Egreso eliminado.")
            else:
                print("No se encontró el egreso para eliminar.")

        # Listar
        elif selected == 4:
            items = getExpensesByUser(current_username)
            if not items:
                print("No hay egresos para este usuario.")
            else:
                print("\nEgresos del usuario actual:")
                for i in range(len(items)):
                    it = items[i]
                    print(f"- [{it['id']}] {it['date']} | {it['category']} | {it['amount']}")

        elif selected == 5:
            print("Volviendo al menú principal...")


## BASES DE DATOS ##

def metrics_menu(current_username):
    options = [
        "Calcular ahorro mensual",
        "Comparar ahorro entre dos meses",
        "Porcentaje de gasto por categoría",         
        "Volver"
    ]

    selected = 0
    while selected != len(options):
        selected = get_menu_option("Menú de Métricas", options)

        # Calcular ahorro mensual
        if selected == 1:
            print("\n--- Calcular Ahorro Mensual ---")
            month = 0
            while not (1 <= month <= 12):
                month_str = input("Ingrese el mes (1-12): ")
                if month_str.isdigit():
                    month = int(month_str)
                if not (1 <= month <= 12):
                    print("Error: debe ingresar un mes válido (1-12).")
            
            year = 0
            while not (year > 1900):
                year_str = input("Ingrese el año (ej: 2024): ")
                if year_str.isdigit():
                    year = int(year_str)
                if not (year > 1900):
                    print("Error: debe ingresar un año válido (mayor a 1900).")

            savings = calculate_monthly_savings(current_username, month, year)
            savings_formatted = int(savings * 100) / 100.0
            print(f"\nEl ahorro para el mes {month} en el año {year} fue de: ${savings_formatted}")

        # Comparar ahorro
        elif selected == 2:    
            print("\n--- Comparar Ahorro Entre Dos Meses ---")
            print("-- Primer Período --")
            month1 = 0
            while not (1 <= month1 <= 12):
                month1_str = input("Ingrese el mes (1-12): ")
                if month1_str.isdigit():
                    month1 = int(month1_str)
                if not (1 <= month1 <= 12):
                    print("Error: debe ingresar un mes válido (1-12).")
            year1 = 0
            while not (year1 > 1900):
                year1_str = input("Ingrese el año (ej: 2023): ")
                if year1_str.isdigit():
                    year1 = int(year1_str)
                if not (year1 > 1900):
                    print("Error: debe ingresar un año válido (mayor a 1900).")

            print("\n--- Segundo Período ---")
            month2 = 0
            while not (1 <= month2 <= 12):
                month2_str = input("Ingrese el mes (1-12): ")
                if month2_str.isdigit():
                    month2 = int(month2_str)
                if not (1 <= month2 <= 12):
                    print("Error: debe ingresar un mes válido (1-12).")
            year2 = 0
            while not (year2 > 1900):
                year2_str = input("Ingrese el año (ej: 2024): ")
                if year2_str.isdigit():
                    year2 = int(year2_str)
                if not (year2 > 1900):
                    print("Error: debe ingresar un año válido (mayor a 1900).")
            
            change = percent_change_in_savings(current_username, month1, year1, month2, year2)

            if change is None:
                print("\nNo se puede calcular el cambio porcentual (el ahorro del primer período fue cero).")
            else:
                change_formatted = int(change * 100) / 100.0
                if change > 0:
                    print(f"\nHubo un aumento del {change_formatted}% en el ahorro.")
                elif change < 0:
                    decrease_formatted = int((change * -1) * 100) / 100.0
                    print(f"\nHubo una disminución del {decrease_formatted}% en el ahorro.")
                else:
                    print("\nNo hubo cambios en el ahorro entre los dos períodos.")

        elif selected == 3:
            print("\n--- Porcentaje de Gasto por Categoría ---")
            month = 0
            while not (1 <= month <= 12):
                month_str = input("Ingrese el mes (1-12): ")
                if month_str.isdigit():
                    month = int(month_str)
                if not (1 <= month <= 12):
                    print("Error: debe ingresar un mes válido (1-12).")

            year = 0
            while not (year > 1900):
                year_str = input("Ingrese el año (ej: 2024): ")
                if year_str.isdigit():
                    year = int(year_str)
                if not (year > 1900):
                    print("Error: debe ingresar un año válido (mayor a 1900).")

            percentages = average_expense_by_category(current_username, month, year)
    
            if not percentages:
                print(f"\nNo hay egresos para el mes {month}/{year}.")
            else:
                print(f"\nPorcentaje de gasto por categoría en la fecha: {month}/{year}:")
                for categoria, porcentaje in percentages.items():
                    print(f"- {categoria}: {porcentaje:.2f}%")
    

        elif selected == 4:
            print("Volviendo al menú principal...")



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
    
    # Menú principal
    main_options = [
        "Ingresos",
        "Egresos",
        "Métricas",
        "Salir"
    ]

    selected = 0
    while selected != len(main_options):
        selected = get_menu_option("Menú principal", main_options)

        if selected == 1:
            incomes_menu(username)
        elif selected == 2:
            expenses_menu(username)
        elif selected == 3:
            metrics_menu(username)
        elif selected == 4:
            print("Saliendo...")


#### INICIO DE PROGRAMA
ensure_db_files()
main()