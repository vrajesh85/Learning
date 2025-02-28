using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DesignPatterns.Structural.Composite.Pattern_1
{
    public class Managers : IEmployee
    {
        private string _name;
        private string _position;
        private string _id;

        public Managers(string name, string position, string id)
        {
            _name = name;
            _position = position;
            _id = id;
        }
        public void ShowDetails()
        {
            Console.WriteLine($"The details are {_id}, {_name},{_position}");
        }
    }
}
