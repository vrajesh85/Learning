using DI.Middleware;
using DI.Services;

namespace DI
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.
          //  builder.Services.AddControllersWithViews();

            builder.Services.AddSingleton(typeof(ICollection<>),typeof(List<>));

            builder.Services.AddScoped<ITimeStamper, DefaultTimeStamper>();
            builder.Services.AddScoped<IGuidService, GuidService>();

            builder.Services.Configure<CookiePolicyOptions>(opts =>
            {
                opts.CheckConsentNeeded = context => true;
            });

            builder.Services.AddDistributedMemoryCache();
            builder.Services.AddSession(opts =>
            {
                opts.IdleTimeout = TimeSpan.FromMinutes(30);
                opts.Cookie.IsEssential = true;
            });

            var app = builder.Build();

            app.Logger.LogDebug("Processing started...");

            app.UseCookiePolicy();
            app.UseSession();

            var configuration = builder.Configuration;
            //  app.UseMiddleware<WeatherMiddleware>();
            //app.UseMiddleware<CityMiddleware>();

            app.MapGet("cookie", async context =>
            {
               int counter1 = int.Parse(context.Request.Cookies["counter1"] ?? "0") + 1;
               int counter2 = int.Parse(context.Request.Cookies["counter2"] ?? "0") + 1;

               context.Response.Cookies.Append("counter1", counter1.ToString(), new CookieOptions { MaxAge = TimeSpan.FromMinutes(1), IsEssential = true });
               context.Response.Cookies.Append("counter2", counter2.ToString(), new CookieOptions { MaxAge = TimeSpan.FromMinutes(1)});

               await context.Response.WriteAsync($"Counter 1 {counter1} and Counter 2 {counter2}");
            });

            app.MapGet("clear", context =>
            {
                context.Response.Cookies.Delete("counter1");
                context.Response.Cookies.Delete("counter2");

                return Task.CompletedTask;
            });

            app.MapFallback(async context =>
            {
                await context.Response.WriteAsync("This is fallback middleware");
            });

            //app.MapGet("string", async (HttpContext context, IConfiguration config) =>
            //{
            //    configuration.GetSection("Logging");
            //    string logLevel = config["logging:logLevel:default"];
            //    ICollection<string> collection = context.RequestServices.GetRequiredService<ICollection<string>>();
            //    collection.Add("Rajesh");
            //    foreach(string str in collection)
            //        await context.Response.WriteAsync($"string is {str} and loglevel is {logLevel}");
            //});

            //app.MapGet("int", async context =>
            //{
            //    ICollection<int> collection = context.RequestServices.GetRequiredService<ICollection<int>>();
            //    collection.Add(1);
            //    foreach(int val in collection)
            //        await context.Response.WriteAsync($" int value is {val}");
            //});

            //app.Use(async (context, next) =>
            //{
            //    new WeatherMiddleware(context,next).Invoke(context);
            //    await next();
            //});

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

            app.Run();
        }
    }
}