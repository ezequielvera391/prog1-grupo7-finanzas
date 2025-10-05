import getpass
import random

## DATOS DEL SISTEMA

## BASE DE DATOS
## Defino acá el path para los distintos archivos que van a representar las colecciones de mi base de datos
DB_DIR = "./data"
USERS_FILE = f"{DB_DIR}/users.json"
INCOMES_FILE = f"{DB_DIR}/incomes.json"
EXPENSES_FILE = f"{DB_DIR}/expenses.json"

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
### Generales
def read_collection(file_path):
    '''
    Recibe un string que es el path donde va a buscar el archivo de base de datos
    Devuelve la lista del documento o [] si no existe o está vacio
    '''

def next_id_from_collection(file_path, id_field="id"):
    '''
    Recibe el path de una coleccion, y opcionalmente un string con el nombre del campo de id que debe modificar (por defecto "id")
    Calcula el valor del siguiente id (id max de la colleccion + 1), si la coleccion no tiene elementos retorna 1.
    '''

### Usuarios 
def users_insert(user):
    '''
    Verifica que el usuario que se intenta ingresar no exista ya en base de datos
    De no existir lo ingresa, sino envía un error
    '''

def users_update(user):
    '''
    Recibe un usuario, busca que exista el nombre de usuario y el id
    En caso de existir lo actualiza, sino envía un error.
    '''

def users_delete(user_id):
    '''
    Recibe el id de un usuario, busca que exista.
    En caso de existir lo elimina, sino envía un error.
    '''

def users_find_by_name(name):
    '''
    Recibe el nombre de un usuario, busca que exista.
    En caso de existir lo devuelve completo, sino envía un error.
    '''

def login_check(username, password):
    '''
    Recibe un usuario y contraseña, 
    verifica que el usuario exista y luego que la contraseña ingresada coincida con la que está guardada para ese usuario
    En caso de éxito devuelve True, sino devuelve False
    '''

### Incomes

def incomes_insert(income):
    '''
    Recibe un ingreso y lo guarda en incomes.json.
    Chequeos básicos:
    - amount > 0
    - category en income_categories
    - formato de fecha
    - user existe en users.json
    Se asigna id Auto-incremental (max(id)+1).
    Devuelve (True, income_final) o (False, "motivo").
    '''

def incomes_update(income):
    '''
    Actualiza un ingreso existente (mismo id).
    Aplica los mismos chequeos que el insert.
    Devuelve (True, None) o (False, "motivo").
    '''

def incomes_delete(income_id):
    '''
    Borra un ingreso por id de incomes.json.
    Devuelve (True, None) o (False, "no existe").
    '''

def incomes_by_user(username):
    '''
    Devuelve todos los incomes donde user == username.
    (Opcional: ordenar por fecha si hace falta)
    '''

def incomes_find_by_id(income_id):
    '''
    Busca un income por id.
    Devuelve el dict o None.
    '''

### Expenses
def expenses_insert(expense):
    '''
    Recibe un egreso y lo guarda en expenses.json.
    Chequeos básicos:
    - amount > 0
    - category en expense_categories
    - formato de fecha
    - user existe en users.json
    Se asigna id Auto-incremental (max(id)+1)
    Devuelve (True, expense_final) o (False, "motivo").
    '''

def expenses_update(expense):
    '''
    Actualiza un egreso existente (mismo id).
    Mismos chequeos que el insert.
    Devuelve (True, None) o (False, "motivo").
    '''

def expenses_delete(expense_id):
    '''
    Borra un egreso por id de expenses.json.
    Devuelve (True, None) o (False, "no existe").
    '''

def expenses_by_user(username):
    '''
    Devuelve todos los expenses donde user == username.
    (Opcional: ordenar por fecha si hace falta)
    '''

def expenses_find_by_id(expense_id):
    '''
    Busca un expense por id.
    Devuelve el dict o None.
    '''

### Boostrap DDBB
def ensure_db_files():
    '''
    Crea ./data si no existe y asegura que existan:
    - users.json
    - incomes.json
    - expenses.json
    Si falta alguno, lo inicializa con [].
    No imprime ni pide input. Es solo para inicializar la bbdd en caso de que no exista
    '''

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
            print("Métricas: próximamente…")
        elif selected == 4:
            print("Saliendo...")


#### INICIO DE PROGRAMA
main()