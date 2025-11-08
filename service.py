#service 


"""El archivo service.py agrupa las funciones que procesan y analizan los datos. 
    Usa la información de ingresos y egresos que maneja db.py para calcular metricas
 como el ahorro mensual, la variacion del ahorro entre meses y el porcentaje de gastos por categoria.
 """


from db import incomes_by_user, expenses_by_user
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

#TODAS LAS FUNCIONES
_all_=[
    "calculate_monthly_savings",
    "percent_change_in_savings", 
    "average_expense_by_category"
]



