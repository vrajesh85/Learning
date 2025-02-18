using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DesignPatterns.Creational.Factory
{
    // Concrete Factory    
    public class Factory : IFactory
    {
        public Vehicle? Create(VehicleType type)
        {
            switch (type)
            {
                case VehicleType.Two:
                    return new TwoWheeler();

                case VehicleType.Three:
                    return new ThreeWheeler();

                case VehicleType.Four:
                    return new FourWheeler();
                default:
                    return null;
            }
        }
    }
}
