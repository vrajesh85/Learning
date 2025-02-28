using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DesignPatterns.Structural.Composite.Pattern_1
{
    public class CompanyDirectory : IEmployee
    { 
        private List<IEmployee> _employees = new List<IEmployee>();
        public void ShowDetails()
        {
            foreach(var employee in _employees)
            {
                employee.ShowDetails();
            }
        }
        public void AddEmployee(IEmployee employee) => _employees.Add(employee);
        public void RemoveEmployee(IEmployee employee) => _employees.Remove(employee);
    }
}
