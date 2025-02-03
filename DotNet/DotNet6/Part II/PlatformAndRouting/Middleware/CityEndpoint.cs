using Microsoft.Extensions.DependencyInjection;
namespace PlatformAndRouting.Middleware

{
    public class CityEndpoint
    {
        public static async Task Endpoint(IEndpointRouteBuilder app,HttpContext context)  {
           var formatter = app.ServiceProvider.GetRequiredService<IGuidService>();
            var guid = formatter.GetGuid();
            await context.Response.WriteAsync($"The guid value is {guid}");
    }
    }
}
