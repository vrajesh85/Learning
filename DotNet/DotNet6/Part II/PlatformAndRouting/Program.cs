using Microsoft.Extensions.Options;
using PlatformAndRouting.Middleware;

namespace PlatformAndRouting
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            string result = string.Empty;

            // Add services to the container.
            // builder.Services.AddControllersWithViews();

            builder.Services.Configure<MessageOptions>(options =>
            {
                options.Name = "Rajesh";
            });

            builder.Services.AddSingleton<IResponseFormatter, HTMLFormatter>();

            builder.Services.AddSingleton<IResponseFormatter, TextFormatter>();

            builder.Services.AddTransient<IGuidService, GuidService>();

            var app = builder.Build();

            #region Middleware

            // Configure the HTTP request pipeline.
            //if (!app.Environment.IsDevelopment())
            //{
            //    app.UseExceptionHandler("/Home/Error");
            //}
            //app.UseStaticFiles();

            //app.UseRouting();

            //app.UseAuthorization();

            //app.MapControllerRoute(
            //    name: "default",
            //    pattern: "{controller=Home}/{action=Index}/{id?}");


            // app.Run(new QueryMiddleware().Invoke);

            // app.Use(async (context, next) => {
            //     if (context.Request.Method == HttpMethods.Get)
            //     {
            //         await next();
            //         result += "First Middleware \n";
            //       //  context.Response.ContentType = "text/plain";
            //         await context.Response.WriteAsync(result);
            //     }
            // });

            // app.Use(async (context,next) => {
            //     if (context.Request.Method == HttpMethods.Get)
            //     {
            //         result += "second Middleware \n";
            //         await next();
            //     }
            // });

            //// app.UseMiddleware<QueryMiddleware>();

            //  app.MapGet("/", async (HttpContext context, IOptions<MessageOptions> opts) => {
            //      context.Response.ContentType = "text/plain";
            //      await context.Response.WriteAsync($"my name is {opts.Value.Name}\n");
            // });

            #endregion

         //   app.UseMiddleware<WeatherMiddleware>();

            app.UseRouting();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapGet("middleware/function", async (HttpContext context, IResponseFormatter formatter, IGuidService guidService) =>
                {
                    string guid1 = guidService.GetGuid(); string guid2 = guidService.GetGuid();
                    await formatter.Format(context, $"from middleware with guid 1 {guid1} and guid 2 {guid2}");
                });
                endpoints.MapGet("middleware/endpoint", async (HttpContext context, IResponseFormatter formatter, IGuidService guidService) =>
                {
                    string guid = guidService.GetGuid();
                    await WeatherEndpoint.EndPoint(context, formatter, $"from end point with guid {guid}");
                });
                endpoints.MapGet("city",  async (HttpContext context) =>
                {
                    await CityEndpoint.Endpoint(endpoints, context);
                });
                endpoints.MapGet("village", async (HttpContext context, IGuidService formatter) =>
                {
                    await formatter.Format(context);
                });
            });

            //app.Run(async (context) =>
            //{
            //    context.Response.ContentType = "text/plain";
            //    await context.Response.WriteAsync("Empty\n");
            //});

            //app.Use(async (context, next) =>
            //{
            //    result += "Second Middleware \n";
            //    await next();
            //});

            //app.Use(async (context, next) =>
            //{
            //    result += "Third Middleware \n";

            //    await next();
            //});

            app.Run();
        }
    }
}