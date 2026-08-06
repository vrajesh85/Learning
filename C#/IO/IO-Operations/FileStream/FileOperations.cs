using System.IO;

namespace IO_Operations.FileOperations
{
    public class FileStreamHandlers : IFileOperations
    {
        public const int BUFFERSIZE = 4096;
        public void Read(string path, byte[] buffer)
        {
            using var myStream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read);
            for (int offset = 0; offset < buffer.Length; offset += BUFFERSIZE)
            {
                int count = Math.Min(buffer.Length - offset, BUFFERSIZE);
                int totalRead = myStream.Read(buffer, offset, count);
                if (totalRead == 0) break;
            }
        }

        public void Write(string path, byte[] buffer)
        {
            using var myStream = new FileStream(path, FileMode.Create, FileAccess.Write, FileShare.None);
            for (int offset = 0; offset < buffer.Length; offset += BUFFERSIZE)
            {
                int count = Math.Min(BUFFERSIZE, buffer.Length - offset);
                myStream.Write(buffer, offset, count);
            }
        }

        public void ReadWrite(string readPath, string writePath)
        {
            using var readStream = new FileStream(readPath, FileMode.Open, FileAccess.Read, FileShare.Read);
            using var writeStream = new FileStream(writePath, FileMode.Create, FileAccess.Write, FileShare.Write);
            int bytesRead = 0;
            byte[] buffer = new byte[BUFFERSIZE];
            while ((bytesRead = readStream.Read(buffer, 0, BUFFERSIZE)) > 0)
            {
                writeStream.Write(buffer, 0, BUFFERSIZE);
            }
        }
    }
}
