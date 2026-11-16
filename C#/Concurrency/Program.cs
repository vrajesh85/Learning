using System.Threading.Tasks;

namespace Concurrency
{
    internal class Program
    {
        static async Task Main(string[] args)
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

            //var nonExclusive = new NonExclusiveLocking();
            //nonExclusive.CreateThreads();

            //Task task = GetResult();
            //var awaiter = task.GetAwaiter();
            //Console.WriteLine(task.Status);
            //Console.WriteLine(awaiter.IsCompleted);

            //awaiter.OnCompleted(() =>
            //{
            //    Console.WriteLine("Task writes");
            //    try
            //    {
            //        awaiter.GetResult();
            //    }
            //    catch (Exception ex)
            //    {
            //        Console.WriteLine($"exception occured is : { ex.ToString()}" );
            //    }
            //});

            //Console.ReadLine();

            //Task result = GetResult();



            //// Implementation 1
            //var sometask = await IsBlocked();


            //// Implementation 2
            //var awaiterTask = IsBlocked().GetAwaiter();

            //awaiterTask.OnCompleted(() =>
            //{
            //    Console.WriteLine($"The result is ${awaiterTask.GetResult()}");
            //});

            System.Diagnostics.Stopwatch sw = new System.Diagnostics.Stopwatch();
            sw.Start();

            var method1result = await GetDataMethod1(); // execution will stop till we get result
            var method2result = await GetDataMethod2(); // execution will stop till we get result
            Console.WriteLine($"The result of method 1 is {method1result}");
            Console.WriteLine($"The result of method 2 is {method2result}");
            sw.Stop();
            Console.WriteLine($"The result of stop watch is {sw.Elapsed.Seconds}");


            //sw = new System.Diagnostics.Stopwatch();
            //sw.Start();
            var task1 = GetDataMethod1(); // execution will NOT stop till we get result
            var task2 = GetDataMethod2(); // execution will NOT stop till we get result
            await task2;

            Console.WriteLine($"The result of method 2 is {task2.Result}");
            await task1;
            Console.WriteLine($"The result of method 1 is {task1.Result}");
            sw.Stop();
            Console.WriteLine($"The result of stop watch is {sw.Elapsed.Seconds}");
        }

        static async Task<int> GetDataMethod1()
        {
            await Task.Delay(8000);
            return 10;
        }

        static async Task<int> GetDataMethod2()
        {
            return await Task.FromResult(20);
        }
.
        static async Task GetResult()
        {
            await Task.Delay(3000);
            // throw new NotImplementedException();
            Console.WriteLine("Print from GetResult");
        }

        static Task<bool> IsBlocked() => Task.FromResult(true);

       
        static async Task<int> GetException(int val)
        {
            if (val < 0)
                throw new Exception("Value is less than zero");
            else return await Task.FromResult(val);
        }
    }
}
