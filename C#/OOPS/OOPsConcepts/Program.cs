using OOPsConcepts.Inheritance;

namespace OOPsConcepts
{
    public class Program
    {
        delegate void DelMethod(int x);
        static void Main(string[] args)
        {
            BaseClass objChildClass = new ChildClass();
            objChildClass.PrintName();
            DelMethod objDelegate = new SubscriberA().MethodA;
            objDelegate += new SubcriberB().MethodB;

            objDelegate(10);
        }
    }



    public class SubscriberA
    {
        public void MethodA(int x) => Console.WriteLine($"This is from subscriber A with value {x}");
    }

    public class SubcriberB
    {
        public void MethodB(int y) => Console.WriteLine($"This is from subcriber B with value {y}");
    }
}