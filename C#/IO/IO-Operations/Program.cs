using IO_Operations.FileOperations;
using static System.Runtime.InteropServices.JavaScript.JSType;


namespace IO_Operations
{
    internal class Program
    {
        static void Main(string[] args)
        {
            IFileOperations operations = new FileStreamHandlers();
            byte[] data = File.ReadAllBytes(@"C:\Temp\File.txt");
            operations.Write("writefile.txt", data);
        }
    }
}
