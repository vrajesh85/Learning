
namespace IO_Operations.FileOperations
{
    public interface IFileOperations
    {
         void Write(string path, byte[] buffer);
         void Read(string path, byte[] buffer);
         void ReadWrite(string readPath, string writePath);
    }
}
