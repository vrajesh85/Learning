namespace DotNet6.Middleware
{
    public class GuidService : IResponseFormatter
    {
        private Guid _guid = Guid.NewGuid();
        private int counter = 0;

        public string Format(string text)
        {
            return $"{text} is with ' {_guid} and with count as {++counter} '";
        }
    }
}
