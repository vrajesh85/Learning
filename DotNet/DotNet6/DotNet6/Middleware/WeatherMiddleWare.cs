namespace DotNet6.Middleware
{
    public class WeatherMiddleWare
    {
        private RequestDelegate _next;

        public WeatherMiddleWare(RequestDelegate requestDelegate)
        {
            _next = requestDelegate;
        }

        public async Task Invoke(HttpContext context)
        {
            await context.Response.WriteAsync($"This is from weather middleware component");
            await _next(context);
        }
    }
}
