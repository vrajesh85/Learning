
namespace DesignPatterns.Structural.Composite.Pattern_2
{
    public class Director : CompanyEmployee
    {
        private string _name;
        private string _position;
        private string _id;
        protected List<CompanyEmployee> _employees = new List<CompanyEmployee>();

        public Director(string name, string position,string id)
        {
            _name = name;
            _position = position;
            _id = id;
        }

        public override void Add(CompanyEmployee emp) => _employees.Add(emp);
        public override void Remove(CompanyEmployee emp) => _employees.Remove(emp);
        public override bool IsComposite() => true;
        public override void ShowDetails()
        {
            Console.WriteLine($"Director details {_name}, {_position}, {_id}");
            foreach (var emp in _employees)
                emp.ShowDetails();
        }
    }
}
