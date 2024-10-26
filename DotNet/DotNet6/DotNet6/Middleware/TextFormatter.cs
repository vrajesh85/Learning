namespace DotNet6.Middleware
{
    public class TextFormatter : IResponseFormatter
    {
        private int counter = 0;
        private static TextFormatter _sharedObj;

        public string Format(string text)
        {
            return $"Formatted text --> {text} with counter value as {++this.counter}";
        }

        public static TextFormatter Singleton()
        {
            if (_sharedObj == null)
                _sharedObj = new TextFormatter();
            return _sharedObj;
        }
    }

    public interface IResponseFormatter
    {
        string Format(string text);
    }
}
