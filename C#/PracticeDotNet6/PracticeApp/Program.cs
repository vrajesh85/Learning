
using System.Text;

Point p1 = new Point();
p1.x = 1;
Point p2 = p1; // Assignment causes copy

Console.WriteLine($"value of p1 x is {p1.x}");
p1.x = 2;
Console.WriteLine($"value of p1 x is {p1.x} and p2 x is {p2.x}");

PointClass p3 = new PointClass();
p3.x = 3;
PointClass p4 = p3; // Assignment causes the copy of reference variable not actual object

Console.WriteLine($"value of p3 x is {p3.x}");
p3.x = 2;
Console.WriteLine($"value of p3 x is {p3.x} and p4 x is {p4.x}");

float f = 4.5F;

StringBuilder sb = new StringBuilder();
Foo(sb);
Console.WriteLine($" the value of sb is { sb.ToString()}");

void Foo(StringBuilder? fooSB)
{
    fooSB?.Append("test");
    fooSB = null;
}

PointClass objPointClassOutside = new PointClass();

objPointClassOutside.x = 10;
objPointClassOutside.y = 20;

Change(objPointClassOutside);
Console.WriteLine($"objPointClassOutside X value is {objPointClassOutside.x}"); // value will be 100

void Change(PointClass obj)
{
    obj.x = 100;
    obj.y = 200;
    obj = null;
}

string str = "Rajesh";
ChangeString(str);
Console.WriteLine($"The value of str is {str}");
void ChangeString(string obj)
{    
    obj = "test";
}

int initialValue = 0;
ChangeInt(ref initialValue);
Console.WriteLine($"The value of initial value is {initialValue}");

void ChangeInt(ref int temp)
{ 
    initialValue = 20;
    temp = 10;
    Console.WriteLine($"The value of temp is {temp}");
}

char[] vowels = new char[] { 'a', 'e', 'i', 'o', 'u' };
Index last = ^1;
Console.WriteLine($"the value is {vowels[last]}");
Console.WriteLine($"{vowels[..3]}");

Console.WriteLine($" the value of float is greater than 4 --> {f > 4}");

string valueType = "string" switch
{
    string => "it's a string",
    _ => "test"
};

Console.WriteLine(valueType);

void PrintType(object obj)
{
    switch (obj)
    {
        case float f:
            Console.WriteLine($"");
        break;
        case double d: Console.WriteLine($"");
            break;
        case string s: Console.WriteLine($"");
            break;
        default: Console.WriteLine($"");
            break;
    }
}



public struct Point { public int x; public int y; };
public class PointClass {  public int x; public int y; }

