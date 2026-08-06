using Concurrency.Locking;

namespace Concurrency
{
    internal class Program
    {
        static void Main(string[] args)
        {
            //Thread t1 = new Thread(() =>
            //{
            //    for (int i = 0; i < 5; i++)
            //    {
            //        Console.WriteLine("X");
            //    }
            //});
            //Thread t2 = new Thread(() =>
            //{
            //    t1.Join();
            //    for (int i = 0; i < 5; i++)
            //    {
            //        Console.WriteLine("Y");
            //    }
            //});
            //t1.Start();
            //t2.Start();

            //t2.Join();
            //Console.WriteLine("End reached");

            //// Signaling
            //var signal = new ManualResetEvent(false);
            //new Thread(() =>
            //{
            //    Console.WriteLine("Thread started..");
            //    signal.WaitOne();
            //    signal.Dispose();
            //    Console.WriteLine("Thread ended..");
            //}).Start();

            //Console.WriteLine("main thread");
            //Thread.Sleep(3000);
            //signal.Set();

            //var objLocking = new ExclusiveLocking();
            //Task t1 = Task.Run(() => objLocking.LockWithTasks());
            //Task t2 = Task.Run(() => objLocking.LockWithTasks());
            //Task t3 = Task.Run(() => objLocking.LockWithTasks());

            //Task.WaitAll(t1, t2, t3);

            var nonExclusive = new NonExclusiveLocking();
            nonExclusive.CreateThreads();

        }
    }
}
