using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace PracticeApp
{
   public class MyReporter
    {
        public string Prefix = "Value is --> ";
        public void ReportProgress(int percentComplete)
        => Console.WriteLine(Prefix + percentComplete);
        public void WriteProgress(int percentComplete)
        => Console.WriteLine($"percentage completed is {percentComplete.ToString()}");
        public void InvokeDelegate(Action action) => action.Invoke();
        public void Square(int x) => Console.WriteLine($"square value is {x * x}");
        public void Cube(int x) => Console.WriteLine($"cube value is {x * x * x}");
        public int GetPercent(int percentComplete) => percentComplete;
        public int GetSquare(int x) =>  x * x;
        public int GetCube(int x) => x * x * x;
        public string GetString(string x) => x;
        public static void HardWork(Action<int> actionDelegate)
        {
            for(int i = 0; i < 10; i++)
            {
                actionDelegate.Invoke(i * 10);
               // Thread.Sleep(100);
            }
        }
    }

   public class BroadCaster
    {
        public delegate void BroadCasterDelegate(int x);
    }

    public class SubscriberX
    {
        public void SubscriberExecute(int x)
        {
            Console.WriteLine($"subscriber execute of x with value {x}");
        }
    }

    public class SubscriberY
    {
        public void SubscriberExecute(int x)
        {
            Console.WriteLine($"subscriber execute of y with value {x}");
        }
    }
}
