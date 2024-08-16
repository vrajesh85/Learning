using System;
using System.Data.Common;
using System.Xml.Serialization;

namespace App
{
    internal class Program
    {
        static void Main(string[] args)
        {
            #region 
            Point objPoint1 = new Point(10, 20);
            Point objPoint2 = objPoint1 with { Y = 30 };
            
            Console.WriteLine($"objPoint1 values are {objPoint1.X}, {objPoint1.Y}"); // 10, 20
            Console.WriteLine($"objPoint2 values are {objPoint2.X}, {objPoint2.Y}"); // 10, 30

            #endregion
        }
    }

   record Point
    {
        public Point(int x, int y) => (X ,Y) = (x ,y);
        
        public int X { get; init; }
        public int Y { get; init; }
    }
}
