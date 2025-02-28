using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DesignPatterns.Structural.Composite.Pattern_2
{
    internal class Employee : CompanyEmployee
    {
        private string _name;
        private string _position;
        private string _id;

        public Employee(string name, string position,string id)
        {
            _name = name;
            _position = position;
            _id = id;
        }

        public override void ShowDetails() => Console.WriteLine($"\tEmployee details are {_name}, {_position}, {_id}");
    }
}
