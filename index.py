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


incomes = [
    # Datos de prueba para el usuario 'admin'
    {"id": "1001", "amount": 50000.0, "category": "Salario", "date": "05/06/2024", "user": "admin"},
    {"id": "1002", "amount": 5000.0, "category": "Regalo", "date": "15/06/2024", "user": "admin"},
    {"id": "1003", "amount": 52000.0, "category": "Salario", "date": "05/07/2024", "user": "admin"},
]
income_categories = ["Salario", "Regalo", "Otros"]

expenses = [
    # Datos de prueba para el usuario 'admin'
    {"id": "2001", "amount": 10000.0, "category": "Supermercado", "date": "10/06/2024", "user": "admin"},
    {"id": "2001", "amount": 15000.0, "category": "Supermercado", "date": "15/06/2024", "user": "admin"},
    {"id": "2003", "amount": 12000.0, "category": "Supermercado", "date": "10/06/2024", "user": "admin"},
    {"id": "2003", "amount": 2000.0, "category": "Otros", "date": "10/06/2024", "user": "admin"},
    {"id": "2002", "amount": 3000.0, "category": "Transporte", "date": "20/06/2024", "user": "admin"},
    {"id": "2004", "amount": 105000.0, "category": "Vivienda", "date": "15/06/2024", "user": "admin"},
]
expense_categories = ["Supermercado", "Vivienda", "Transporte", "Otros"]

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

goals = [
    # Datos de prueba para el usuario 'admin'
    {"id": "1001", "category": "Viaje", "total_amount": 25000.0, "saved_amount": 23000.0, "start_date": "10/06/2024", "end_date": "10/10/2024", "status": "Iniciado", "user": "admin"},
    {"id": "1002", "category": "Vivienda", "total_amount": 150000.0, "saved_amount": 40000.0, "start_date": "10/06/2024", "end_date": "10/10/2024",  "status": "Iniciado", "user": "admin"},
    {"id": "1003", "category": "Otros", "total_amount": 50000.0, "saved_amount": 10000.0, "start_date": "10/06/2024", "end_date": "10/10/2024",  "status": "Iniciado", "user": "admin"},
]
goal_categories = ["Viaje", "Vivienda", "Electrodomesticos", "Educacion", "Otros"]

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
    Este método recibe el nombre de un usuario y filtra la lista 
    para devolver todos los ingresos de ese usuario.
    '''
    found_incomes = list(filter(lambda income: income.get("user") == username, incomes))

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
    Este método recibe el nombre de un usuario y filtra la lista 
    para devolver todos los agresos de ese usuario.
    '''
    found_expenses = list(filter(lambda expense: expense.get("user") == username, expenses))

    return found_expenses

# ABM OBJETIVOS DE AHORRO
def insertGoals(goal):
    '''
        Este método recibe un objetivo de ahorro, se asegura que sea un objetivo válido
        y lo inserta en la lista de objetivos de ahorros.

        Devuelve un número de error o 0 si se insertó correctamente.

        0 = OK
        1 = Monto objetivo (<= 0)
        2 = Monto guardado (< 0)
        3 = Fecha final anterior a fecha de inicio
    '''
    
    # Validar monto total del objetivo
    if goal.get("total_amount") <= 0:
        return 1

    # Validar monto a guardar del objetivo
    if goal.get("saved_amount") > goal.get("total_amount"):
        return 2

    # Validar fecha final del objetivo
    goal_start_date = goal.get("start_date")
    goal_end_date = goal.get("end_date")

    fecha_inicio_goal = convert_to_tuple(goal_start_date)
    fecha_fin_goal = convert_to_tuple(goal_end_date)

    if fecha_fin_goal and fecha_inicio_goal and (fecha_fin_goal[2], fecha_fin_goal[1], fecha_fin_goal[0]) < (fecha_inicio_goal[2], fecha_inicio_goal[1], fecha_inicio_goal[0]):
        return 3
   
    # Si todas las validaciones pasan insertar en lista
    goals.append(goal)
    return 0 

def updateGoals(goal):
    '''
    Este método recibe un objetivo de ahorro, se asegura que sea un objetivo de ahorro válido y que exista en la lista de objetivos de ahorro reemplaza el objetivo de ahorro anterior con el nuevo
    '''
    for i in range(len(goals)):
        if goals[i].get("id") == goal.get("id"):
            goals[i] = goal
            return True
    return False

def deleteGoals(goal):
    '''
    Este método recibe el id de un objetivo de ahorrro, se asegura que exista en la lista de objetivos de ahorro
    elimina el objetivo de ahorrro correspondiente al id
    '''
    for i in range(len(goals)):
        if goals[i].get("id") == goal.get("id"):
            goals.pop(i)
            return True
    return False

def getGoalsByUser(username):
    '''
    Este método recibe el nombre de un usuario y filtra la lista 
    para devolver todos los objetivos de ahorro de ese usuario.
    '''
    found_goals = list(filter(lambda goal: goal.get("user") == username, goals))
    print(found_goals)

    return found_goals
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


def registrar_usuario(users, name, password, password2, age, genre, role="user"):
    
    #Registra un nuevo usuario despues de validar que no exista y que las contraseñas coincidan.
       #Verifica si el usuario ya existe en la lista.
        # - Compara que ambas contraseñas coincidan.
        #- Agrega el nuevo usuario a la lista "users".
        #crear un nuevo diccionario con el nuevo usuario 

    #Retorna:
       # Lista de usuarios actualizada (con el nuevo usuario).
    
    # Validar si el usuario ya existe
    if validar_existenciauser(users, name):
        print("El usuario ya existe. Intente con otro nombre.")
        return users,False
    

    # Validar que las contraseñas coincidan
    if password != password2:
        print("Las contraseñas no coinciden. Intente nuevamente.")
        return users,False
    

    # Crear el nuevo usuario
    new_user = {
        "id": str(len(users) + 1),
        "name": name,
        "password": password,
        "age": age,
        "genre": genre,
        "role": role
    }

    users.append(new_user)
    print("Usuario registrado correctamente.")
    return users, True

def validar_existenciauser(users, name):
    """
    Valida si un usuario existe en la lista de usuarios.
    """
    for user in users:
        if user["name"] == name:
            return True
    return False

def validar_userandpassword(users, name, password):
    """
    Valida que el usuario exista y que la contraseña ingresada sea correcta.
    """
    for user in users:
        if user["name"] == name:
            if user["password"] == password:
                print("Acceso concedido.")
                return True
            else:
                print("Contraseña incorrecta.")
                return False
    print("Usuario no registrado.")
    return False


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

def input_int(mensaje):#funcion para validar que el input sea un entero
    valor = input(mensaje).strip()# otra vez  uso strip para quitar espacios en blanco al inicio y final si el user lo escribe
    valido = False# uso  bandera para controlar el bucle
    while not valido:# mientras no sea valido sigo pidiendo el valor
        try: # intento convertir el valor a entero con el nuevo concepto que vimos en clase
            valor_int = int(valor)
            valido = True
        except ValueError:
            print("Debe ingresar un numero entero valido. Intente nuevamente.")
            valor = input(mensaje).strip()
    return valor_int

def input_password(mensaje="Ingrese contraseña: ", min_length=6):#funcion para validar la contraseña.recibe un mensaje y una longitud minima
    pwd = getpass.getpass(mensaje).strip()
    
    if not pwd:
        print("La contraseña no puede estar vacia, intente nuevamente.")
        return input_password(mensaje, min_length)  # vuelve a pedir la contraseña 
    elif len(pwd) < min_length:
        print(f"La contraseña debe tener al menos {min_length} caracteres.")
        return input_password(mensaje, min_length)  # vuelve a pedir la contraseña
    else:
        return pwd  # contraseña valida
    
def choose_category(categories):
    """
    Muestra un menú para elegir una categoría de la lista y devuelve el string elegido.
    """
    idx = get_menu_option("Elija una categoría", categories)
    return categories[idx - 1]



##metricas
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
    for inc in incomes:
        if inc.get("user") == username:
            parsed = convert_to_tuple(inc.get("date"))
            if parsed and (parsed[1], parsed[2]) == (month, year):
                total_in = total_in + float(inc.get("amount", 0.0))

    total_out = 0.0
    for exp in expenses:
        if exp.get("user") == username:
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
        
    for exp in expenses:
        if exp.get("user") == username:
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
            goal_id = str(random.randint(1000, 9999))
            print(goal_id)
            goal_category = choose_category(goal_categories)
            goal_total_amount = input_float("Ingrese el monto del objetivo (meta total): ")
            goal_saved_amount = input_float("Ingrese el monto que desea guardar: ")
            goal_start_date = input_date("Ingrese la fecha en formato (dd/mm/yyyy) del inicio de su objetivo: ")
            goal_end_date = input_date("Ingrese la fecha en formato (dd/mm/yyyy) de finalizacion de su objetivo: ")
            goal_status = "Iniciado"

            goal = {
                "id": goal_id,
                "category": goal_category,
                "total_amount": goal_total_amount,
                "saved_amount": goal_saved_amount,
                "start_date": goal_start_date,
                "end_date": goal_end_date,
                "status": goal_status,
                "user": current_username
            }

            respuesta = insertGoals(goal)

            if respuesta == 0:
                print("Objetivo de ahorro creado correctamente.")
            elif respuesta == 1:
                print("Error: el monto total debe ser mayor a 0.")
            elif respuesta == 2:
                print("Error: el monto guardado no puede superar el monto total del objetivo")
            else:
                print("Error: la fecha final no puede ser anterior a la fecha de inicio.")
        # Modificar un objetivo de ahorro
        elif selected == 2:
            goal_id = input_non_empty("ID del objetivo de ahorro a actualizar: ")
            goal_category = choose_category(goal_categories)
            goal_total_amount = input_float("Ingrese el monto del objetivo (meta total): ")
            goal_saved_amount = input_float("Ingrese el monto que desea guardar: ")
            goal_start_date = input_date("Nueve fecha incial (dd/mm/yyyy) de su objetivo: ")
            goal_end_date = input_date("Nueve fecha final (dd/mm/yyyy) de su objetivo: ")
            goal_status = "Iniciado"

            goal = {
                "id": goal_id,
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

    while True:#uso un while True para repetir el flujo hasta que el user se registre o loguee correctamente
        # nvuelvo a preguntar si ya tiene cuenta
        tiene_cuenta = get_menu_option("¿Ya posee una cuenta? (si/no): ", ["si", "no"])
        
        while tiene_cuenta == 2:
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
            genre = get_menu_option("Ingrese genero (masculino/femenino/otro): ", ["masculino", "femenino", "otro"])

            # Intentar registrar usuario
            users_new, exito = registrar_usuario(users, username, password, password2, age, genre)
            if exito:
                print(" Registro completado correctamente.")
                break  # Salimos del while y continuamos al login
            else:
                print(" No se pudo completar el registro. Vamos a intentarlo de nuevo.\n")
                # El while vuelve al inicio del registro automaticamente

        else:
            break  # Ya tiene cuenta, pasar al login

    # --- LOGIN ---
    username = input_non_empty("Ingrese nombre de usuario: ")
    password = getpass.getpass("Ingrese contraseña: ")

    # usar validar_userandpassword en lugar de login  #(Ayuda no se porque me da error en islogged)
    isLogged = validar_userandpassword(users, username, password) #llama a la funcion para validar usuario y contraseña
    while not isLogged:
        print("Error en las credenciales")
        username = input("Ingrese nombre de usuario: ")
        password = getpass.getpass("Ingrese contraseña: ")
        isLogged = validar_userandpassword(users, username, password)

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
main() #aca tampoco se porque me da error ;(
