



"""usuarios=[]
contrasenias=[]

def ingreso_dedatos():
    usuario=input("ingrese un usuario:")
    if usuario in usuarios:
        print("ingrese otro usuario, este ya existe")
        return
    
    contrasenia=input("ingrese una contraseña:")
    contrasenia2=input("ingrese otra vez su contraseña:")
    while contrasenia !=contrasenia2:
        print("ingrese su contraseña anterior correctamente.")
        contrasenia=input("ingrese una contraseña: ")
        contrasenia2=input("ingrese otra vez su contraseña:")
    usuarios.append(usuario)
    contrasenias.append(contrasenia)
 
    print("usted ingreso correctamente.")

#----- validacion de existencia -----------------------------------------------------------------------------
def validar_existenciauser():
    usuario=input("ingrese su usuario para validar :")
    while usuario not in usuarios:
        print("usuario no encontrado, por favor vuelva a intentar")
        usuario=input("ingrese su usuario:")
    print("usuario encontrado correctamente.")

#------------------------------------------------------------------------------
def validar_userandpassword(usuario,contrasenia):

    if usuario in usuarios:
        index=usuarios.index(usuario)
        if contrasenias[index]==contrasenia:
            print("Acceso concedido.")
        else:
            print("contraseña incorrecta.")
    else:
        print("usuario no registrado ")



#--------------------------------------------------------------------------------

def main ():
    ingreso_dedatos()
    validar_existenciauser()
    usuario=input(" ingrese un usuario para validar:")
    contrasenia=input("ingrese su contraseña para validar: ")
    validar_userandpassword(usuario,contrasenia)
    salir=input("ingrese un 1 para salir del programa:")
    if salir=="1":
        print("programa finalizado.")
        return
main()"""

# ---------------------- BASE DE DATOS DE USUARIOS -----------------------
users = [
    {
        "id": "1",
        "name": "admin",
        "password": "1234",
        "age": 20,
        "genre": "M",
        "role": "admin"
    },
]


# ---------------------- FUNCIONES -----------------------

def ingreso_dedatos(users, name, password, password2):
    """Registra un nuevo usuario si no existe y las contraseñas coinciden."""
    # Verificar si el usuario ya existe
    for user in users:
        if user["name"] == name:
            print("El usuario ya existe. Intente con otro nombre.")
            return users

    # Validar contraseñas
    if password != password2:
        print("Las contraseñas no coinciden. Intente nuevamente.")
        return users

    # Crear nuevo usuario
    new_user = {
        "id": str(len(users) + 1),
        "name": name,
        "password": password,
        "age": None,
        "genre": None,
        "role": "user"
    }

    users.append(new_user)
    print("Usuario registrado correctamente.")
    return users


def validar_existenciauser(users, name):
    """Valida si un usuario existe."""
    for user in users:
        if user["name"] == name:
            print("Usuario encontrado correctamente.")
            return True
    print("Usuario no encontrado.")
    return False


def validar_userandpassword(users, name, password):
    """Valida si el usuario y la contraseña coinciden."""
    for user in users:
        if user["name"] == name:
            if user["password"] == password:
                print("Acceso concedido.")
                return True
            else:
                print("Contraseña incorrecta.")
                return False
    print("Usuario no registrado.")
    return False


# ---------------------- PROGRAMA PRINCIPAL -----------------------

def main():
    # Todos los input van acá:
    name = input("Ingrese un nombre de usuario nuevo: ")
    password = input("Ingrese una contraseña: ")
    password2 = input("Repita la contraseña: ")

    ingreso_dedatos(users, name, password, password2)

    name_check = input("Ingrese su usuario para validar existencia: ")
    validar_existenciauser(users, name_check)

    name_login = input("Ingrese su usuario para iniciar sesión: ")
    password_login = input("Ingrese su contraseña: ")
    validar_userandpassword(users, name_login, password_login)

    salir = input("Ingrese 1 para salir del programa: ")
    if salir == "1":
        print("Programa finalizado.")


# ---------------------- EJECUCIÓN -----------------------
main()
