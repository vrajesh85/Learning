using Networking.Helpers;
namespace Networking
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.

            builder.Services.AddControllers();
            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();
            builder.Services.AddHttpClient();
            builder.Services.AddTransient<CustomMessageHandler>();
            builder.Services.AddTransient<MyAPITypeClient>();
            builder.Services.AddHttpClient("SingleObject", request =>
            {
                request.BaseAddress = new Uri("https://api.restful-api.dev/");
            });

            builder.Services.AddHttpClient("CollectionsObject", request =>
            {
                request.BaseAddress = new Uri("https://api.restful-api.dev/");
            }).AddHttpMessageHandler<CustomMessageHandler>();

            builder.Services.AddHttpClient<MyAPITypeClient>(request =>
            {
                request.BaseAddress = new Uri("https://api.restful-api.dev/");
            }).AddHttpMessageHandler<CustomMessageHandler>();

            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI();
            }

            app.UseHttpsRedirection();

            app.UseAuthorization();


            app.MapControllers();

            app.Run();
        }
    }
}
