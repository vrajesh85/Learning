namespace DotNet6.Middleware
{
    public class WeatherEndPoint
    {
        public async Task Endpoint(HttpContext context)
        {
            IResponseFormatter formatter = context.RequestServices.GetRequiredService<IResponseFormatter>();
            await context.Response.WriteAsync(formatter.Format("This is coming from Weather Endpoint"));
        }
    }
}
