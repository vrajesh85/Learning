using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace Concurrency.Locking
{
    public class NonExclusiveLocking 
    {
        SemaphoreSlim semaphoreSlim = new SemaphoreSlim(3);

        public void CreateThreads()
        {
            for(int i = 1; i <= 5; i++)
            {
                new Thread(EnterIn).Start(i);
            }
        }

        public void EnterIn(object id)
        {
            Console.WriteLine($"{id} wants to enter");
            semaphoreSlim.Wait();
            Console.WriteLine($"{id} entered");
            Thread.Sleep(2000);
            semaphoreSlim.Release();
            Console.WriteLine($"{id} exit");
        }
    }
}
