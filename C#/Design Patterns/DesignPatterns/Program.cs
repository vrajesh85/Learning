using DesignPatterns.Creational.Factory;

namespace DesignPatterns
{
    internal class Program
    {
        static void Main(string[] args)
        {
            #region Factory

            Factory factory = new Factory();
            Client objClient = new Client(factory);
            objClient.Build(VehicleType.Four)?.Print();
            objClient.Build(VehicleType.Three)?.Print();
            objClient.Build(VehicleType.Two)?.Print();  

            #endregion
        }
    }
}