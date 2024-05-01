import threading
import time
import random

class Cine:
    def __init__(self, asientos_por_fila):
        self.asientos = [False] * asientos_por_fila  # False indica que el asiento está libre
        self.bloqueo = threading.Lock()

    def comprar_asientos(self, num_asientos):
        with self.bloqueo:
            asientos_libres = [idx for idx, libre in enumerate(self.asientos) if not libre]
            if len(asientos_libres) >= num_asientos:
                for i in range(num_asientos):
                    self.asientos[asientos_libres[i]] = True  # Marcar asientos como ocupados
                print(f"Asientos {asientos_libres[:num_asientos]} comprados exitosamente.")
                return True
            else:
                print("No hay suficientes asientos disponibles para comprar.")
                return False

def cliente(cinema):
    num_asientos = random.randint(1, 5)  # Número aleatorio de asientos que el cliente desea comprar
    time.sleep(0.3)  # Simular retraso
    cinema.comprar_asientos(num_asientos)

# Configuración inicial del cine
fila_cine = Cine(20)  # 50 asientos en la fila

# Crear hilos para clientes intentando comprar un número aleatorio de asientos
clientes = [threading.Thread(target=cliente, args=(fila_cine,)) for _ in range(9)]

# Iniciar todos los hilos
for c in clientes:
    c.start()

# Esperar a que todos los hilos terminen
for c in clientes:
    c.join()

print("\nSala 1: Aforo completo")
