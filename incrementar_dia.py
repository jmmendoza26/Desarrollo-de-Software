'''
Lee una fecha en formato: dd mm yyyy
Imprime la fecha del día siguiente en el mismo formato.
'''

from datetime import date, timedelta

f = input("Ingrese la fecha (dd mm yyyy): ").strip()
dd, mm, yyyy = map(int, f.split())

fecha = date(yyyy, mm, dd)

siguiente = fecha + timedelta(days=1)

print("Siguiente día: ", siguiente.strftime("%d %m %Y"))
