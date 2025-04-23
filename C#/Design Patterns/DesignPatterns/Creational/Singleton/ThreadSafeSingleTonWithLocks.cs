
namespace DesignPatterns.Creational.Singleton
{
    public class ThreadSafeSingleTonWithLocks
    {
        private static object _lock = new object();
        private static ThreadSafeSingleTonWithLocks? _instance;

        public int value = 10;

        private ThreadSafeSingleTonWithLocks() { }

        public static ThreadSafeSingleTonWithLocks Instance
        {
            get
            {
                lock (_lock)
                {
                    if (_instance == null)
                        _instance = new ThreadSafeSingleTonWithLocks();
                }
                return _instance;
            }            
        }
    }
}
