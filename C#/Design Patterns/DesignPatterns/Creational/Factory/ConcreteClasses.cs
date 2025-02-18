using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DesignPatterns.Creational.Factory
{
    public class TwoWheeler : Vehicle
    {
        public override void Print()
        {
            Console.WriteLine("This is two wheeler");
        }
    }
    public class ThreeWheeler : Vehicle
    {
        public override void Print()
        {
            Console.WriteLine("This is three wheeler");
        }
    }

    public class FourWheeler : Vehicle
    {
        public override void Print()
        {
            Console.WriteLine("This is four wheeler");
        }
    }
}
