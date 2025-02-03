namespace PlatformAndRouting.Middleware
{
    public class TextFormatter : IResponseFormatter
    {
        private int counter = 0;
        public async Task Format(HttpContext context, string content) => await context.Response.WriteAsync($"The format is {content} and counter is {++counter}");

        private static TextFormatter _shared;

        public static TextFormatter SingleTon()
        {
            if (_shared == null)
                _shared = new TextFormatter();
            return _shared;
        }
    }
}
