
namespace DesignPatterns.Creational.Singleton
{
    public class LazyThreadSafe
    {
        //  private LazyThreadSafe() { }
        public int value = 10;
        public static LazyThreadSafe Instance
        {
            get
            {
                return Nested.Instance;
            }
        }

        private class Nested
        {
            static Nested() { }

            internal static readonly LazyThreadSafe Instance = new LazyThreadSafe();
        }
    }
}
