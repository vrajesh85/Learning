namespace DotNet6.Middleware
{
    public class BranchMiddleWare
    {
        private RequestDelegate _next;

        public BranchMiddleWare(RequestDelegate requestDelegate)
        {
            _next = requestDelegate;
        }

        public async Task Invoke(HttpContext context)
        {          
            context.Response.ContentType = "text/plain";
            await context.Response.WriteAsync("This is from branch middleware class");
        }
    }
}
