using System;
using System.Threading;

class Program
{
    private static int counter = 0;  // Contador compartido
    private static object lockObject = new object();  // Objeto para sincronización

    public static void IncrementCounter()
    {
        for (int i = 0; i < 10000; i++)
        {
            // Uso de lock para garantizar que solo un hilo modifique el contador a la vez
            lock (lockObject)
            {
                counter++;
            }
        }
    }

    static void Main(string[] args)
    {
        Thread t1 = new Thread(new ThreadStart(IncrementCounter));
        Thread t2 = new Thread(new ThreadStart(IncrementCounter));

        t1.Start();  // Iniciar el primer hilo
        t2.Start();  // Iniciar el segundo hilo

        t1.Join();  // Esperar a que el primer hilo termine
        t2.Join();  // Esperar a que el segundo hilo termine

        Console.WriteLine($"Final counter value: {counter}");
    }
}
