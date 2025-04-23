
namespace DesignPatterns.Creational.Singleton
{
    public class ThreadSafeSingleTonWithoutLocks
    {
        private static ThreadSafeSingleTonWithoutLocks _instance = new ThreadSafeSingleTonWithoutLocks();

        static ThreadSafeSingleTonWithoutLocks() { }

        private ThreadSafeSingleTonWithoutLocks() { }

        public static ThreadSafeSingleTonWithoutLocks Instance
        {
            get
            {
                return _instance;
            }
        }
    }
}
