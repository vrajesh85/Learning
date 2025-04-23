
namespace DesignPatterns.Creational.Singleton
{
    public class LazySingleTon
    {
        private LazySingleTon() { }

        private static Lazy<LazySingleTon> _instance = new Lazy<LazySingleTon>(() => new LazySingleTon()); 

        public static LazySingleTon Instance
        {
            get
            {
                return _instance.Value;
            }
        }
    }
}
