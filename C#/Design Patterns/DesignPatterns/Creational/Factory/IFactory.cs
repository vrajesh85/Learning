using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DesignPatterns.Creational.Factory
{
    public interface IFactory
    {
        Vehicle? Create(VehicleType type);
    }

    public abstract class Vehicle
    {
        public abstract void Print();
    }
}
