class Restaurante {
    // Estado para controlar cuando un pedido está listo
    boolean pedidoListo = false;

    // Método sincronizado para que el cliente haga un pedido
    public synchronized void hacerPedido(String cliente) throws InterruptedException {
        while (pedidoListo) {
            wait(); // Espera si hay un pedido en proceso
        }
        System.out.println(cliente + " hace un pedido.");
        pedidoListo = true;
        notifyAll(); // Notifica que hay un nuevo pedido
    }

    // Método sincronizado para que el mesero procese el pedido
    public synchronized void procesarPedido() throws InterruptedException {
        while (!pedidoListo) {
            wait(); // Espera hasta que haya un pedido
        }
        System.out.println("El mesero toma el pedido y lo pasa al cocinero.");
        notifyAll(); // Notifica al cocinero que puede empezar a cocinar
    }

    // Método sincronizado para que el cocinero prepare el pedido
    public synchronized void prepararPedido() throws InterruptedException {
        while (!pedidoListo) {
            wait(); // Espera hasta que el mesero procese el pedido
        }
        System.out.println("El cocinero prepara la comida.");
        Thread.sleep(1000); // Simula el tiempo de preparación
        System.out.println("El cocinero termina de preparar la comida y está lista para servir.");
        pedidoListo = false;
        notifyAll(); // Notifica a los clientes que el pedido está listo
    }
}

class Cliente extends Thread {
    private Restaurante restaurante;
    private String nombre;

    public Cliente(Restaurante restaurante, String nombre) {
        this.restaurante = restaurante;
        this.nombre = nombre;
    }

    public void run() {
        try {
            restaurante.hacerPedido(this.nombre);
            Thread.sleep(5000); // Espera antes de hacer otro pedido
        } catch (InterruptedException e) {
            System.out.println("Cliente interrumpido.");
        }
    }
}

class Mesero extends Thread {
    private Restaurante restaurante;

    public Mesero(Restaurante restaurante) {
        this.restaurante = restaurante;
    }

    public void run() {
        try {
            while (true) {
                restaurante.procesarPedido();
                Thread.sleep(100); // Da un pequeño respiro para evitar uso excesivo del CPU
            }
        } catch (InterruptedException e) {
            System.out.println("Mesero interrumpido.");
        }
    }
}

class Cocinero extends Thread {
    private Restaurante restaurante;

    public Cocinero(Restaurante restaurante) {
        this.restaurante = restaurante;
    }

    public void run() {
        try {
            while (true) {
                restaurante.prepararPedido();
                Thread.sleep(100); // Da un pequeño respiro para evitar uso excesivo del CPU
            }
        } catch (InterruptedException e) {
            System.out.println("Cocinero interrumpido.");
        }
    }
}

public class SimulacionRestaurante {
    public static void main(String[] args) {
        Restaurante restaurante = new Restaurante();
        Cliente cliente1 = new Cliente(restaurante, "Cliente 1");
        Cliente cliente2 = new Cliente(restaurante, "Cliente 2");
        Mesero mesero = new Mesero(restaurante);
        Cocinero cocinero = new Cocinero(restaurante);

        cliente1.start();
        cliente2.start();
        mesero.start();
        cocinero.start();
    }
}
