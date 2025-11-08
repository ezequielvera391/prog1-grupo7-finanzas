#utils

"""utils.py tiene las funciones que manejan todo lo que el usuario
 escribe por teclado: pedir datos,
 validar fechas, números, textos o mostrar menus."""

from index import(
get_menu_option,
input_float,
input_non_empty,
input_date,
input_int,
choose_category,
input_period,
convert_to_tuple


)


def get_menu_option(message, options):
    '''
    Recibe un message de tipo Str y un options de tipo list
    Muestra un menú con las opciones dadas y devuelve el índice elegido.
    - message: título del menú
    - options: lista de strings con las opciones
    Retorna un int con el valor del índice de la posición en la lista de opciones de la opcion elegida
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
    Recibe un messge de tipo str
    Solicita a traves de input el ingreso de un valor, usando como mensaje al usuario el message recibido
    Valida que pueda convertirse a número decimal y pide reintentar hasta que se ingrese correctamente.
    Retorna el valor ingresado por el usuario, covnertido a float
    """
    value = None
    while value is None:
        user_input = input(message)
        if user_input.replace(".", "", 1).isdigit(): 
            value = float(user_input)
        else:
            print("Error: debe ingresar un número válido.")
    return value


def input_non_empty(message):
    """
    Recibe un messge de tipo str
    Solicita a traves de input el ingreso de un valor, usando como mensaje al usuario el message recibido
    Valida que el valor ingresado no sea una cadena vacia y pide reintentar hasta que se ingrese correctamente.
    Retorna el valor ingresado por el usuario de tipo str
    """
    value = ""
    while not value.strip():
        value = input(message)
        if not value.strip():
            print("Error: no puede estar vacío.")
    return value


def input_date(message):
    """
    Recibe un messge de tipo str
    Solicita a traves de input el ingreso de un valor, usando como mensaje al usuario el message recibido
    Valida que el valor ingresado cumpla con el formato de fecha dd/mm/yyyy y pide reintentar hasta que se ingrese correctamente.
    Retorna el valor ingresado por el usuario de tipo str
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


def input_int(mensaje):
    """
    Recibe un messge de tipo str
    Solicita a traves de input el ingreso de un valor, usando como mensaje al usuario el message recibido
    Valida que pueda convertirse a número entero y pide reintentar hasta que se ingrese correctamente.
    Retorna el valor ingresado por el usuario, covnertido a int
    """
    value = input(mensaje).strip()
    is_valid = False
    while not is_valid:
        try:
            int_value = int(value)
            is_valid = True
        except ValueError:
            print("Debe ingresar un numero entero valido. Intente nuevamente.")
            value = input(mensaje).strip()
    return int_value


def choose_category(categories):
    """
    Recibe una lista de str, donde cada elemento representa una categoria
    Utiliza la funcion get_menu_option para mostrar de forma visual un menu de selección y capturar la eleccion del usuario
    retorna el elemento de tipo str seleccionado por el usuario
    """
    idx = get_menu_option("Elija una categoría", categories)
    return categories[idx - 1]


def input_period(message):
    """
    Recibe un string
    Solicita al usuario un mes y un año, validando la entrada.
    Retorna una tupla (month, year)
    """
    print(message)
    month = 0
    while not (1 <= month <= 12):
        month_str = input("Ingrese el mes (1-12): ")
        if month_str.isdigit():
            month = int(month_str)
        if not (1 <= month <= 12):
            print("Error: debe ingresar un mes válido (1-12).")
    
    year = 0
    while not (year > 1900):
        year = input_int("Ingrese el año (ej: 2024): ")
        if not (year > 1900):
            print("Error: debe ingresar un año válido (mayor a 1900).")
    return month, year


def convert_to_tuple(date_str):
    '''
    Recibe un str date_str con el formato "dd/mm/yyyy"
    Convierte date_str con formato "dd/mm/yyyy" en una tupla (day, month, year) de enteros.
    Si la fecha no tiene el formato correcto o valores fuera de rango, devuelve None.
    Sino retorna la tupla con formato (day, month, year)
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


#TODAS LAS FUNCIONES
__all__ = [
    "get_menu_option",
    "input_float",
    "input_non_empty",
    "input_date",
    "input_int",
    "choose_category",
    "input_period",
    "convert_to_tuple"
]
