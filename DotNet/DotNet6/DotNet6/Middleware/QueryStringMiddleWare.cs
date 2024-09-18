namespace DotNet6.Middleware
{
    public class QueryStringMiddleWare
    {
        private RequestDelegate next;

        public QueryStringMiddleWare(RequestDelegate requestDelegate)
        {
            next = requestDelegate;
        }

        public async Task Invoke(HttpContext context)
        {
            if (context.Request.Method == HttpMethods.Get && context.Request.Query["custom"] == "true")
            {
                if (!context.Response.HasStarted)
                {
                    context.Response.ContentType = "text/plain";
                }
                await context.Response.WriteAsync("Custom Middleware from class \n");
            }
            await next(context);
        }
    }
}
