using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DesignPatterns.Creational.Builder
{
    internal class CompletePerson : IPerson
    {
        public string Name { get; set; }
        public int Age { get; set; }
        public string Address { get; set; }
        public IPerson WithAge(int age)
        {
          this.Age = age;
          return this;
        }
        public IPerson WithAddress(string address)
        {
          this.Address = address;
          return this;
        }
        public IPerson WithName(string name)
        {
          this.Name = name;
          return this;
        }           
    }

    public interface IPerson
    {
        string Name { get; set; }
        int Age { get; set; }
        string Address { get; set; }
        IPerson WithAge(int age);
        IPerson WithAddress(string address);
        IPerson WithName(string name);
    }
}
