
namespace DesignPatterns.Structural.Composite.Pattern_2
{
    public class Manager : CompanyEmployee
    {
        private string _name;
        private string _position;
        private string _id;
        protected List<CompanyEmployee> _employees = new List<CompanyEmployee>();

        public Manager(string name, string position, string id)
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
            Console.WriteLine($"  Manager details are : {_name}, {_position}, {_id}");
            foreach (var emp in _employees)
                emp.ShowDetails();
        }
    }
}
