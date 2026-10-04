"""Cliente de consola - Sistema de Gestion de Tareas (PFO2 - Redes).

Consume la API Flask del servidor (servidor.py) via HTTP.
Requiere que el servidor este corriendo en http://127.0.0.1:5000
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def registrarse():
    """Pide credenciales y llama a POST /registro."""
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    respuesta = requests.post(
        f"{BASE_URL}/registro",
        json={"usuario": usuario, "contraseña": contraseña},
    )
    print(f"[{respuesta.status_code}] {respuesta.json()}")


def iniciar_sesion():
    """Pide credenciales y llama a POST /login."""
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    respuesta = requests.post(
        f"{BASE_URL}/login",
        json={"usuario": usuario, "contraseña": contraseña},
    )
    print(f"[{respuesta.status_code}] {respuesta.json()}")


def ver_tareas():
    """Llama a GET /tareas y muestra el HTML de bienvenida."""
    respuesta = requests.get(f"{BASE_URL}/tareas")
    print(f"[{respuesta.status_code}]")
    print(respuesta.text)


def main():
    """Menu principal del cliente."""
    while True:
        print("\n=== Sistema de Gestion de Tareas ===")
        print("1. Registrarse")
        print("2. Iniciar sesion")
        print("3. Ver tareas")
        print("4. Salir")
        opcion = input("Opcion: ").strip()

        if opcion == "1":
            registrarse()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            print("Hasta luego!")
            break
        else:
            print("Opcion invalida, intenta de nuevo.")


if __name__ == "__main__":
    main()
