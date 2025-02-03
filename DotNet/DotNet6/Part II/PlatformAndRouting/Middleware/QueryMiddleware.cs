using System.ComponentModel.DataAnnotations;

namespace PlatformAndRouting.Middleware
{
    public class QueryMiddleware
    {
        private readonly RequestDelegate _requestDelegate;
      //  public QueryMiddleware() { }
        public QueryMiddleware(RequestDelegate next)
        {
            _requestDelegate = next;
        }

        public async Task Invoke(HttpContext context)
        {
            if (context.Request.Method == "GET")
            {
                //context.Response.ContentType = "text/plain";
                await context.Response.WriteAsync("Query Middlware \n");
            }
           await _requestDelegate(context);
        }
    }
}
