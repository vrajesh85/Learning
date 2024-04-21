using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PracticeApp
{
    internal class Program
    {
        delegate void myFirstDelegate(int percent);
        delegate T Transformer<T>(T arg);
        static void Main(string[] args)
        {
            #region Delegates

                #region DirectCalling
                var objReporter = new MyReporter();
                myFirstDelegate objDel = objReporter.ReportProgress;
                objDel(100);
                Console.WriteLine($"target instance is {objDel.Target}");
                Console.WriteLine($"method name is {objDel.Method.Name}");
                #endregion

                #region AddingDelegates
                List<Action> lstDelegates = new List<Action>();
                for(int i = 0; i < 3; i++)
                {
                    lstDelegates.Add(() => objDel(i));
                }

                foreach (var item in lstDelegates)
                {
                    item.Invoke();// value of i will be 3 and hence it value of 3 is printed 3 times
                }
                #endregion

                #region MultiCasting
                objDel += objReporter.Square;
                objDel += objReporter.Cube;
                objDel(100);

                 Func<int,int> mySecondDelegate = objReporter.GetPercent;
                 mySecondDelegate += objReporter.GetSquare;
                 mySecondDelegate += objReporter.GetCube;
                 Console.WriteLine($"Final value is {mySecondDelegate(10)}"); // 1000 will be printed as previous return values in multi cast delegates are lost

                 Action<int> myThirdDelegate = objReporter.ReportProgress;
                 myThirdDelegate += objReporter.WriteProgress;

                 MyReporter.HardWork(myThirdDelegate); // in case of void return types previous method calls also will not be lost

            #endregion

                #region GenericDelegates
                Transformer<int> intDelegate = objReporter.GetPercent;
                Transformer<string> stringDelegate = objReporter.GetString;
                Console.WriteLine($"int value is {intDelegate(10)}");
                Console.WriteLine($"string value is {stringDelegate("Rajesh")}");
            #endregion

                #region BroadCaster/Subscribers

                SubscriberX objX = new SubscriberX();
                SubscriberY objY = new SubscriberY();
                BroadCaster.BroadCasterDelegate objDelegate = objX.SubscriberExecute;
                objDelegate += objY.SubscriberExecute;
                Console.WriteLine($"target is {objDelegate.Target}");
                objDelegate(10);

                #endregion

            #endregion
        }
    }
}
