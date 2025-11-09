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
    users_insert,
    login_check,
    users_find_by_name,
    goals_insert,
    goals_update,
    goals_delete,
    goals_by_user,
)
#utils
from utils import(
   get_menu_option,
    input_float,
    input_non_empty,
    input_date,
    input_int,
    choose_category,
    input_period,
    convert_to_tuple,
    input_password
)
#service
from service import (
    calculate_monthly_savings,
    percent_change_in_savings, 
    average_expense_by_category

)
import getpass

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

## Ingresos y egresos, van a tener la misma interfaz
# hay lista de ingresos y de egresos, y tienen las siguientes propiedades
# - id: string (debe ser único)
# - amount: number
# - category: categorias (vamos a definir un listado fijo de categorias de ingreso y de egreso)
# - date: "dd/mm/yyyy" (pueden ingresarse fechas que no sean la actual)
# - user: string (se debe guardar automaticamente con el valor del nombre o el id del usuario que realice la carga)
# Ejemplo de valor correcto para un ingreso o egreso: entidad = { "id": "1", "amount": 1800.0, "category": "Other", "date": "08/06/2025", "user": "admin" }

## Objetivos de ahorro
# hay lista de objetivos de ahorro, y tienen las siguientes propiedades
# - id: string (debe ser único)
# - category: categorias (vamos a definir un listado fijo de categorias de objetivos de ahorro)
# - total_amount: float (Monto total del objetivo de ahorro)
# - saved_amount: float (Monto total que decide guardar el usuario)
# - start_date: "dd/mm/yyyy" (fecha inicio)
# - end_date: "dd/mm/yyyy" (fecha final)
# - status: string (Puede tomar los valores de "Iniciado", "En proceso" y "Completado")
# - user: string (se debe guardar automaticamente con el valor del nombre o el id del usuario que realice la carga)

goal_categories = ["Viaje", "Vivienda", "Electrodomesticos", "Educacion", "Otros"]

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

# ABM OBJETIVOS DE AHORRO
def insertGoals(goal):
    '''
    Este método recibe un egreso de tipo dict
    y lo inserta en la base de datos a través de una función de db.py.
    Devuelve True en caso de éxito, False en caso de error.
    '''
    # TODO: pasar validaciones a db.py

    # Validar monto total del objetivo
    if goal.get("total_amount") <= 0:
        print("Error: el monto total debe ser mayor a 0.")
        return False

    # Validar monto a guardar del objetivo
    if goal.get("saved_amount") > goal.get("total_amount"):
        print("Error: el monto guardado no puede superar el monto total del objetivo")
        return False

    # Validar fecha final del objetivo
    goal_start_date = goal.get("start_date")
    goal_end_date = goal.get("end_date")

    fecha_inicio_goal = convert_to_tuple(goal_start_date)
    fecha_fin_goal = convert_to_tuple(goal_end_date)

    if fecha_fin_goal and fecha_inicio_goal and (fecha_fin_goal[2], fecha_fin_goal[1], fecha_fin_goal[0]) < (fecha_inicio_goal[2], fecha_inicio_goal[1], fecha_inicio_goal[0]):
        print("Error: la fecha final no puede ser anterior a la fecha de inicio.")
        return False
   
    # Si todas las validaciones pasan intenta insertar en lista
    ok, _ = goals_insert(goal)
    if not ok:
        print("Error al guardar en base de datos.")
        return False
    
    print("Objetivo de ahorro creado correctamente.")
    return True

def updateGoals(goal):
    '''
    Este método recibe un objetivo de ahorro de tipo dict.
    Realiza el update a través de una función de db.py,
    reemplazando el objetivo de ahorro anterior con el nuevo (mismo id).
    Devuelve True en caso de éxito, False en caso de error.
    '''
    ok, _ = goals_update(goal)
    return ok

def deleteGoals(goal):
    '''
    Este método recibe un objetivo de ahorro de tipo dict,
    extrae el id y borra en base de datos el objetivo de ahorro que coincida con ese id,
    utilizando una función de db.py.
    Devuelve True en caso de éxito, False en caso de error.
    '''
    goal_id = goal.get("id")
    ok, _ = goals_delete(goal_id)
   
    return ok

def getGoalsByUser(username):
    '''
    Este método recibe el nombre de un usuario de tipo str
    Usa una función de db.py que busca todos los goals pertenecientes a ese usuario
    Devuelve una lista de goals, si el usuario no existe o no tiene goals devuelve una lista vacia.
    '''
    return goals_by_user(username)

# AUTH

def register_user(name, password, password2, age, genre, role="user"):
    '''
    Recibe un name, password, password2, age, genre y role de tipo str
    Valida que el usuario exista, que las contraseñas sean iguales
    Usa un método de db.json para hacer el insert
    Si todo sale bien, devuelve un True
    Si alguna validación falla o falla el guardado en db devuelve False
    '''

    _, user_exist = users_find_by_name(name)
    if user_exist:
        print("El usuario ya existe. Intente con otro nombre.")
        return False
    
    if password != password2:
        print("Las contraseñas no coinciden. Intente nuevamente.")
        return False
    
    new_user = {
        "name": name,
        "password": password,
        "age": age,
        "genre": genre,
        "role": role
    }

    ok = users_insert(new_user)
    if ok :
        return True
    
    print("ERROR: no se pudo registrar el usuario.")
    return False

def login(name, password):
    """
    Redibe un name y password de tipo str
    Valida que el usuario exista y que la contraseña ingresada sea correcta.
    Retorna True si el usuario existe y coincide la contraseña, retorna False si no coinciden o no existe
    """
    login_success = login_check(name, password)
    if login_success: 
        print("Acceso concedido.")
    else:
        print("Error: credenciales incorrectas o usuario no existente")
    return login_success


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
            amount = input_float("Ingrese el monto: ")
            category = choose_category(income_categories)
            date = input_date("Ingrese la fecha en formato (dd/mm/yyyy): ")
            income = {
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
            amount = input_float("Ingrese el monto: ")
            category = choose_category(expense_categories)
            date = input_date("Ingrese la fecha en formato (dd/mm/yyyy): ")
            expense = {
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
            month, year = input_period("Ingrese el período a calcular:")
            savings = calculate_monthly_savings(current_username, month, year)
            savings_formatted = int(savings * 100) / 100.0
            print(f"\nEl ahorro para el mes {month} en el año {year} fue de: ${savings_formatted}")

        # Comparar ahorro
        elif selected == 2:    
            print("\n--- Comparar Ahorro Entre Dos Meses ---")
            month1, year1 = input_period("-- Primer Período --")
            month2, year2 = input_period("\n-- Segundo Período --")
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
            month, year = input_period("Ingrese el período a analizar:")
            percentages = average_expense_by_category(current_username, month, year)
    
            if not percentages:
                print(f"\nNo hay egresos para el mes {month}/{year}.")
            else:
                print(f"\nPorcentaje de gasto por categoría en la fecha: {month}/{year}:")
                for categoria, porcentaje in percentages.items():
                    print(f"- {categoria}: {porcentaje:.2f}%")
    

        elif selected == 4:
            print("Volviendo al menú principal...")

def goals_menu(current_username):
    options = [
        "Agregar objetivo de ahorro",
        "Modificar objetivo de ahorro",
        "Eliminar objetivo de ahorro",
        "Listar todos mis objetivo de ahorros",
        "Volver"
    ]

    selected = 0
    while selected != len(options):
        selected = get_menu_option("Menú de Objetivos de ahorro", options)

        # Crear objetivo de ahorro
        if selected == 1:
            goal_name = input_non_empty("Ingrese el nombre del objetivo: ")
            goal_category = choose_category(goal_categories)
            goal_total_amount = input_float("Ingrese el monto del objetivo (meta total): ")
            goal_saved_amount = input_float("Ingrese el monto que desea guardar: ")
            goal_start_date = input_date("Ingrese la fecha en formato (dd/mm/yyyy) del inicio de su objetivo: ")
            goal_end_date = input_date("Ingrese la fecha en formato (dd/mm/yyyy) de finalizacion de su objetivo: ")
            goal_status = "Iniciado"

            goal = {
                "name": goal_name,
                "category": goal_category,
                "total_amount": goal_total_amount,
                "saved_amount": goal_saved_amount,
                "start_date": goal_start_date,
                "end_date": goal_end_date,
                "status": goal_status,
                "user": current_username
            }

            ok = insertGoals(goal)
        # Modificar un objetivo de ahorro
        elif selected == 2:
            goal_id = input_non_empty("ID del objetivo de ahorro a actualizar: ")
            goal_name = input_non_empty("Ingrese el nombre del objetivo: ")
            goal_category = choose_category(goal_categories)
            goal_total_amount = input_float("Ingrese el monto del objetivo (meta total): ")
            goal_saved_amount = input_float("Ingrese el monto que desea guardar: ")
            goal_start_date = input_date("Nueve fecha incial (dd/mm/yyyy) de su objetivo: ")
            goal_end_date = input_date("Nueve fecha final (dd/mm/yyyy) de su objetivo: ")
            goal_status = "Iniciado"

            goal = {
                "id": goal_id,
                "name": goal_name,
                "category": goal_category,
                "total_amount": goal_total_amount,
                "saved_amount": goal_saved_amount,
                "start_date": goal_start_date,
                "end_date": goal_end_date,
                "status": goal_status,
                "user": current_username
            }

            ok = updateGoals(goal)
            print("Ingreso actualizado." if ok else "No se encontró el objetivo para actualizar.")
        # Eliminar Objetivo de ahorro
        elif selected == 3:
            goal_id = input_non_empty("ID del egreso a eliminar: ")
            ok = deleteGoals({"id": goal_id})
            if ok:
                print("Objetivo de ahorro eliminado.")
            else:
                print("No se encontró el objetivo de ahorro para eliminar.")
        # Listar Objetivo de ahorro
        elif selected == 4:
            items = getGoalsByUser(current_username)
            if not items:
                print("No hay objetivos de ahorro para este usuario.")
            else:
                print("\nObjetivos de ahorro del usuario actual:")
                for i in range(len(items)):
                    it = items[i]
                    print(f"- [{it['id']}] {it['category']} | {it['total_amount']} | {it['saved_amount']} | {it['start_date']} | {it['end_date']} | {it['status']}")
        # Volver al menú principal
        elif selected == 5:
            print("Volviendo al menú principal...")

def main():

#### INICIO DE PROGRAMA--------



# --- FLUJO DE REGISTRO / LOGIN ---

    print("Bienvenido al sistema de finanzas.")

    #TODO: toda la perte de usuarios hasta 858 (print("resultado: Auteticacion exitosa")) se crea funcion para modularizar el menu de auth crear funcion auth_menu o dividr registro y login.

    is_register = get_menu_option("¿Ya posee una cuenta? (si/no): ", ["si", "no"])
    
    while is_register == 2:
        print("\n--- REGISTRO DE NUEVO USUARIO ---")
        username = input_non_empty("Ingrese nombre de usuario: ")

        # Contraseña y confirmacion
        password = input_password()
        password2 = input_password("Confirme contraseña: ")
        while password != password2:
            print("Las contraseñas no coinciden. Intente nuevamente.")
            password = input_password()#la vuelov a pedir
            password2 = input_password("Confirme contraseña: ")

        # Edad y genero
        age = input_int("Ingrese edad: ")
        genre_option = get_menu_option("Ingrese genero (masculino/femenino/otro): ", ["masculino", "femenino", "otro"])
        genre = ""
        if genre_option == 1:
            genre = "M"
        elif genre_option == 2:
            genre = "F"
        else:
            genre = "X"
        # Intentar registrar usuario
        ok = register_user(username, password, password2, age, genre)
        if ok:
            print(" Registro completado correctamente.")
            is_register = 1
        else:
            print(" No se pudo completar el registro. Vamos a intentarlo de nuevo.\n")


    # --- LOGIN ---
    print("Bienvenido al sistema de finanzas.\n")
    username = input_non_empty("Ingrese nombre de usuario: ")
    password = getpass.getpass("Ingrese contraseña: ")

    isLogged = login(username, password)
    while not isLogged:
        username = input("Ingrese nombre de usuario: ")
        password = getpass.getpass("Ingrese contraseña: ")
        isLogged = login(username, password)

    print("resultado: Auteticacion exitosa")
    
    # Menú principal
    main_options = [
        "Ingresos",
        "Egresos",
        "Métricas",
        "Objetivos de ahorros",
        "Salir"
    ]

    selected = 0
    while selected != len(main_options):
        selected = get_menu_option("Menu principal", main_options)

        if selected == 1:
            incomes_menu(username)
        elif selected == 2:
            expenses_menu(username)
        elif selected == 3:
            metrics_menu(username)
        elif selected == 4:
            goals_menu(username)
        elif selected == 5:
            print("Saliendo...")

#### INICIO DE PROGRAMA
ensure_db_files()
main()