using Microsoft.Win32.SafeHandles;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PracticeApp.Design_Patterns
{
    public class Subject : IObservable<string>
    {
        public IList<IObserver<string>> Observers { get; set; } = new List<IObserver<string>>();
        public IDisposable Subscribe(IObserver<string> observer)
        {
            if(!Observers.Contains(observer))  
                Observers.Add(observer);
            return new Unsubscriber(Observers,observer);
        }

        public void NotifyObservers()
        {
            int count = 1;
            foreach(var observer in Observers)
            {
                observer.OnNext($"observer count is {count}");
                ++count;
            }
        }
    }

    public class Unsubscriber : IDisposable
    {
        private IList<IObserver<string>> _observers = new List<IObserver<string>>();
        private IObserver<string> _observer;

        public Unsubscriber(IList<IObserver<string>> observers, IObserver<string> observer)
        {
            this._observers = observers;
            this._observer = observer;
        }

        public void Dispose()
        {
            if (this._observers != null && this._observers.Contains(this._observer))
                this._observers.Remove(this._observer);
        }
    }


    public class Observer : IObserver<string>
    {
        void IObserver<string>.OnCompleted()
        {
            throw new NotImplementedException();
        }

        void IObserver<string>.OnError(Exception error)
        {
            throw new NotImplementedException();
        }

        void IObserver<string>.OnNext(string value)
        {
            Console.WriteLine($"This is coming from {value}");
        }
    }
}
