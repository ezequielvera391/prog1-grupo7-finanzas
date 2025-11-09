import os
import json


#utils
from validations import(
validate_expense,
validate_income,
validate_user,
validate_goal
)


# ----- Rutas y constantes -----
DB_DIR = "./data"
USERS_FILE = os.path.join(DB_DIR, "users.json")
INCOMES_FILE = os.path.join(DB_DIR, "incomes.json")
EXPENSES_FILE = os.path.join(DB_DIR, "expenses.json")
GOALS_FILE = os.path.join(DB_DIR, "goals.json")

income_categories = ["Salario", "Regalo", "Otros"]
expense_categories = ["Supermercado", "Vivienda", "Transporte", "Otros"]
goal_categories = ["Viaje", "Vivienda", "Electrodomesticos", "Educacion", "Otros"]
goals_status = ["Iniciado", "En proceso", "Completado"]


### Generales
## Privadas
def _collection_path(name):
    lower = str(name).strip().lower()
    if lower == "users":
        return USERS_FILE
    if lower == "incomes":
        return INCOMES_FILE
    if lower == "expenses":
        return EXPENSES_FILE
    if lower == "goals":
        return GOALS_FILE
    print(f"Error: colección desconocida '{name}'. Las opciones válidas son 'users', 'incomes', o 'expenses'.")
    return None

def _read_collection(file_path):
    try:
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def _next_id_from_collection(file_path, id_field="id"):
    # TODO: podría guardar un json de contadores con el último valor de id de cáda colección para evitar recorrer las colecciones 
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

def _find_row_index(file_path, id_value, id_field="id"):
    """
    Recibe un file_path que es un str con el valor del path de la colección donde vamos a buscar
    Tambien recibe un id_value que es el valor del id que estamos buscando
    Y por último de forma opcional recibe un id_field que es un str que define como se llama el campo id en la colección, por defecto 'id'
    Devuelve el índice del primer registro cuyo id == id_value.
    Si no existe, devuelve None.
    """
    rows = _read_collection(file_path)
    for i, row in enumerate(rows):
        if str(row.get(id_field, "")) == str(id_value):
            return i
    return None

def _write_collection(file_path, rows):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


## Publicas
def read_collection_by_name(name):
    """
    Recibe un name de formato string 
    Lee una colección con ese name, los name validos son: 'users' | 'incomes' | 'expenses'.
    Si el name es inválido, devuelve [].
    Si el name es válido devuelve la colección con dicho nombre
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
    _, userExist = users_find_by_name(user.get("name"))

    if userExist:
        return False
    
    ok, msg = validate_user(user)

    if not ok:
        return False
    
    rows = _read_collection(USERS_FILE)
    new_id = _next_id_from_collection(USERS_FILE)

    user_final = {
        "id": new_id,
        "name": user.get("name"),
        "password": user.get("password"),
        "age": user.get("age"),
        "genre": user.get("genre"),
        "role": user.get("role")
    }

    rows.append(user_final)
    _write_collection(USERS_FILE, rows)
    return True

def users_update(user):
    '''
    Recibe un usuario, busca que exista el nombre de usuario y el id
    En caso de existir lo actualiza, sino envía un error.
    '''
    index, userExist = users_find_by_name(user.get("name"))

    if not userExist:
        return False
    
    ok, msg = validate_user(user)

    if not ok:
        return False
    
    rows = _read_collection(USERS_FILE)
    new_id = _next_id_from_collection(USERS_FILE)

    rows[index] = {
        "id": new_id,
        "name": user.get("name"),
        "password": user.get("password"),
        "age": user.get("age"),
        "genre": user.get("genre"),
        "role": user.get("role")
    }

    _write_collection(USERS_FILE, rows)

def users_delete(user_id):
    '''
    Recibe el id de un usuario, busca que exista.
    En caso de existir lo elimina, sino envía un error.
    '''
    rows = _read_collection(USERS_FILE)
    updated_rows = [row for row in rows if str(row.get("id")) != str(user_id)]

    if len(updated_rows) == len(rows):
        return (False, "El ingreso que intenta borrar no existe")

    _write_collection(USERS_FILE, updated_rows)

    return (True, "El usuario fue borrado satisfactoriamente")

def users_find_by_name(username):
    '''
    Recibe el nombre de un usuario, busca que exista.
    En caso de existir lo devuelve completo, sino envía un error.
    '''
    rows = _read_collection(USERS_FILE)
    user = None
    for index, row in enumerate(rows):
        if row.get("name") == username:
            user = row
    if not user: 
        return (None, False)

    return (index, user)

def login_check(username, password):
    '''
    Recibe un usuario y contraseña, 
    verifica que el usuario exista y luego que la contraseña ingresada coincida con la que está guardada para ese usuario
    En caso de éxito devuelve True, sino devuelve False
    '''
    _, user = users_find_by_name(username)
    if not user: 
        return False

    return True if user.get("password") == password else False



### Incomes

def incomes_insert(income):
    '''
    Recibe income de tipo dict.
    Guarda un ingreso en incomes.json.
    Chequeos básicos:
    - amount > 0
    - category en income_categories
    - formato de fecha
    - user existe en users.json
    Se asigna id Auto-incremental (max(id)+1).
    Devuelve (True, income_final) o (False, "motivo").
    '''
    ok, msg = validate_income(income)
    if not ok:
        return (False, msg)

    rows = _read_collection(INCOMES_FILE)
    new_id = _next_id_from_collection(INCOMES_FILE)

    income_final = {
        "id": new_id,
        "amount": income.get("amount"),
        "category": income.get("category"),
        "date": income.get("date"),
        "user": income.get("user")
    }

    rows.append(income_final)
    _write_collection(INCOMES_FILE, rows)

    return (True, income_final)

def incomes_update(income):
    '''
    Recibe income de tipo dict.
    Actualiza un ingreso existente en incomes.json.
    Aplica los mismos chequeos que el insert.
    Devuelve (True, None) si se actualizó correctamente,
    o (False, "motivo") si no se pudo actualizar.
    '''
    income_id = income.get("id")
    if not income_id:
        return (False, "falta campo id")

    rows = _read_collection(INCOMES_FILE)
    if not rows:
        return (False, "no hay registros en incomes.json")

    # Buscar índice del registro a actualizar
    index = _find_row_index(INCOMES_FILE, income_id)
    if index is None:
        return (False, f"no existe ingreso con id {income_id}")

    valid, msg = validate_income(income)
    if not valid:
        return (False, msg)

    rows[index] = {
        "id": str(income_id),
        "amount": income.get("amount"),
        "category": income.get("category"),
        "date": income.get("date"),
        "user": income.get("user")
    }
    _write_collection(INCOMES_FILE, rows)

    return (True, None)

def incomes_delete(income_id):
    '''
    Recibe income_id de tipo str.
    Borra un ingreso por id de incomes.json.
    Devuelve:
    (True, "El ingreso fue borrado satisfactoriamente")
    o (False, "El ingreso que intenta borrar no existe").
    '''
    rows = _read_collection(INCOMES_FILE)
    updated_rows = [row for row in rows if str(row.get("id")) != str(income_id)]

    if len(updated_rows) == len(rows):
        return (False, "El ingreso que intenta borrar no existe")

    _write_collection(INCOMES_FILE, updated_rows)

    return (True, "El ingreso fue borrado satisfactoriamente")

def incomes_by_user(username):
    '''
    Recibe username de tipo str.
    Devuelve una lista con todos los ingresos (incomes) donde el campo "user" coincide con username.
    Si no hay coincidencias, devuelve una lista vacía.
    '''
    rows = _read_collection(INCOMES_FILE)
    results = [row for row in rows if row.get("user") == username]
    return results

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

    # Validación
    ok, msg = validate_expense(expense)
    if not ok:
        return (False, msg)
    
    # Leer colección y calcular próximo id
    rows = _read_collection(EXPENSES_FILE)
    new_id = _next_id_from_collection(EXPENSES_FILE)

    expense_final = {
        "id": new_id,
        "amount": expense.get("amount"),
        "category": expense.get("category"),
        "date": expense.get("date"),
        "user": expense.get("user")
    }

    # Guardar en base de datos
    rows.append(expense_final)
    _write_collection(EXPENSES_FILE, rows)

    return (True, expense_final)

def expenses_update(expense):
    '''
    Recibe expense de tipo dict.
    Actualiza un egreso existente (mismo id) en expenses.json.
    Valida las siguientes reglas:
    - amount > 0
    - category en expense_categories
    - formato de fecha dd/mm/yyyy
    - user existente en users.json
    Devuelve (True, None) si se actualizó correctamente,
    o (False, "motivo") si no se pudo actualizar.
    '''
    # Validaciones propias de esta funcion
    expense_id = expense.get("id")
    if not expense_id:
        return (False, "falta campo id")
    
    rows = _read_collection(EXPENSES_FILE)
    if not rows:
        return (False, "no hay registros en expenses.json")

    index = _find_row_index(EXPENSES_FILE, expense_id)
    if index is None:
        return (False, f"no existe egreso con id {expense_id}")

    # Validar las reglas de negocio antes de reemplazar
    valid, msg = validate_expense(expense)
    if not valid:
        return (False, msg)

    # Actualizar registro existente
    rows[index] = {
        "id": str(expense_id),
        "amount": expense.get("amount"),
        "category": expense.get("category"),
        "date": expense.get("date"),
        "user": expense.get("user")
    }

    # Guardar en disco
    _write_collection(EXPENSES_FILE, rows)

    return (True, None)

def expenses_delete(expense_id):
    '''
    Recibe expense_id de tipo str.
    Borra un egreso por id de expenses.json.
    Devuelve:
    En caso de éxito: (True, "El egreso fue borrado satisfactoriamente")
    En caso de que no encuentre el expense: (False, "El egreso que intenta borrar no existe").
    '''
    rows = _read_collection(EXPENSES_FILE)
    updated_rows = [row for row in rows if str(row.get("id")) != str(expense_id)]

    # Si la cantidad no cambió, no existía
    if len(updated_rows) == len(rows):
        return (False, "El egreso que intenta borrar no existe")

    # Guardar cambios
    _write_collection(EXPENSES_FILE, updated_rows)

    return (True, "El egreso fue borrado satisfactoriamente")
    
def expenses_by_user(username):
    '''
    Recibe username de tipo str.
    Devuelve una lista con todos los egresos (expenses) donde el campo "user" coincide con username.
    Si no hay coincidencias, devuelve una lista vacía.
    '''
    rows = _read_collection(EXPENSES_FILE)
    results = [row for row in rows if row.get("user") == username]
    return results

### Goals

def goals_insert(goal):
    '''
    Recibe un goal y lo guarda en goals.json.
    Chequeos básicos:
    - valida que user no esté vacio
    - category esté entre las categorias válidas
    - total_amount y saved_amount sean de tipo float
    - start_date y end_date sean fechas válidas
    - status esté entre los estados válidos
    - user existe en users.json
    Se asigna id Auto-incremental (max(id)+1)
    Devuelve (True, expense_final) o (False, "motivo").
    '''
    ok, msg = validate_goal(goal)
    if not ok:
        return (False, msg)
    
    # Leer colección y calcular próximo id
    rows = _read_collection(GOALS_FILE)
    new_id = _next_id_from_collection(GOALS_FILE)

    goal_final = {
        "id": new_id,
        "category": goal.get("category"),
        "total_amount": goal.get("total_amount"),
        "saved_amount": goal.get("saved_amount"),
        "start_date": goal.get("start_date"),
        "end_date": goal.get("end_date"),
        "status": goal.get("status"),
        "user": goal.get("user")
    }

    # Guardar en base de datos
    rows.append(goal_final)
    _write_collection(GOALS_FILE, rows)

    return (True, goal_final)

def goals_update(goal):
    '''
    Recibe goal de tipo dict.
    Actualiza una meta existente (mismo id) en goals.json.
    Valida las siguientes reglas:
    - valida que user no esté vacio
    - category esté entre las categorias válidas
    - total_amount y saved_amount sean de tipo float
    - start_date y end_date sean fechas válidas
    - status esté entre los estados válidos
    - user existe en users.json
    Devuelve (True, None) si se actualizó correctamente,
    o (False, "motivo") si no se pudo actualizar.
    '''
    # Validaciones propias de esta funcion
    goal_id = goal.get("id")
    if not goal_id:
        return (False, "falta campo id")
    
    rows = _read_collection(GOALS_FILE)
    if not rows:
        return (False, "no hay registros en goals.json")

    index = _find_row_index(GOALS_FILE, goal_id)
    if index is None:
        return (False, f"no existe egreso con id {goal_id}")

    # Validar las reglas de negocio antes de reemplazar
    valid, msg = validate_goal(goal)
    if not valid:
        return (False, msg)

    # Actualizar registro existente
    rows[index] = {
        "id": str(goal_id),
        "category": goal.get("category"),
        "total_amount": goal.get("total_amount"),
        "saved_amount": goal.get("saved_amount"),
        "start_date": goal.get("start_date"),
        "end_date": goal.get("end_date"),
        "status": goal.get("status"),
        "user": goal.get("user")
    }

    # Guardar en disco
    _write_collection(GOALS_FILE, rows)

    return (True, None)

def goals_delete(goal_id):
    '''
    Recibe goal_id de tipo str.
    Borra una meta por id de goals.json.
    Devuelve:
    En caso de éxito: (True, "La meta fue borrada satisfactoriamente")
    En caso de que no encuentre el expense: (False, "La meta que intenta borrar no existe").
    '''
    rows = _read_collection(GOALS_FILE)
    updated_rows = [row for row in rows if str(row.get("id")) != str(goal_id)]

    # Si la cantidad no cambió, no existía
    if len(updated_rows) == len(rows):
        return (False, "La meta que intenta borrar no existe")

    # Guardar cambios
    _write_collection(GOALS_FILE, updated_rows)

    return (True, "La meta fue borrada satisfactoriamente")
    
def goals_by_user(username):
    '''
    Recibe username de tipo str.
    Devuelve una lista con todos las metas (goals) donde el campo "user" coincide con username.
    Si no hay coincidencias, devuelve una lista vacía.
    '''
    rows = _read_collection(GOALS_FILE)
    results = [row for row in rows if row.get("user") == username]
    return results

### Boostrap DDBB
def ensure_db_files():
    '''
    Crea ./data si no existe y asegura que existan:
    - users.json
    - incomes.json
    - expenses.json
    - goals.json
    Si falta alguno, lo inicializa con [].
    No imprime ni pide input. Es solo para inicializar la bbdd en caso de que no exista
    '''
    os.makedirs(DB_DIR, exist_ok=True)

    for path in (USERS_FILE, INCOMES_FILE, EXPENSES_FILE, GOALS_FILE):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False)


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

    # Expenses
    "expenses_insert",
    "expenses_update",
    "expenses_delete",
    "expenses_by_user",

    # Users
    "users_insert",
    "users_update",
    "users_delete",
    "login_check",
    "users_find_by_name",

    # Goals
    "goals_insert",
    "goals_update",
    "goals_delete",
    "goals_by_user",

    # Utils / Setup
    "ensure_db_files"
]