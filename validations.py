"""El archivo validations.py es el modulo encargado de verificar y validar la informacion
Se asegura de que los datos sean correctos, tengan formato valido 
y correspondan a un usuario existente antes de guardarlos."""
from datetime import datetime

#rutas 

def is_valid_date(date_str):
    """
    Recibe un date_str de tipo str
    Valida que la fecha tenga formato dd/mm/yyyy, que exista (considerando años bisiestos)
    y que el año esté entre 1900 y el año actual inclusive.
    Devuelve True si es válida, False en caso contrario.
    """
    try:
        d, m, y = date_str.split("/")
        d, m, y = int(d), int(m), int(y)

        # si date time no puede generar la fecha (como 29 de febrero de un año ni bisiesto, sale por el except) 
        datetime(y, m, d) 

        if 1900 <= y <= datetime.now().year:
            return True
        return False
    except Exception:
        return False
    
def validate_expense(expense, expense_categories, users):
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

    if not is_valid_date(expense.get("date")):
        return (False, "Fecha inválida (usar dd/mm/yyyy)")

    if not any(user.get("name") == expense.get("user") for user in users):
        return (False, "El usuario que intenta realizar la operación no existe")

    return (True, None)

def validate_income(income, income_categories, users):
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

    if not is_valid_date(income.get("date")):
        return (False, "Fecha inválida (usar dd/mm/yyyy)")

    if not any(user.get("name") == income.get("user") for user in users):
        return (False, "El usuario que intenta realizar la operación no existe")

    return (True, None)

def validate_user(user):
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

def validate_goal(goal, goal_categories, goals_status, users):
    '''
    Recibe un goal de tipo dict
    Valida que tenga los campos básicos correctos:

    user: string no vacio
    category: un string que debe estar dentro de la lista goal_categories
    total_amount: de tipo float (Monto total del objetivo de ahorro)
    saved_amount: de tipo float (Monto total que decide guardar el usuario)
    start_date: "dd/mm/yyyy" (fecha inicio)
    end_date: "dd/mm/yyyy" (fecha final, debe ser mayor a la fecha de inicio)
    status: string debe estar en la lista goals_status
    '''
    # TODO: verificar validaciones de si total debe ser mayor a saved, y si fecha inicio y final tiene un plazo minimo
    if not isinstance(goal, dict):
        return (False, "formato inválido")
    
    try:
        total_amount = float(goal.get("total_amount", 0))
    except (TypeError, ValueError):
        return (False, "total_amount debe ser numérico")

    if total_amount <= 0:
        return (False, "total_amount debe ser mayor a 0")
    
    try:
        saved_amount = float(goal.get("total_amount", 0))
    except (TypeError, ValueError):
        return (False, "total_amount debe ser numérico")

    if saved_amount <= 0:
        return (False, "total_amount debe ser mayor a 0")
    
    if not is_valid_date(goal.get("start_date")):
        return (False, "Fecha de inicio inválida (usar dd/mm/yyyy)")
    
    if not is_valid_date(goal.get("end_date")):
        return (False, "Fecha de fin inválida (usar dd/mm/yyyy)")

    # TODO: validar que start sea menor a end

    if not goal.get("name").strip():
        return (False, "El campo name no puede estar vacío")
    
    if goal.get("category") not in goal_categories:
        return (False, "Categoría inválida")
    
    if goal.get("status") not in goals_status:
        return (False, "Estado inválido")

    if not any(user.get("name") == goal.get("user") for user in users):
        return (False, "El usuario que intenta realizar la operación no existe")
    
    return (True, None)

#TODAS LAS FUNCIONES 
__all__=[
    "is_valid_date",
    "validate_expense",
    "validate_income",
    "validate_user",
    "validate_goal",
]
