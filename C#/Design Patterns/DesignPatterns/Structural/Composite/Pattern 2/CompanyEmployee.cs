using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DesignPatterns.Structural.Composite.Pattern_2
{
    public abstract class CompanyEmployee
    {
        public virtual void Add(CompanyEmployee emp) => throw new NotImplementedException();
        public virtual void Remove(CompanyEmployee employee) => throw new NotImplementedException();
        public virtual bool IsComposite() => false;
        public abstract void ShowDetails();
    }
}
