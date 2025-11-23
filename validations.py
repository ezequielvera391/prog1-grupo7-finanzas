"""El archivo validations.py es el modulo encargado de verificar y validar la informacion
Se asegura de que los datos sean correctos, tengan formato valido 
y correspondan a un usuario existente antes de guardarlos."""
from datetime import datetime, timedelta

#rutas 


def _parse_date(date_str):
    """
    Recibe un String con formato dd/mm/yyyy e intenta convertirolo a objeto datetime.date.
    Devuelve None si el formato es inválido o la fecha no existe.
    """
    try:
        d, m, y = map(int, date_str.split("/"))
        return datetime(y, m, d).date()
    except Exception:
        return None

def is_valid_date(date_str):
    """
    Recibe un date_str de tipo str.
    Valida que la fecha tenga formato dd/mm/yyyy y que exista
    (considerando años bisiestos).
    Devuelve True si es válida, False en caso contrario.
    """
    fecha = _parse_date(date_str)
    if not fecha:
        return False
    
    if fecha.year < 1900:
        return False

    return True

def is_past_or_today(date_str):
    """
    Recibe un String con formato dd/mm/yyyy 
    Valida que la fecha sea válida y esté entre 01/01/1900 y hoy inclusive.
    Útil para gastos, ingresos, etc.
    """
    fecha = _parse_date(date_str)
    if not fecha:
        return False

    today = datetime.now().date()
    return fecha <= today and fecha.year >= 1900

def is_valid_goal_date(date_str, max_years=50):
    """
    Recibe un String con formato dd/mm/yyyy y un int max_years
    Valida que la fecha sea válida, a futuro (>= hoy)
    y no más allá de max_years años desde hoy.
    Útil para fechas de finalización de objetivos de ahorro.
    """
    fecha = _parse_date(date_str)
    if not fecha:
        return False

    today = datetime.now().date()

    if fecha <= today:
        return False

    max_date = today + timedelta(days=365 * max_years)
    return fecha <= max_date


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

    if not is_past_or_today(income.get("date")):
        return (False, "Fecha inválida (usar dd/mm/yyyy y no puede ser futura)")

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
    end_date: "dd/mm/yyyy" (fecha final, debe ser mayor a la fecha de inicio)
    status: string debe estar en la lista goals_status
    '''
    if not isinstance(goal, dict):
        return (False, "formato inválido")
    
    try:
        total_amount = float(goal.get("total_amount", 0))
    except (TypeError, ValueError):
        return (False, "Monto total debe ser numérico")

    if total_amount <= 0:
        return (False, "Monto total  debe ser mayor a 0")
    
    try:
        saved_amount = float(goal.get("saved_amount", 0))
    except (TypeError, ValueError):
        return (False, "Monto total  debe ser numérico")

    if saved_amount < 0:
        return (False, "Monto a ahorrar no puede ser negativo")
    
    if saved_amount >= total_amount:
        return (False, "Monto total debe ser mayor al monto ya ahorrado")
    
    end_date_str = goal.get("end_date")
    if not is_valid_goal_date(end_date_str):
        return (False, "Fecha de fin inválida (usar dd/mm/yyyy, debe ser futura y en un rango razonable)")

    if not goal.get("name").strip():
        return (False, "El campo nombre no puede estar vacío")
    
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
    "is_past_or_today",
    "is_valid_goal_date",
    "validate_expense",
    "validate_income",
    "validate_user",
    "validate_goal",
]
