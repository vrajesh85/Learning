namespace DotNet6.Middleware
{
   public class QueryStringMiddleWare
    {
        private RequestDelegate _next;

        public QueryStringMiddleWare(RequestDelegate requestDelegate)
        {
            _next = requestDelegate;
        }


        public async Task Invoke(HttpContext context)
        {
            if(context.Request.Method == "GET" && context.Request.Query["custom"] == "true")
            {
               // context.Response.ContentType = "text/plain";
                await context.Response.WriteAsync("This is from custom middleware component class \n");                
            }
            await _next(context);
        }
    }
}
