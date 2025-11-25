import pytest
import os
import json

from index import (
    register_user,
    login,
    insertIncome,
    insertExpenses,
    insertGoals,
)
from db import USERS_FILE, INCOMES_FILE, EXPENSES_FILE, GOALS_FILE, ensure_db_files


def setup_test_database():
    """
    Función de ayuda para limpiar la base de datos antes de una prueba.
    """
    ensure_db_files()
    for db_file in [USERS_FILE, INCOMES_FILE, EXPENSES_FILE, GOALS_FILE]:
        if os.path.exists(db_file):
            with open(db_file, "w") as f:
                json.dump([], f)


#  Pruebas para Autenticación (Auth) 

def test_register_user_success():
    """Prueba el registro exitoso de un nuevo usuario."""
    setup_test_database()
    assert register_user("testuser", "pass123", "pass123", 30, "M") == True

def test_register_user_fails_if_already_exists():
    """Prueba que el registro falla si el usuario ya existe."""
    setup_test_database()
    register_user("testuser", "pass123", "pass123", 30, "M")
    assert register_user("testuser", "pass123", "pass123", 30, "M") == False

def test_register_user_fails_if_passwords_mismatch():
    """Prueba que el registro falla si las contraseñas no coinciden."""
    setup_test_database()
    assert register_user("newuser", "pass123", "pass456", 25, "F") == False

def test_login_success():
    """Prueba un inicio de sesión exitoso."""
    setup_test_database()
    register_user("testuser", "pass123", "pass123", 30, "M")
    assert login("testuser", "pass123") == True

def test_login_fails_with_wrong_password():
    """Prueba que el login falla con una contraseña incorrecta."""
    setup_test_database()
    register_user("testuser", "pass123", "pass123", 30, "M")
    assert login("testuser", "wrongpassword") == False

#  Pruebas para Ingresos y Egresos 

def test_insert_income_success():
    """Prueba la inserción exitosa de un ingreso."""
    setup_test_database()
    register_user("testuser", "pass123", "pass123", 30, "M")
    income = {"amount": 1500.0, "category": "Salario", "date": "15/07/2024", "user": "testuser"}
    assert insertIncome(income)[0] == True

def test_insert_expense_success():
    """Prueba la inserción exitosa de un egreso."""
    setup_test_database()
    register_user("testuser", "pass123", "pass123", 30, "M")
    expense = {"amount": 200.0, "category": "Supermercado", "date": "16/07/2024", "user": "testuser"}
    assert insertExpenses(expense)[0] == True

def test_insert_goal_success():
    """Prueba la inserción exitosa de un objetivo de ahorro."""
    setup_test_database()
    register_user("testuser", "pass123", "pass123", 30, "M")
    goal = {"name": "Viaje", "category": "Viaje", "total_amount": 500.0, "saved_amount": 50.0, "end_date": "01/01/2026", "status": "Iniciado", "user": "testuser"}
    assert insertGoals(goal)[0] == True