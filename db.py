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
## Privadas
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

# TODO: esto podría ser una función pública de un módulo de útils para toda la app
def _is_valid_date(date_str):
    """
    Recibe un date_str de tipo str
    Valida que la fecha tenga formato dd/mm/yyyy y valores superiores o iguales a 1/1/1900.
    Devuelve True si es válida, False en caso contrario.
    """
    try:
        d, m, y = date_str.split("/")
        d, m, y = int(d), int(m), int(y)
        if 1 <= d <= 31 and 1 <= m <= 12 and y > 1900:
            return True
        return False
    except Exception:
        return False
    
def _validate_expense(expense):
    """
    Recibe expense de tipo dict.
    Valida que tenga los campos básicos correctos:
    - amount numérico y > 0
    - category válida
    - date en formato dd/mm/yyyy
    - user existente en users.json
    Devuelve (True, None) si es válido, o (False, "motivo") si no lo es.
    """
    if not isinstance(expense, dict):
        return (False, "formato inválido")
    
    try:
        amount = float(expense.get("amount", 0))
    except (TypeError, ValueError):
        return (False, "amount debe ser numérico")

    if amount <= 0:
        return (False, "amount debe ser mayor a 0")

    if expense.get("category") not in expense_categories:
        return (False, "Categoría inválida")

    if not _is_valid_date(expense.get("date")):
        return (False, "Fecha inválida (usar dd/mm/yyyy)")

    users = _read_collection(USERS_FILE)
    if not any(user.get("name") == expense.get("user") for user in users):
        return (False, "El usuario que intenta realizar la operación no existe")

    return (True, None)

def _validate_income(income):
    """
    Recibe income de tipo dict.
    Valida que tenga los campos básicos correctos:
    - amount numérico y > 0
    - category válida
    - date en formato dd/mm/yyyy
    - user existente en users.json
    Devuelve (True, None) si es válido, o (False, "motivo") si no lo es.
    """
    if not isinstance(income, dict):
        return (False, "formato inválido")
    
    try:
        amount = float(income.get("amount", 0))
    except (TypeError, ValueError):
        return (False, "amount debe ser numérico")

    if amount <= 0:
        return (False, "amount debe ser mayor a 0")

    if income.get("category") not in income_categories:
        return (False, "Categoría inválida")

    if not _is_valid_date(income.get("date")):
        return (False, "Fecha inválida (usar dd/mm/yyyy)")

    users = _read_collection(USERS_FILE)
    if not any(user.get("name") == income.get("user") for user in users):
        return (False, "El usuario que intenta realizar la operación no existe")

    return (True, None)

def _validate_user(user):
    """
    Recibe un user de tipo dict
    Valida que tenga los campos básicos correctos:
    - name es un string, no puede estar vacío
    - password es un string, no puede estar vacío
    - age es un número entero debe ser mayor a 0
    - genre debe ser una M, una F o una X
    - role debe ser admin o user
    Devuelve (True, None) si es válido, o (False, "motivo") si no lo es.
    """
    if not isinstance(user, dict):
        return (False, "formato inválido")
    
    if not user.get("name").strip():
        return (False, "El campo name no puede estar vacío")
    
    if not user.get("password").strip():
        return (False, "El campo password no puede estar vacío")
    
    valid_genres = ["M", "F", "X"]

    if user.get("genre") not in valid_genres:
        return (False, "El campo genero debe ser M, F o X")
    
    try:
        age = int(user.get("age", 0))
    except (TypeError, ValueError):
        return (False, "Edad debe ser numérico")

    if age <= 0:
        return (False, "Edad debe ser mayor a 0")

    valid_roles = ["admin", "user"]
    if user.get("role") not in valid_roles:
        return (False, "Rol inválido")

    return (True, None)



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
    
    ok, msg = _validate_user(user)

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
    
    ok, msg = _validate_user(user)

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
    if not user: return (None, False)

    return (index, user)

def login_check(username, password):
    '''
    Recibe un usuario y contraseña, 
    verifica que el usuario exista y luego que la contraseña ingresada coincida con la que está guardada para ese usuario
    En caso de éxito devuelve True, sino devuelve False
    '''
    _, user = users_find_by_name(username)
    if not user: return False

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
    ok, msg = _validate_income(income)
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

    valid, msg = _validate_income(income)
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
    ok, msg = _validate_expense(expense)
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
    valid, msg = _validate_expense(expense)
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

    # TODO: Users

    # Utils / Setup
    "ensure_db_files"
]