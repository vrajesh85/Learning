using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DesignPatterns.Creational.Factory
{
    public class Client
    {    
        private IFactory _factory;
        public Client(IFactory factory)         
        {
            _factory = factory;
        }
        public Vehicle? Build(VehicleType type) => _factory.Create(type);        
    }

    public enum VehicleType
    {
        Two,
        Three,
        Four
    }
}
