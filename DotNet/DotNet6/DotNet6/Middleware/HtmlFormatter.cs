namespace DotNet6.Middleware
{
    public class HtmlFormatter : IResponseFormatter
    {
        private int counter = 0;
       public string Format(string text)
        {
            return $"The value of counter is {++counter}";
        }
    }
}
