from db import (
    ensure_db_files,
    income_categories, 
    expense_categories,
    incomes_insert, 
    incomes_id_is_valid,
    incomes_update, 
    incomes_delete, 
    incomes_by_user, 
    expenses_insert,
    expenses_id_is_valid,
    expenses_update, 
    expenses_delete, 
    expenses_by_user,
    users_insert,
    login_check,
    users_find_by_name,
    goals_insert,
    goals_id_is_valid,
    goals_update,
    goals_delete,
    goals_by_user,
    load_sample_data
)
#utils
from utils import(
    get_menu_option,
    input_float,
    input_non_empty,
    input_date,
    input_validation_age,
    choose_category,
    input_period,
    input_password,
    COLORS
)
#service
from service import (
    calculate_monthly_savings,
    percent_change_in_savings, 
    average_expense_by_category,
    build_dashboard_metrics

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
    ok, message = incomes_insert(income)
    return ok, message


def updateIncome(income):
    '''
    Este método recibe un ingreso de tipo dict
    Realiza el update a ravés de una funcion de db.py
    Reemplaza el ingreso anterior con el nuevo
    Devuelve True en caso de éxito, False en caso de error
    '''
    ok, message = incomes_update(income)
    return ok, message

def deleteIncome(income):
    '''
    Este método recibe un income de tipo dict, 
    Extrae el id y borra en base de datos el valor de income que coincida con ese id
    Esto lo hace a través de una funcion de db.py
    Devuelve True en caso de éxito, False en caso de error
    '''
    income_id = income.get("id")
    ok, message = incomes_delete(income_id)
    return ok, message
    

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
    ok, message = expenses_insert(expense)
    return ok, message
    

def updateExpenses(expense):
    '''
    Este método recibe un egreso de tipo dict.
    Realiza el update a través de una función de db.py,
    reemplazando el egreso anterior con el nuevo (mismo id).
    Devuelve True en caso de éxito, False en caso de error.
    '''
    ok, message = expenses_update(expense)
    return ok, message

def deleteExpenses(expense):
    '''
    Este método recibe un egreso de tipo dict,
    extrae el id y borra en base de datos el egreso que coincida con ese id,
    utilizando una función de db.py.
    Devuelve True en caso de éxito, False en caso de error.
    '''
    expense_id = expense.get("id")
    ok, message = expenses_delete(expense_id)
    return ok, message

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
    Este método recibe un objetivo de ahorro de tipo dict
    y lo inserta en la base de datos a través de una función de db.py.
    Devuelve True en caso de éxito, False en caso de error.
    '''
    ok, message = goals_insert(goal)
    return ok, message

def updateGoals(goal):
    '''
    Este método recibe un objetivo de ahorro de tipo dict.
    Realiza el update a través de una función de db.py,
    reemplazando el objetivo de ahorro anterior con el nuevo (mismo id).
    Devuelve True en caso de éxito, False en caso de error.
    '''
    ok, message = goals_update(goal)
    return ok, message

def deleteGoals(goal):
    '''
    Este método recibe un objetivo de ahorro de tipo dict,
    extrae el id y borra en base de datos el objetivo de ahorro que coincida con ese id,
    utilizando una función de db.py.
    Devuelve True en caso de éxito, False en caso de error.
    '''
    goal_id = goal.get("id")
    ok, message = goals_delete(goal_id)
   
    return ok, message

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
            ok, message = insertIncome(income)
            print("Ingreso agregado." if ok else message)
        # Actualizar
        elif selected == 2:
            income_id = input_non_empty("ID del ingreso a actualizar: ")
            income_id_validated = incomes_id_is_valid(income_id)

            while not income_id_validated:
                income_id = input_non_empty("ID del ingreso a actualizar: ")
                income_id_validated = incomes_id_is_valid(income_id)
            
            amount = input_float("Ingrese el monto del nuevo ingreso: ")
            category = choose_category(income_categories)
            date = input_date("Nueva fecha (dd/mm/yyyy): ")
            income = {
                "id": income_id,
                "amount": amount,
                "category": category,
                "date": date,
                "user": current_username
            }

            ok, message = updateIncome(income)
            print("Ingreso actualizado." if ok else message)

        # Eliminar
        elif selected == 3:
            income_id = input_non_empty("ID del income a eliminar: ")
            ok, message = deleteIncome({"id": income_id})
            print("Ingreso eliminado." if ok else message)
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
            ok, message = insertExpenses(expense)
            print("Egreso agregado." if ok else message)

        # Actualizar
        elif selected == 2:
            expense_id = input_non_empty("ID del egreso a actualizar: ")
            expense_id_validated = expenses_id_is_valid(expense_id)

            while not expense_id_validated:
                expense_id = input_non_empty("ID del egreso a actualizar: ")
                expense_id_validated = expenses_id_is_valid(expense_id)

            amount = input_float("Ingrese el monto del nuevo egreso: ")
            category = choose_category(expense_categories)
            date = input_date("Nueva fecha (dd/mm/yyyy): ")
            expense = {
                "id": expense_id,
                "amount": amount,
                "category": category,
                "date": date,
                "user": current_username
            }
            ok, message = updateExpenses(expense)
            print("Egreso actualizado." if ok else message)

        # Eliminar
        elif selected == 3:
            expense_id = input_non_empty("ID del egreso a eliminar: ")
            ok, message = deleteExpenses({"id": expense_id})
            print("Egreso eliminado." if ok else message)

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


def _show_dashboard_details(metrics, username):
    month = metrics["month"]
    year = metrics["year"]
    prev_month = metrics["prev_month"]
    prev_year = metrics["prev_year"]

    total_in_all = metrics["total_in_all"]
    total_out_all = metrics["total_out_all"]
    savings_all = metrics["savings_all"]

    total_in = metrics["total_in"]
    total_out = metrics["total_out"]
    savings_current = metrics["savings_current"]
    savings_prev = metrics["savings_prev"]
    change_pct = metrics["change_pct"]
    goals_info = metrics["goals"]
    dist = metrics["expenses_distribution"]

    # Extraer colores del diccionario para un uso más fácil
    GREEN, RED, BLUE, CYAN, YELLOW, MAGENTA, BOLD, RESET = COLORS.values()
    print("\n" + "=" * 60)
    print(f"{BOLD}{CYAN}DASHBOARD FINANCIERO - Usuario: {username}{RESET}")
    print("=" * 60)

    # --- Resumen Histórico (Azul) ---
    print(f"\n{BLUE}{BOLD}Resumen histórico:{RESET}")
    if total_in_all == 0.0 and total_out_all == 0.0:
        print("- No hay datos de ingresos ni egresos aún.")
    else:
        print(f"- Total ingresado: {GREEN}${total_in_all:.2f}{RESET}")
        print(f"- Total egresado:  {RED}${total_out_all:.2f}{RESET}")
        color_saving_all = GREEN if savings_all >= 0 else RED
        print(f"- Ahorro histórico: {color_saving_all}${savings_all:.2f}{RESET}")

    # --- Comparación (Cian) ---
    print(f"\n{CYAN}{BOLD}Comparación vs. mes anterior ({prev_month}/{prev_year}):{RESET}")
    if savings_prev == 0.0 and savings_current == 0.0:
        print("- No hay datos suficientes para comparar (ambos meses sin ahorro).")
    else:
        print(f"- Ahorro mes anterior: ${savings_prev:.2f}")
        if change_pct is None:
            print("- Cambio porcentual: no se puede calcular (ahorro anterior = 0)")
        else:
            sign_color = GREEN if change_pct >= 0 else RED
            print(f"- Cambio porcentual: {sign_color}{change_pct:.2f}%{RESET}")

    # --- Metas de Ahorro (Amarillo) ---
    print(f"\n{YELLOW}{BOLD}Metas de ahorro:{RESET}")
    if goals_info["total_goals"] == 0:
        print("- No hay objetivos de ahorro registrados.")
    else:
        print(f"- Total metas: {goals_info['total_goals']}")
        print(f"- Completadas: {goals_info['goals_completed']}")
        print(f"- En progreso: {goals_info['goals_in_progress']}")
        print(f"- No iniciadas: {goals_info['goals_not_started']}")
        print("\n  Detalle:")

        # Lógica para la barra de progreso
        max_bar_width = 20
        bar_char = "■"

        for g in goals_info["details"]:
            progress_pct = g["progress_pct"]
            num_blocks = int((progress_pct / 100) * max_bar_width)
            bar_color = GREEN if progress_pct >= 100 else YELLOW
            bar = bar_color + (bar_char * num_blocks) + RESET

            print(
                f"  · {g['name']:<20} ({g['progress_pct']:.1f}%)"
                f"\n    {bar} | Meta: ${g['total_amount']:.2f} | Ahorrado: ${g['saved_amount']:.2f}"
            )

    # --- Distribución de Gastos (Azul) ---
    print(f"\n{BLUE}{BOLD}Distribución de gastos por categoría ({month}/{year}):{RESET}")
    if not dist:
        print("- No hay egresos registrados para el mes actual.")
    else:
        max_bar_width = 25
        bar_char = "■"

        for categoria, porcentaje in dist.items():
            num_blocks = int((porcentaje / 100) * max_bar_width)
            bar = bar_char * num_blocks
            print(f"  · {categoria:<15} | {BLUE}{bar}{RESET} {porcentaje:.2f}%")

    print("\n" + "=" * 60 + "\n")

def show_dashboard_plain(username):
    metrics = build_dashboard_metrics(username)

    month = metrics["month"]
    year = metrics["year"]

    total_in = metrics["total_in"]
    total_out = metrics["total_out"]
    savings_current = metrics["savings_current"]

    # Extraer colores del diccionario para un uso más fácil
    GREEN, RED, BLUE, CYAN, YELLOW, MAGENTA, BOLD, RESET = COLORS.values()

    print("\n" + "=" * 60)
    print(f"{BOLD}{CYAN}RESUMEN FINANCIERO - Usuario: {username}{RESET}")
    print("=" * 60)

    # --- Resumen Mes Actual (Magenta) ---
    print(f"\n{MAGENTA}{BOLD}Resumen mes actual ({month}/{year}):{RESET}")
    if total_in == 0.0 and total_out == 0.0:
        print("- No hay movimientos en el mes actual.")
    else:
        print(f"- Ingresos:  {GREEN}${total_in:.2f}{RESET}")
        print(f"- Egresos:   {RED}${total_out:.2f}{RESET}")
        color_saving = GREEN if savings_current >= 0 else RED
        print(f"- Ahorro:    {color_saving}${savings_current:.2f}{RESET}")

    # Preguntar al usuario si quiere ver el informe completo
    choice = get_menu_option("¿Desea ver el informe completo?", ["Sí", "No"])
    if choice == 1:
        _show_dashboard_details(metrics, username)

def metrics_menu(current_username):
    options = [
        "Ver métricas generales",
        "Calcular ahorro mensual",
        "Comparar ahorro entre dos meses",
        "Porcentaje de gasto por categoría",
        "Volver"
    ]

    selected = 0
    while selected != len(options):
        selected = get_menu_option("Menú de Métricas", options)

        # 1 - Dashboard general
        if selected == 1:
            show_dashboard_plain(current_username)

        # 2 - Calcular ahorro mensual
        elif selected == 2:
            print("\n--- Calcular Ahorro Mensual ---")
            month, year = input_period("Ingrese el período a calcular:")
            savings = calculate_monthly_savings(current_username, month, year)
            savings_formatted = int(savings * 100) / 100.0
            print(f"\nEl ahorro para el mes {month} en el año {year} fue de: ${savings_formatted}")

        # 3 - Comparar ahorro
        elif selected == 3:
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

        # 4 - Porcentaje de gasto por categoría
        elif selected == 4:
            print("\n--- Porcentaje de Gasto por Categoría ---")
            month, year = input_period("Ingrese el período a analizar:")
            percentages = average_expense_by_category(current_username, month, year)

            if not percentages:
                print(f"\nNo hay egresos para el mes {month}/{year}.")
            else:
                print(f"\nPorcentaje de gasto por categoría en la fecha: {month}/{year}:")
                for categoria, porcentaje in percentages.items():
                    print(f"- {categoria}: {porcentaje:.2f}%")

        elif selected == 5:
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
            goal_end_date = input_date("Ingrese la fecha en formato (dd/mm/yyyy) de finalizacion de su objetivo: ")
            goal_status = "Iniciado"

            goal = {
                "name": goal_name,
                "category": goal_category,
                "total_amount": goal_total_amount,
                "saved_amount": goal_saved_amount,
                "end_date": goal_end_date,
                "status": goal_status,
                "user": current_username
            }

            ok, message = insertGoals(goal)
            print("Objetivo de ahorro creado." if ok else message)
        # Modificar un objetivo de ahorro
        elif selected == 2:
            goal_id = input_non_empty("ID del objetivo de ahorro a actualizar: ")
            goal_id_validated = goals_id_is_valid(goal_id)

            while not goal_id_validated:
                goal_id = input_non_empty("ID del objetivo de ahorro a actualizar: ")
                goal_id_validated = goals_id_is_valid(goal_id)

            goal_name = input_non_empty("Ingrese el nombre del objetivo: ")
            goal_category = choose_category(goal_categories)
            goal_total_amount = input_float("Ingrese el monto del objetivo (meta total): ")
            goal_saved_amount = input_float("Ingrese el monto que desea guardar: ")
            goal_end_date = input_date("Nueve fecha final (dd/mm/yyyy) de su objetivo: ")
            goal_status = "Iniciado"

            goal = {
                "id": goal_id,
                "name": goal_name,
                "category": goal_category,
                "total_amount": goal_total_amount,
                "saved_amount": goal_saved_amount,
                "end_date": goal_end_date,
                "status": goal_status,
                "user": current_username
            }

            ok, message = updateGoals(goal)
            print("Objetivo de ahorro actualizado." if ok else message)
        # Eliminar Objetivo de ahorro
        elif selected == 3:
            goal_id = input_non_empty("ID del objetivo a eliminar: ")
            ok, message = deleteGoals({"id": goal_id})
            print("Objetivo de ahorro eliminado." if ok else message)
        # Listar Objetivo de ahorro
        elif selected == 4:
            items = getGoalsByUser(current_username)
            if not items:
                print("No hay objetivos de ahorro para este usuario.")
            else:
                print("\nObjetivos de ahorro del usuario actual:")
                for i in range(len(items)):
                    it = items[i]
                    print(f"- [{it['id']}] | {it['name']} | {it['category']} | {it['total_amount']} | {it['saved_amount']} | {it['start_date']} | {it['end_date']} | {it['status']}")
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
        age, validation_age = input_validation_age()
        if validation_age:
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

    # 1. Mostrar el dashboard justo después de iniciar sesión
    print("\nCargando tu dashboard...")
    show_dashboard_plain(username)
    
    # Menú principal
    main_options = [
        "Ver Dashboard",
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
            show_dashboard_plain(username)
        elif selected == 2:
            incomes_menu(username)
        elif selected == 3:
            expenses_menu(username)
        elif selected == 4:
            metrics_menu(username)
        elif selected == 5:
            goals_menu(username)
        elif selected == 6:
            print("Saliendo...")

#### INICIO DE PROGRAMA
#ensure_db_files()
# para pruebas comentar ensure_db_files() y dscomentar load_sample_data()
load_sample_data() 
main()