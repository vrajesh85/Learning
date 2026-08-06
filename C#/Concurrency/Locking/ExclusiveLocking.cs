using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Concurrency.Locking
{
    public class ExclusiveLocking
    {
        bool flag = false;
        object _locker = new object();
        public void LockWithTasks()
        {
            lock(_locker)
            {
                if (!flag)
                {
                    Console.WriteLine("Inside LockWithTasks");
                }
                flag = true;
            }
        }
    }
}
