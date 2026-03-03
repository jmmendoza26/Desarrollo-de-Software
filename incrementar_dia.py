'''
Lee una fecha en formato: dd mm yyyy
Imprime la fecha del día siguiente en el mismo formato.
'''

from datetime import date, timedelta

try:

    f = input("Ingrese la fecha (dd mm yyyy): ").strip()
    dd, mm, yyyy = map(int, f.split())

    fecha = date(yyyy, mm, dd)

<<<<<<< HEAD
print("Siguiente día: ", siguiente.strftime("%d %m %Y"))
=======
    siguiente = fecha + timedelta(days=1)

    print(siguiente.strftime("%d %m %Y"))

except ValueError:
    print("ERROR: Formato inválido o fecha no válida. Use: dd mm yyyy")
>>>>>>> 2369b41 (Manejo de errores en incrementar_dia.py)
