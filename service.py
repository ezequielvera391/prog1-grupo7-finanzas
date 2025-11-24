#service 


"""El archivo service.py agrupa las funciones que procesan y analizan los datos. 
    Usa la información de ingresos y egresos que maneja db.py para calcular metricas
 como el ahorro mensual, la variacion del ahorro entre meses y el porcentaje de gastos por categoria.
 """


from datetime import datetime
from db import incomes_by_user, expenses_by_user, goals_by_user
from utils import convert_to_tuple



def calculate_monthly_savings(username, month, year):
    '''
    -Calcula el ahorro (ingresos - egresos) del usuario `username`
    para el mes `month` y año `year`.
    - Devuelve float (positivo/negativo/0.0).
    '''
    total_in = 0.0
    for inc in incomes_by_user(username):
        parsed = convert_to_tuple(inc.get("date"))
        if parsed and (parsed[1], parsed[2]) == (month, year):
            total_in = total_in + float(inc.get("amount", 0.0))

    total_out = 0.0
    for exp in  expenses_by_user(username):
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
        
    for exp in expenses_by_user(username):
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

def total_incomes_for_month(username, month, year):
    '''
    Recibe
    
    username: str que corresponde al nombre de usuario
    month: int para el mes
    year: para el año
    Trae todos los incomes para ese username y devuelve la suma total de los incomes correspondintes al mes y año recibidos
    '''
    total = 0.0
    for inc in incomes_by_user(username):
        parsed = convert_to_tuple(inc.get("date"))
        if parsed and (parsed[1], parsed[2]) == (month, year):
            total += float(inc.get("amount", 0.0))
    return total

def total_expenses_for_month(username, month, year):
    '''
    Recibe
    
    username: str que corresponde al nombre de usuario
    month: int para el mes
    year: para el año
    Trae todos los expenses para ese username y devuelve la suma total de las expenses correspondintes al mes y año recibidos
    '''
    total = 0.0
    for exp in expenses_by_user(username):
        parsed = convert_to_tuple(exp.get("date"))
        if parsed and (parsed[1], parsed[2]) == (month, year):
            total += float(exp.get("amount", 0.0))
    return total

def total_incomes_all_time(username):
    '''    
    username: str que corresponde al nombre de usuario
    Devuelve todos los incomes pertenecientes al usuario que recibe por parametro, si no existen o no existe el usuario devuelve None
    '''
    total = 0.0
    for inc in incomes_by_user(username):
        total += float(inc.get("amount", 0.0))
    return total

def total_expenses_all_time(username):
    '''    
    username: str que corresponde al nombre de usuario
    Devuelve todos los expenses pertenecientes al usuario que recibe por parametro, si no existen o no existe el usuario devuelve None
    '''
    total = 0.0
    for exp in expenses_by_user(username):
        total += float(exp.get("amount", 0.0))
    return total

def compute_goal_status(total_amount, saved_amount):
    """
    Devuelve el estado de una meta según su progreso:
    - Iniciado: saved == 0
    - En proceso: 0 < saved < total
    - Completado: saved >= total
    El campo status en el JSON puede ignorarse y recalcularse siempre.
    """
    total = float(total_amount)
    saved = float(saved_amount)

    if total <= 0:
        return "Iniciado"

    if saved <= 0:
        return "Iniciado"
    elif saved < total:
        return "En proceso"
    else:
        return "Completado"

def goals_summary(username):
    """
    Recibe
    
    username: str que corresponde al nombre de usuario
    Devuelve un resumen de objetivos de ahorro del usuario:
    - total_goals
    - goals_completed
    - goals_in_progress
    - goals_not_started
    - details: lista de metas con % de avance y estado calculado
    """
    goals = goals_by_user(username)
    summary = {
        "total_goals": 0,
        "goals_completed": 0,
        "goals_in_progress": 0,
        "goals_not_started": 0,
        "details": []
    }

    if not goals:
        return summary

    summary["total_goals"] = len(goals)

    for g in goals:
        total = float(g.get("total_amount", 0.0))
        saved = float(g.get("saved_amount", 0.0))

        progress_pct = 0.0
        if total > 0:
            progress_pct = (saved / total) * 100.0

        status = compute_goal_status(total, saved)

        if status == "Completado":
            summary["goals_completed"] += 1
        elif status == "En proceso":
            summary["goals_in_progress"] += 1
        else:
            summary["goals_not_started"] += 1

        summary["details"].append({
            "id": g.get("id"),
            "name": g.get("name"),
            "category": g.get("category"),
            "total_amount": total,
            "saved_amount": saved,
            "progress_pct": progress_pct,
            "end_date": g.get("end_date"),
            "status": status
        })

    return summary

def build_dashboard_metrics(username):
    """
    Arma todas las métricas necesarias para el dashboard:
    - Histórico: total_in_all, total_out_all, savings_all
    - Mes actual: ingresos, egresos, ahorro
    - Mes anterior: ahorro y cambio %
    - Resumen de metas
    - Distribución de egresos por categoría (mes actual)
    """
    today = datetime.today()
    month = today.month
    year = today.year

    # Totales históricos
    total_in_all = total_incomes_all_time(username)
    total_out_all = total_expenses_all_time(username)
    savings_all = total_in_all - total_out_all

    # Mes actual
    total_in = total_incomes_for_month(username, month, year)
    total_out = total_expenses_for_month(username, month, year)
    savings_current = total_in - total_out

    # Mes anterior
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    savings_prev = calculate_monthly_savings(username, prev_month, prev_year)

    # Cambio porcentual
    change_pct = None
    if savings_prev == 0.0 and savings_current == 0.0:
        change_pct = 0.0
    elif savings_prev != 0.0:
        base = savings_prev if savings_prev >= 0 else -savings_prev
        change_pct = ((savings_current - savings_prev) / base) * 100.0

    # Metas
    goals_info = goals_summary(username)

    # Distribución de egresos por categoría (mes actual)
    expenses_distribution = average_expense_by_category(username, month, year)

    return {
        "month": month,
        "year": year,
        "prev_month": prev_month,
        "prev_year": prev_year,
        "total_in_all": total_in_all,
        "total_out_all": total_out_all,
        "savings_all": savings_all,
        "total_in": total_in,
        "total_out": total_out,
        "savings_current": savings_current,
        "savings_prev": savings_prev,
        "change_pct": change_pct,
        "goals": goals_info,
        "expenses_distribution": expenses_distribution
    }


#TODAS LAS FUNCIONES
__all__ = [
    "calculate_monthly_savings",
    "percent_change_in_savings",
    "average_expense_by_category",
    "total_incomes_for_month",
    "total_expenses_for_month",
    "total_incomes_all_time",
    "total_expenses_all_time",
    "compute_goal_status",
    "goals_summary",
    "build_dashboard_metrics",
]



