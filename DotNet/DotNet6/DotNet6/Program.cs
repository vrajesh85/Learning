using DotNet6.Middleware;
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<MessageOptions>(options => {
    options.Name = "Rajesh";
    options.Age = 40;
});

//builder.Services.AddSingleton<IResponseFormatter , GuidService>();

builder.Services.AddTransient<IResponseFormatter , GuidService>();

var app = builder.Build();

//app.UseRouting();

app.UseMiddleware<TestingDIMiddleWareOne>();
app.UseMiddleware<TestingDIMiddleWareTwo>();

//IResponseFormatter formatter = new TextFormatter();

//app.UseEndpoints(endpoints =>
//{
//    endpoints.MapGet("routing", async (context) =>
//    {
//        await context.Response.WriteAsync("You are getting this response from endpoint");
//    });

//    endpoints.MapGet("city", City.EndPoint);
//    endpoints.MapGet("middleware/function", async (HttpContext context , IResponseFormatter formatter) =>
//    {
//        await context.Response.WriteAsync(formatter.Format("Sample text to format"));
//    });

//    endpoints.MapGet("middleware/singleton", async (context) =>
//    {
//        IResponseFormatter formatter2 = TextFormatter.Singleton();
//        await context.Response.WriteAsync(formatter2.Format("Sample text to format"));
//    });

//    endpoints.MapGet("{first}/{second}/{third}", async context =>
//    {
//        await context.Response.WriteAsync("This is from URL placeholder");
//        foreach (var val in context.Request.RouteValues)
//            await context.Response.WriteAsync($"The route value is  {val.ToString()} \n");
//    });

//    endpoints.MapGet("/", async (HttpContext context, IOptions<MessageOptions> options) =>
//    {
//        MessageOptions opts = options.Value;
//        await context.Response.WriteAsync($"Hello World! \n , My name is {opts.Name} and my age is {opts.Age}");
//    }).WithMetadata(new RouteNameMetadata("default"));
//});

//app.Map("/branch", branch =>
//{
//    branch.UseMiddleware<BranchMiddleWare>();

//    branch.Use(async (HttpContext context, Func<Task> next) =>
//    {
//        context.Response.ContentType = "text/plain";
//        await context.Response.WriteAsync("This is from branch of map");
//    });
//});


//app.Use(async (context, next) => {
//    await next();
//    await context.Response.WriteAsync($" the status code is {context.Response.StatusCode}");
//});

//app.Use(async (context, next) => {
//    if (context.Request.Method == "GET" && context.Request.Query["custom"] == "true") {
//        // prevents subsequent middleware from assigning status code and status headers
//       context.Response.ContentType = "text/plain";
//       await context.Response.WriteAsync("This is custom middleware \n");
//    }       
//    await next();
//});

//app.UseMiddleware<QueryStringMiddleWare>();

app.Run();

