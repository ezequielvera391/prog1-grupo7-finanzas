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
    with open(INCOMES_FILE, "w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)

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
    index = next((i for i, row in enumerate(rows) if str(row.get("id")) == str(income_id)), None)
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

    with open(INCOMES_FILE, "w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)

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

    with open(INCOMES_FILE, "w", encoding="utf-8") as file:
        json.dump(updated_rows, file, ensure_ascii=False, indent=2)

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

def incomes_find_by_id(income_id):
    '''
    Recibe income_id de tipo str.
    Busca un income por id dentro de la colección de incomes.
    Devuelve el dict o None.
    '''
    rows = _read_collection(INCOMES_FILE)
    for row in rows:
        if str(row.get("id")) == str(income_id):
            return row
    return None

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
    with open(EXPENSES_FILE, "w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)

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

    # Para cada i, row en rows, si el id del row coincide con expense_id, devuelve ese i; si no hay coincidencias, devuelve None.
    # En otras palabras, devuelve el primer indice de rows que coincida con expense_id
    index = next((i for i, row in enumerate(rows) if str(row.get("id")) == str(expense_id)), None)
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
    with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

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
    with open(EXPENSES_FILE, "w", encoding="utf-8") as file:
        json.dump(updated_rows, file, ensure_ascii=False, indent=2)

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

def expenses_find_by_id(expense_id):
    '''
    Recibe expense_id de tipo str.
    Busca un expense por id.
    Devuelve el dict o None.
    '''
    rows = _read_collection(EXPENSES_FILE)
    for row in rows:
        if str(row.get("id")) == str(expense_id):
            return row
    return None

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