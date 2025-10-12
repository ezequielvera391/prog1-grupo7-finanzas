import os
import json

# ----- Rutas y constantes -----
DB_DIR = "./data"
USERS_FILE = os.path.join(DB_DIR, "users.json")
INCOMES_FILE = os.path.join(DB_DIR, "incomes.json")
EXPENSES_FILE = os.path.join(DB_DIR, "expenses.json")

income_categories = ["Salario", "Regalo", "Otros"]
expense_categories = ["Supermercado", "Vivienda", "Transporte", "Otros"]

### Generales
def _collection_path(name):
    lower = str(name).strip().lower()
    if lower == "users":
        return USERS_FILE
    if lower == "incomes":
        return INCOMES_FILE
    if lower == "expenses":
        return EXPENSES_FILE
    print(f"Error: colección desconocida '{name}'. Las opciones válidas son 'users', 'incomes', o 'expenses'.")
    return None

def _read_collection(file_path):
    try:
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def _next_id_from_collection(file_path, id_field="id"):
    rows = _read_collection(file_path)
    max_id = 0
    for row in rows:
        try:
            current = int(str(row.get(id_field, "0")))
            if current > max_id:
                max_id = current
        except Exception:
            print("ERROR: el campo id no es numerico.")
    return str(max_id + 1)

def read_collection_by_name(name):
    """
    Lee una colección por nombre ('users' | 'incomes' | 'expenses').
    Si el nombre es inválido, devuelve [].
    """
    path = _collection_path(name)
    if path is None:
        print(f"Error: cannot read collection '{name}' because it is invalid.")
        return []
    return _read_collection(path)


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
    os.makedirs(DB_DIR, exist_ok=True)

    for path in (USERS_FILE, INCOMES_FILE, EXPENSES_FILE):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False)


### EXPORTS ### 
__all__ = [
    # Rutas y constantes
    "DB_DIR",
    "USERS_FILE",
    "INCOMES_FILE",
    "EXPENSES_FILE",
    "income_categories",
    "expense_categories",

    # General
    "read_collection_by_name",

    # Incomes
    "incomes_insert",
    "incomes_update",
    "incomes_delete",
    "incomes_by_user",
    "incomes_find_by_id",

    # Expenses
    "expenses_insert",
    "expenses_update",
    "expenses_delete",
    "expenses_by_user",
    "expenses_find_by_id",

    # Utils / Setup
    "ensure_db_files"
]