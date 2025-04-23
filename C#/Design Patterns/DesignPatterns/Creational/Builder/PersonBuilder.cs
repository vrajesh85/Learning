
namespace DesignPatterns.Creational.Builder
{
    public class PersonBuilder
    {
        private string? _name;
        private int _age;
        private string? _address;

        public PersonBuilder WithName(string name)
        {
            this._name = name;
            return this;
        }

        public PersonBuilder WithAge(int age)
        {
            this._age = age;
            return this;
        }

        public PersonBuilder WithAddress(string address) 
        {  
            this._address = address; 
            return this; 
        }

        public Person Build()
        {
            return new Person
            {
                Age = _age,
                Address = _address,
                Name = _name
            };
        }
    }

    public class Person : ICloneable
    {
        public string? Address { get; set; }
        public string? Name { get; set; }
        public int Age { get; set; }

        public object Clone()
        {
            return this.MemberwiseClone();
        }
    }
}
