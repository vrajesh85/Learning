namespace DotNet6.Middleware
{
    public class City
    {
        public static async Task EndPoint(HttpContext context)
        {
            //context.Response.Redirect($"/branch");

            LinkGenerator? generator = context.RequestServices.GetService<LinkGenerator>();
            string? url = generator?.GetPathByRouteValues(context, "default", null);

            context.Response.Redirect(url);

            await context.Response.WriteAsync("This will not be written");
        }
    }
}
