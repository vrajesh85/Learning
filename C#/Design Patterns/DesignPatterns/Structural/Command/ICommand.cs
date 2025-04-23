
namespace DesignPatterns.Structural.Command
{
    public interface ICommand
    {
        void TurnOn();
        void TurnOff();
    }

    public interface IDevice
    {
        void Start();
        void Stop();
    }

    public class TV : IDevice
    {
        public void Start()
        {
            Console.WriteLine("Tv has turned ON");
        }

        public void Stop()
        {
            Console.WriteLine("TV has turned OFF");
        }
    }

    public class Command : ICommand
    {
        private IDevice _device;
        public Command(IDevice device)
        {
            _device = device;
        }
        public void TurnOn()
        {
            _device.Start();
        }
    
        public void TurnOff() 
        { 
           _device.Stop();
        }
    }
}
