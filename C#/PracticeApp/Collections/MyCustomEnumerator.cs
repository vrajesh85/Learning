using System;
using System.Collections;
using System.Collections.Generic;

namespace PracticeApp.Collections
{
    public class MyCustomEnumerator : IEnumerator
    {
        public string[] List { get; set; }
        public string stringLine { get; set; }
        public int Count { get; set; } = 0;
        public bool HasRecords => List.Length != Count;
        
        public bool MoveNext()
        {
            while (HasRecords)
            {
                Current = List[Count];
                Count++;
                Console.WriteLine(Current);
            }
            return false;
        }

        public object Current { get; set; }

        public void Reset()
        {
            Count = 0;
            MoveNext();
        }

        public string BuildRecursive(IEnumerable stringValue)
        {

            string resultString = string.Empty;
            foreach (var item in stringValue)
            {
                var element = item as IEnumerable;
                if(element != null)
                     resultString += " " + BuildRecursive(element);
                else
                     resultString += item.ToString();
            }
            stringLine += " " + resultString;
            return resultString;
        }
    }

    public class MyCollectionEnumerable : IEnumerable
    {
        public int[] data = { 1, 2, 3 };

        public IEnumerator GetEnumerator()
        {
           foreach(var item in data)
                if (item != 1)
                yield return item;
        }

        public IEnumerable<int> GetEvenNumbersWithYieldReturn(int count)
        {
            for(int i =0; i <= count; i+=2)
            {
                yield return i;
                Console.WriteLine($"This will get executed with value after {i}");
            }
        }

        public void GetEvenNumbersWithoutYieldReturn(int count)
        {
            for (int i = 0; i <= count; i += 2)
            {
                Console.WriteLine($"value is  {i}");
            }
        }

        public IEnumerable<int> GetNumbers()
        {
            yield return 1;
            yield return 2;
            yield return 3;
        }
    }
}
