using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace OOPsConcepts.Inheritance
{
    public abstract class BaseClass
    {
        public virtual void PrintName()
        {
            Console.WriteLine("This is print name from base class");
        }

        public abstract void PrintDescription();
    }
}
