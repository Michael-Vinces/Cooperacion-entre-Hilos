import threading
import time
import random

class CuentaBancaria:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial
        self.bloqueo = threading.Lock() # Asegura el determinismo


    # Secciones Criticas
    def depositar(self, monto):
        with self.bloqueo:
            print(f"Depositando {monto}")
            time.sleep(random.uniform(0.1, 0.5))  
            self.saldo += monto
            print(f"Saldo después del depósito: {self.saldo}")

    def retirar(self, monto):
        with self.bloqueo:
            if self.saldo >= monto:
                print(f"Retirando {monto}")
                time.sleep(random.uniform(0.1, 0.5))  
                self.saldo -= monto
                print(f"Saldo después del retiro: {self.saldo}")
            else:
                print(f"Fallo al retirar {monto}, fondos insuficientes. Saldo actual: {self.saldo}")

def actividad_bancaria(cuenta, num_transacciones):
    for _ in range(num_transacciones):
        accion = random.choice(['depositar', 'retirar'])
        monto = random.randint(10, 100)
        if accion == 'depositar':
            cuenta.depositar(monto)
        elif accion == 'retirar':
            cuenta.retirar(monto)

# Programa principal
saldo_inicial = 1000
cuenta = CuentaBancaria(saldo_inicial)

# Crear hilos para múltiples clientes
clientes = [threading.Thread(target=actividad_bancaria, args=(cuenta, 10)) for _ in range(5)]

# Iniciar todos los hilos
for cliente in clientes:
    cliente.start()

# Esperar a que todos los hilos terminen
for cliente in clientes:
    cliente.join()

print(f"Saldo final: {cuenta.saldo}")
