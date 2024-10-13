using DotNet6.Middleware;
using Microsoft.Extensions.Options;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<MessageOptions>(options => {
    options.Name = "Rajesh";
    options.Age = 40;
});


var app = builder.Build();

app.Map("/branch", branch => {
    branch.UseMiddleware<BranchMiddleWare>();

    branch.Use(async (HttpContext context, Func<Task> next) =>
    {
        context.Response.ContentType = "text/plain";
        await context.Response.WriteAsync("This is from branch of map");
    });
});


app.Use(async (context, next) => {
    await next();
    await context.Response.WriteAsync($" the status code is {context.Response.StatusCode}");
});

app.Use(async (context, next) => {
    if (context.Request.Method == "GET" && context.Request.Query["custom"] == "true") {
        // prevents subsequent middleware from assigning status code and status headers
       context.Response.ContentType = "text/plain";
       await context.Response.WriteAsync("This is custom middleware \n");
    }       
    await next();
});

app.UseMiddleware<QueryStringMiddleWare>();

app.MapGet("/", async (HttpContext context, IOptions<MessageOptions> options) =>
{
    MessageOptions opts = options.Value;
    await context.Response.WriteAsync($"Hello World! \n , My name is {opts.Name} and my age is {opts.Age}");
});

app.Run(); 
