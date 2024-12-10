using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using PracticeApp.Concurrency;
using System.Threading.Tasks;
using PracticeApp.Regular_Expressions;
using System.Collections;
using PracticeApp.Design_Patterns;
using System.Data.Common;
using System.IO;
using System.Text.RegularExpressions;

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
        static CancellationTokenSource cts = new CancellationTokenSource();
        static Basics regularExpBasics = new Basics();

        static void Main(string[] args)
        {
            #region RegularExpressions

            //Match match = regularExpBasics.GetMatch("One colors ? There are two colourss in my head", "colou?rs");

            //Match match2 = match.NextMatch();

            //Console.WriteLine(Regex.Escape(@"?")); // \?
            //Console.WriteLine(Regex.Unescape(@"\?")); // ?

            //Console.WriteLine($"Do they match  { regularExpBasics.DoTheyMatch("colours are ?", @"(?i)COLOu?rs are \?")}");

            //Console.WriteLine($"Do they match { regularExpBasics.DoTheyMatch("b1-c444", @"[a-b]\d-[c-d]\d*")}");

            //Console.WriteLine($"Does this email match ? { regularExpBasics.DoTheyMatch("abc855@Gmail.com", @"[a-zA-Z]\d*\@[a-zA-Z].[a-zA-Z]")}");

            //Console.WriteLine($"The value is {regularExpBasics.GetMatch("quiz qwerty",@"q[^aeiou]").ToString() }");

            //Console.WriteLine($"This string contains punctuation ? { Regex.IsMatch("Yes : please", @"\p{P}") }");

            //// Quantifiers

            //Console.WriteLine($"Do these words match ? { regularExpBasics.DoTheyMatch("Vemulakonda", @"[a-zA-Z]+") }");

            //Console.WriteLine($"My Blood pressure is { regularExpBasics.GetMatch("123456789/8000",@"\d{2,3}/\d{2,3}") }"); // 789/800

            //Console.WriteLine(Regex.IsMatch($"cv.dcx",@"cv.*\.dcx"));

            //Console.WriteLine(Regex.IsMatch($"rajesh123", "[a-zA-Z0-9]+")); // [a-zA-Z0-9]+

            //string html = "<i>By default</i>  <i>greedy</i> creatures happen to very greedy and <i></i>";
            //// greedy quantifier
            //foreach (var match in Regex.Matches(html, @"<i>.*</i>"))
            //    Console.WriteLine($"The value with greedy quantifier is {match}");

            ////lazy quantifier
            //foreach(var match in Regex.Matches(html, @"<i>.*?</i>"))
            //    Console.WriteLine($"The value with lazy qunantifiers {match}");

            // positive lookahead
            //string match = Regex.Match("I have 10           cups", @"\d+\s+(?=cups)").ToString();
            //Console.WriteLine($"Is that true  {match}");

            //negative lookahead
            string match = "Don't look for quick hack or quick fix";
            Console.WriteLine(Regex.Match(match, @"(?i)(?!.*(quick))"));

            // basic password match positive lookahead
            // Console.WriteLine($"password is 6 chars long with at least one digit --> { Regex.IsMatch("Rajesh1", @"(?=.*\d).{6,}") }");

            // positive lookbehind
            // Console.WriteLine($" { Regex.IsMatch("","") } ");



            // word boundary
            //foreach (Match m in Regex.Matches("Hello 123", @"\w+"))
            //    Console.WriteLine(m);

            //string pattern = @"\bword\b";
            //string input = "word words sword word.";

            //foreach (Match m in Regex.Matches(input, pattern))
            //    Console.WriteLine(m);

            //string pattern = @"I have a (cat|dog) what is your name \?";

            //string actualString = "I have a dog what is your name ?";

            //MatchCollection matches = Regex.Matches(actualString, pattern);

            //foreach(var item in matches)
            //{
            //    Console.WriteLine(item);5 

            //}

            //pattern = @"[^abc][d-f][a-b]";

            //actualString = "dec";



            //Console.WriteLine($"Do they match  { regularExpBasics.DoTheyMatch(actualString, pattern) }");

            #endregion

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
            //SubscriberAngleOne angelOne = new SubscriberAngleOne();
            //SubscriberZerodha zerodha = new SubscriberZerodha();
            //objStock.PriceChangedHandler += zerodha.OnStockPriceChanged1;
            //objStock.PriceChangedHandler += angelOne.OnStockPriceChanged2;
            //objStock.Price = 100;
            //objStock.Price = 200;

            //Bar((int x) => Foo(x));

            #endregion

            #region LamdaExpressions

            //Console.WriteLine("The value is " + Natural().Invoke());
            //Console.WriteLine("The value is " + Natural().Invoke());
            //Console.WriteLine("The value is " + Natural().Invoke());

            //Action[] actions = new Action[3];
            //for(int i = 0; i < 3; i++)
            //{
            //    actions[i] = () => Console.WriteLine($"value is {i}"); // 3 3 3
            //}

            //foreach(Action action in actions)
            //    action();

            //for(int i = 0; i < 3; i++)
            //{
            //    int localVariable = i;
            //    actions[i] = () => Console.WriteLine($"value is {localVariable}"); // 0 1 2 
            //}

            //foreach (Action action in actions)
            //   action();

            //foreach (var element in GetFibnocciNumbers(10))
            //    Console.Write(element + " ");

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

            //var task = new Tasks();
            //Task resultTask = task.TaskRun();
            //resultTask.Start();
            //resultTask.Wait();

            //TaskStatus isTrue = resultTask.Status;

            //var status = resultTask.Status;
            //var isCompleted = $"status is {resultTask.IsCompleted}";

            //Console.WriteLine($"is task completed {resultTask.IsCompleted} and " +
            //  $"status is {resultTask.Status} at time {DateTime.Now.Ticks}");

            #endregion

            #region Collections

            //int[] array1 = new int[] {1,2,3};
            //int[] array2 = new int[] {1,2,3};

            //string[] strArray = { "Rajesh", "Vemulakonda", "Rodnay" };

            //Console.WriteLine(Array.Find(strArray, n => n.Contains('a')));

            //string[] strResult = Array.FindAll(strArray, n => n.Contains('a'));
            //Array.ForEach(strResult, Console.WriteLine);
            ////Console.WriteLine(array1.Equals(array2)); // false

            //Console.WriteLine(1 % 2);
            //Console.WriteLine(2 % 1);

            //IStructuralEquatable se1 = array1;
            //// compares every element of the array 
            //Console.WriteLine(se1.Equals(array2, StructuralComparisons.StructuralEqualityComparer)); // true

            // Array.ForEach(array1, Console.WriteLine);



            //MyCustomEnumerator objEnumerator = new MyCustomEnumerator();
            //objEnumerator.List = new string[]
            //{
            //    "V R Pantulu",
            //    "V Kasturi",
            //    "Rajesh",
            //    "Srividya",
            //    "Ashritha",
            //    "Ananya"
            //};

            //while (objEnumerator.MoveNext())
            //{
            //    //
            //}
            ////objEnumerator.Reset();
            //objEnumerator.BuildRecursive(objEnumerator.List);
            //Console.WriteLine(objEnumerator.stringLine);


            //MyCollectionEnumerable objEnumerable = new MyCollectionEnumerable();
            ////var enumerator = objEnumerable.GetEnumerator();
            ////enumerator.MoveNext();
            ////int current = (int)enumerator.Current;

            //System.Diagnostics.Stopwatch sw = new System.Diagnostics.Stopwatch();
            //sw.Start();
            //if(objEnumerable.GetEvenNumbersWithYieldReturn(10).Any())
            //    foreach (var num in objEnumerable.GetEvenNumbersWithYieldReturn(10))
            //    Console.WriteLine($"value is  {num}");
            //sw.Stop();

            //var elapsed = sw.Elapsed;

            //Console.WriteLine($"time taken with yield return is {elapsed.Seconds} and {elapsed.Milliseconds}");

            //sw.Start();
            //objEnumerable.GetEvenNumbersWithoutYieldReturn(10);
            //sw.Stop();

            //elapsed = sw.Elapsed;

            //Console.WriteLine($"time taken without yield return is {elapsed.Seconds} and {elapsed.Milliseconds}");

            #endregion

            #region Design Patterns

            //var objSender = new Subject();
            //var objObserver1 = new Observer();
            //var objObserver2 = new Observer();
            //var objObserver3 = new Observer();

            //objSender.Subscribe(objObserver1);
            //objSender.Subscribe(objObserver2);
            //objSender.Subscribe(objObserver3);

            //objSender.NotifyObservers();

            #endregion
        }

        public static async Task WriteAllContentToFile(string path, string content, CancellationToken token)
        {
            byte[] bytes = Encoding.UTF8.GetBytes(content);
            await WriteBytesInBatchSizeAsync(path, bytes, 1024, token);
        }

        public static async Task WriteAllContentToFile(string path, byte[] content, CancellationToken token)
        {
            await WriteBytesInBatchSizeAsync(path, content, 1024, token);
        }

        private static async Task WriteBytesInBatchSizeAsync(string filePath, byte[] data, int batchSize, CancellationToken token)
        {
            using (FileStream fileStream = new FileStream(filePath, FileMode.Create, FileAccess.Write, FileShare.None, bufferSize: 4096, useAsync: true))
            {
                for (int offset = 0; offset < data.Length; offset += batchSize)
                {
                    if (!token.IsCancellationRequested)
                    {
                        // Determine the size of the current batch
                        int size = Math.Min(batchSize, data.Length - offset);
                        byte[] batch = new byte[size];

                        // Copy the current batch into a new array
                        Array.Copy(data, offset, batch, 0, size);

                        // Write the batch asynchronously
                        await fileStream.WriteAsync(batch, 0, size, token);
                    }
                }
            }
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

        static void Foo<T>(T x) { Console.WriteLine($"entered type is {x.GetType()}"); }
        static void Bar<T>(Action<T> x) { }

        static Func<int> Natural()
        {
            return () =>
            {
                int seed = 0;
                return ++seed;
            };
        }

        static IEnumerable<int> GetFibnocciNumbers(int count)
        {
            for(int i = 0, prevFib = 1, currentFib = 1; i < count; i++)
            {
                yield return prevFib;
                int result = prevFib + currentFib;
                prevFib = currentFib;
                currentFib = result;       
                if (i > 5)
                    yield break;
            }
        }

        public class SubscriberZerodha
        {            
            public void OnStockPriceChanged1(object sender, PriceChangedEventArgs e)
            {
                if (e.OldPrice != e.NewPrice)
                    Console.WriteLine($"Price changed event from Zerodha");
            }
        }

        public class SubscriberAngleOne
        {
            public void OnStockPriceChanged2(object sender, PriceChangedEventArgs e)
            {
                if (e.OldPrice != e.NewPrice)
                    Console.WriteLine($"Price changed event from AngelOne");
            }
        }

        

        
    }

}
