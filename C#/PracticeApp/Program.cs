﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using PracticeApp.Concurrency;
using System.Threading.Tasks;

namespace PracticeApp
{
    internal class Program
    {
        delegate void myFirstDelegate(int percent);
        delegate T Transformer<T>(T arg);
        static bool flag;
        static Thread thread1, thread2;
        static Thread firstThread;
        static Thread secondThread;
        static int total = 0;
        static Thread t1;
        static Thread t2;
        static Thread t3;
        static object _locker = new object();

        static void Main(string[] args)
        {
            #region Delegates

            //#region DirectCalling
            //var objReporter = new MyReporter();
            //myFirstDelegate objDel = objReporter.ReportProgress;
            //objDel(100);
            //Console.WriteLine($"target instance is {objDel.Target}");
            //Console.WriteLine($"method name is {objDel.Method.Name}");
            //#endregion

            //#region AddingDelegates
            //List<Action> lstDelegates = new List<Action>();
            //for (int i = 0; i < 3; i++)
            //{
            //    lstDelegates.Add(() => objDel(i));
            //}

            //foreach (var item in lstDelegates)
            //{
            //    item.Invoke();// value of i will be 3 and hence it value of 3 is printed 3 times
            //}
            //#endregion

            //#region MultiCasting
            //objDel += objReporter.Square;
            //objDel += objReporter.Cube;
            //objDel(100);

            //Func<int, int> mySecondDelegate = objReporter.GetPercent;
            //mySecondDelegate += objReporter.GetSquare;
            //mySecondDelegate += objReporter.GetCube;
            //Console.WriteLine($"Final value is {mySecondDelegate(10)}"); // 1000 will be printed as previous return values in multi cast delegates are lost

            //Action<int> myThirdDelegate = objReporter.ReportProgress;
            //myThirdDelegate += objReporter.WriteProgress;

            //MyReporter.HardWork(myThirdDelegate); // in case of void return types previous method calls also will not be lost

            //#endregion

            //#region GenericDelegates
            //Transformer<int> intDelegate = objReporter.GetPercent;
            //Transformer<string> stringDelegate = objReporter.GetString;
            //Console.WriteLine($"int value is {intDelegate(10)}");
            //Console.WriteLine($"string value is {stringDelegate("Rajesh")}");
            //#endregion

            //#region BroadCaster/Subscribers

            //SubscriberX objX = new SubscriberX();
            //SubscriberY objY = new SubscriberY();
            //BroadCaster.BroadCasterDelegate objDelegate = objX.SubscriberExecute;
            //objDelegate += objY.SubscriberExecute;
            //Console.WriteLine($"target is {objDelegate.Target}");
            //objDelegate(10);

            //#endregion

            #endregion

            #region Events

            //Stock objStock = new Stock();
            //objStock.Price = 10;
            //objStock.PriceChanged += stock_PriceChanged;
            //objStock.Price = 20;

            #endregion

            #region MultiThreading

            #region Joins & Signaling

            //thread1 = new Thread(ThreadProc);
            //thread1.Name = "Thread1";
            //thread1.Start();

            //thread2 = new Thread(ThreadProc);
            //thread2.Name = "Thread2";
            //thread2.Start();

            //firstThread = new Thread(PrintX);
            //secondThread = new Thread(PrintY);

            //firstThread.Name = "First";
            //secondThread.Name = "Second";

            //firstThread.Start();
            //secondThread.Start();

            //t1 = new Thread(Increment);
            //t2 = new Thread(Increment);
            //t3 = new Thread(Increment);

            //t1.Name = "T1";
            //t2.Name = "T2";
            //t3.Name = "T3";

            //t1.Start();
            //t1.Join();

            //t2.Start();
            //t2.Join();

            //t3.Start();
            //t3.Join();

            #endregion

            #region Shared State Without Static
            //int limit = 10;
            //bool isDone = false;
            //firstThread = new Thread(() => WriteX(limit));
            //secondThread = new Thread(() => WriteY(limit));
            //firstThread.Name = "First Thread";
            //secondThread.Name = "Second Thread";
            //firstThread.Start();
            //secondThread.Start();

            //Console.WriteLine($"current thread is {Thread.CurrentThread.Name} and it's state is {Thread.CurrentThread.ThreadState}");
            //Console.WriteLine($"first thread is {firstThread.Name} and it's state is {firstThread.ThreadState}");
            //  WriteX(limit);
            #endregion

            #region Shared State With Static
            //new Thread(() => WriteY(limit)).Start();
            //WriteX(limit);
            #endregion

            #region Basic Locking
            //new Thread(Go).Start();
            //Go();
            #endregion

            #region Other Examples
            //for(int i = 0; i < 5; i++)
            //{
            //    //int temp = i;
            //    new Thread(() => Console.Write(i)).Start();
            //}

            //string str = "A";
            //var t1 = new Thread(() => Console.WriteLine(str));

            //str = "B";
            //var t2 = new Thread(() => Console.WriteLine(str));
            //t1.Start();
            //t2.Start();

            //try
            //{
            //    new Thread(ThrowNull).Start();
            //}
            //catch(Exception ex)
            //{
            //    //We never reach here..Reason : Every thread has an independent execution path and hence the above thread gets
            //    //                     struck in a method that throws null and it doesn't come back here
            //    Console.WriteLine("Exception");
            //}
            #endregion

            #region Background threads
            //Thread worker = new Thread(() => Console.ReadLine());
            //if(args.Length > 0)
            //worker.IsBackground = true;
            //worker.Start();

            #endregion

            #endregion

            #region Tasks

            var task = new Tasks();
            Task resultTask = task.TaskRun();
            resultTask.Start();
            resultTask.Wait();

            //TaskStatus isTrue = resultTask.Status;

            //var status = resultTask.Status;
            //var isCompleted = $"status is {resultTask.IsCompleted}";

            //Console.WriteLine($"is task completed {resultTask.IsCompleted} and " +
            //  $"status is {resultTask.Status} at time {DateTime.Now.Ticks}");

            #endregion
        }

        static void stock_PriceChanged(object sender, PriceChangedEventArgs e)
        {
            if (e.newPrice != e.oldPrice)
                Console.WriteLine("Event Fired --> price has changed");
        }

        static void WriteY(int limit,bool isDone)
        {
            if(!isDone)
            {
                for (int i = 0; i < limit; i++)
                {
                    Console.Write("y");
                }
            }
            isDone = true;
        }

        static void WriteX(int limit, bool isDone)
        {
            if (!isDone)
            {
                for (int i = 0; i < limit; i++)
                {
                    Console.Write("x");
                }
            }
            
        }

        static void WriteY(int limit)
        {
            if (!flag)
            {
                for (int i = 0; i < limit; i++)
                {
                    Console.Write("y");
                }
            }
            flag = true;
        }

        static void WriteX(int limit)
        {
            if (!flag)
            {
                for (int i = 0; i < limit; i++)
                {
                    Console.Write("x");
                }
            }
        }

        static void Go()
        {
            lock(_locker)
            {
                if (!flag)
                {
                   Console.WriteLine("Done");
                }
                flag = true;
            }
        }

        static void GoWithoutLockers()
        {
            if (Thread.CurrentThread.Name == "Thread1" && thread2.ThreadState != ThreadState.Unstarted)
                thread2.Join();
            if (!flag)
            {
                Console.WriteLine("Done");
            }  
            flag = true;
        }

        static void PrintX()
        {
            for(int i = 0; i< 5; i++)
            {
                Console.WriteLine("X");
            }
        }

        static void PrintY()
        {
            if (firstThread.ThreadState != ThreadState.Unstarted)
                firstThread.Join();
            for (int i = 0; i < 5; i++)
            {
                Console.WriteLine("Y");
            }
        }

        static void Increment()
        {
            for (int i = 1; i<=5; i++)
            {
                lock (_locker)
                {
                    total++;
                    Console.WriteLine($"Total value is {total} and current thread is {Thread.CurrentThread.Name}");
                }
            }
        }
        static string ThrowNull() => "";// throw null; // throws null reference exception 
    }

}