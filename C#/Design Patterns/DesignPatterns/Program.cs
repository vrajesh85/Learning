using DesignPatterns.Creational.Builder;
using DesignPatterns.Creational.Factory;
using DesignPatterns.Creational.Singleton;
using DesignPatterns.Structural.Command;
using DesignPatterns.Structural.Composite.Pattern_1;
using DesignPatterns.Structural.Composite.Pattern_2;
using DesignPatterns.Structural.Decorator;
using System.ComponentModel.DataAnnotations;
using System.Windows.Input;
using ICommand = DesignPatterns.Structural.Command.ICommand;

namespace DesignPatterns
{
    internal class Program
    {
//Adapter
//Decorator
//Facade
//Composite
//Proxy
//Observer
//State
//Strategy
//Chain Of Responsibility


        static void Main(string[] args)
        {
            #region Creational

            #region Factory

            //IFactory factory = new Factory();
            //Client objClient = new Client(factory);
            //objClient.Build(VehicleType.Four)?.Print();
            //objClient.Build(VehicleType.Three)?.Print();
            //objClient.Build(VehicleType.Two)?.Print();

            #endregion

            #region SingleTon

            //var objThreadSafeSingleTon = ThreadSafeSingleTonWithoutLocks.Instance;

            //var lazyThreadSafe = LazyThreadSafe.Instance;
            #endregion

            #region Builder

            //var person = new PersonBuilder()
            //                 .WithName("Rajesh")
            //                 .WithAddress("Hyd")
            //                 .WithAge(39)
            //                 .Build();

            //var person2 = new CompletePerson()
            //                  .WithName("Rajesh")
            //                  .WithAddress("Hyd")
            //                  .WithAge(39);


            #endregion

            #endregion

            #region Structural

            #region Composite Pattern 1

            //Directors objDirectors = new Directors("Director Sir", "Director", "A1");

            //Managers objManagers1 = new Managers("Manager Sir", "Manager 1", "B1");
            //Managers objManagers2 = new Managers("Manager Sir", "Manager 2", "B2");

            //Employees objEmployee1 = new Employees("Employee", "Employee 1", "E1");
            //Employees objEmployee2 = new Employees("Employee", "Employee 2", "E2");

            //CompanyDirectory companyDirectorsDirectory = new CompanyDirectory();
            //companyDirectorsDirectory.AddEmployee(objDirectors);

            //CompanyDirectory companyManagersDirectory = new CompanyDirectory();
            //companyManagersDirectory.AddEmployee(objManagers1);
            //companyManagersDirectory.AddEmployee(objManagers2);

            //CompanyDirectory companyEmployeeDirectory = new CompanyDirectory();
            //companyEmployeeDirectory.AddEmployee(objEmployee1);
            //companyEmployeeDirectory.AddEmployee(objEmployee2);

            //CompanyDirectory companyDirectory = new CompanyDirectory();

            //companyDirectory.AddEmployee(companyDirectorsDirectory);
            //companyDirectory.AddEmployee(companyManagersDirectory);
            //companyDirectory.AddEmployee(companyEmployeeDirectory);

            //companyDirectory.ShowDetails();
            #endregion

            #region Composite Pattern 2

            //Manager objManager1 = new Manager("Mr Manager A", "Manager", "M1");
            //Manager objManager2 = new Manager("Mr Manager B", "Manager", "M2");

            //Employee objEmployee1 = new Employee("Employee 1", "Employee", "E1");
            //Employee objEmployee2 = new Employee("Employee 2", "Employee", "E2");
            //Employee objEmployee3 = new Employee("Employee 3", "Employee", "E3");
            //Employee objEmployee4 = new Employee("Employee 4", "Employee", "E4");

            //objManager1.Add(objEmployee1);
            //objManager1.Add(objEmployee2);
            //objManager2.Add(objEmployee3);
            //objManager2.Add(objEmployee4);

            //Director objDirector = new Director("Mr Director", "Director", "D1");
            //objDirector.Add(objManager1);
            //objDirector.Add(objManager2);

            //objDirector.ShowDetails();

            #endregion

            #region Decorator

            //Dosa plain = new PlainDosa();
            //var objOnionDosa = new OnionDecorators(plain);
            //Console.WriteLine($"Your dosa is {objOnionDosa.GetDescription()} and cost is {objOnionDosa.GetCost()}");

            //Dosa butter = new ButterDosa();
            //var objMasalaDosa = new MasalaDecorators(butter);
            //Console.WriteLine($"Your dosa is {objMasalaDosa.GetDescription()} and cost is {objMasalaDosa.GetCost()}");

            #endregion

            #region Command

            IDevice device = new TV();
            ICommand command = new Command(device);

            command.TurnOn();
            command.TurnOff();

            #endregion

            #endregion
        }
    }
}