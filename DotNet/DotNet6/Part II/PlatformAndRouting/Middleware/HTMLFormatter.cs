namespace PlatformAndRouting.Middleware
{
    public class HTMLFormatter : IResponseFormatter
    {
        public async Task Format(HttpContext context, string content)
        {
            await context.Response.WriteAsync($@"
              <!DOCTYPE html>
               <head>
                    <title> My Page </title>
               </head>
               <body>
                    <p style = 'background-color:blue'>
                        {content}
                    </p>
                </body>
             </html>");
        }
    }
}
