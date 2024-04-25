import threading
import queue
import time
import random

# Colas thread-safe
pedido_queue = queue.Queue()
cocinado_queue = queue.Queue()

def recepcionista(id, pedido_queue):
    for _ in range(10):  # Cada recepcionista toma 10 pedidos
        pedido = random.randint(1, 100)
        print(f"Recepcionista {id} tomando pedido {pedido}")
        pedido_queue.put(pedido)
        time.sleep(random.random())  # Tiempo para tomar el siguiente pedido

def cocinero(id, pedido_queue, cocinado_queue):
    while not pedido_queue.empty():
        pedido = pedido_queue.get()
        print(f"Cocinero {id} cocinando pedido {pedido}")
        cocinado_queue.put((id, pedido))  # Añade el id del cocinero para seguimiento
        time.sleep(random.random() * 2)  # Tiempo para cocinar

def entregador(id, cocinado_queue):
    while not cocinado_queue.empty():
        cocinero_id, pedido = cocinado_queue.get()
        print(f"Entregador {id} entregando pedido {pedido} cocinado por Cocinero {cocinero_id}")
        time.sleep(random.random())  # Tiempo para entregar el pedido

# Crear y empezar hilos
recepcionistas = [threading.Thread(target=recepcionista, args=(i, pedido_queue)) for i in range(2)]
cocineros = [threading.Thread(target=cocinero, args=(i, pedido_queue, cocinado_queue)) for i in range(3)]
entregadores = [threading.Thread(target=entregador, args=(i, cocinado_queue)) for i in range(2)]

# Iniciar todos los hilos
for t in recepcionistas + cocineros + entregadores:
    t.start()

# Esperar a que todos los hilos terminen
for t in recepcionistas + cocineros + entregadores:
    t.join()

print("Todos los pedidos han sido procesados y entregados.")
