using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace OOPsConcepts.Inheritance
{
    internal class ChildClass : BaseClass
    {
        public override void PrintName()
        {
            Console.WriteLine("This is print name from child class");
        }

        public override void PrintDescription()
        {
            Console.WriteLine("This will print description");
        }
    }
}
