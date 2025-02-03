using System.Runtime.CompilerServices;

namespace PlatformAndRouting.Middleware
{
    public class WeatherEndpoint
    {
        public static async Task EndPoint(HttpContext context,IResponseFormatter formatter, string content) => await formatter.Format(context, content);
    }
}
