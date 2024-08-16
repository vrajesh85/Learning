using System;
using System.Threading.Tasks;

namespace PracticeApp.Concurrency
{
    public class Tasks
    {
        public Task TaskRun()
        {
            Task task = Task.Run(() =>
            {
                Console.WriteLine($"Task Ran at time {DateTime.Now.Ticks}");
            });

            //Task task = new Task(
            //            () => {
            //                Console.WriteLine($"Task Ran at time {DateTime.Now.Ticks}");
            //            });

            return task;
        }
    }
}
