## DATOS DEL SISTEMA

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
# - monto: number
# - categoria: categorias (vamos a definir un listado fijo de categorias de ingreso y de egreso)
# - fecha: "dd/mm/yyyy" (pueden ingresarse fechas que no sean la actual)
# - usuario: string (se debe guardar automaticamente con el valor del nombre o el id del usuario que realice la carga)
# Ejemplo de valor correcto para un ingreso o egreso: entidad = { "id": "1", "monto": 1800.0, "categoria": "Otros", "fecha": "08/06/2025", "usuario": "admin" }

incomes = []
expenses = []

# ABM INGRESOS
def insert(income):
    '''
    Este método recibe un ingreso, se asegura que sea un ingreso válido
    y lo inserta en la lista de ingresos
    '''
    pass

def updateIncome(income):
    '''
    Este método recibe un ingreso, se asegura que sea un ingreso válido y que exista en la lista de ingresos
    reemplaza el ingreso anterior con el nuevo
    '''
    pass

def deleteIncome(incomeId):
    '''
    Este método recibe el id de un ingreso, se asegura que exista en la lista de ingresos
    elimina el ingreso correspondiente al id
    '''
    pass

def getIncomesByUser(username):
    '''
    Este método recibe el nombre de un usuario y busca en la lista todos los incomes que hayan sido ingresados por ese usuario
    '''

# ABM EGRESOS
def insertExpenses(income):
    '''
        Este método recibe un egreso, se asegura que sea un egreso válido
        y lo inserta en la lista de egresos
    '''
    pass

def updateExpenses(income):
    '''
    Este método recibe un egreso, se asegura que sea un egreso válido y que exista en la lista de egresos
    reemplaza el ingreso anterior con el nuevo
    '''
    pass

def deleteExpenses(incomeId):
    '''
    Este método recibe el id de un egreso, se asegura que exista en la lista de egreso
    elimina el egreso correspondiente al id
    '''
    pass

def getExpensesByUser(username):
    '''
    Este método recibe el nombre de un usuario y busca en la lista todos los egresos que hayan sido ingresados por ese usuario
    '''

# AUTH
def login(username, password):
    '''
    Este método recibe un nombre de usuario y una contraseña, 
    busca el usuario que coincida con ese nombre y luego verifica que la contraseña coincida
    - Devuelve un -1 en caso de que no exista el usuario o no se encuentre la contraseña
    - crear método auxiliar para buscar un usuario
    '''

def getUser(username):
    '''
    Este método recibe un nombre de usuario y busca en la lista de usuarios si existe este usuario
    devuelve -1 en caso de no encontrarlo
    '''

# MENÚ E INTERACCIÓN CON EL USUARIO


def main():
    '''
    Función principal del programa
    '''
    print("Sin implementar...")

#### INICIO DE PROGRAMA
main()