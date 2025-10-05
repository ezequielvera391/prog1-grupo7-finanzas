



usuarios=[]
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
main()