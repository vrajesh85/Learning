namespace PlatformAndRouting.Middleware
{
    public class GuidService : IGuidService
    {
        private Guid guid = Guid.NewGuid();
        public string GetGuid() => guid.ToString();

        public async Task Format(HttpContext context) => await context.Response.WriteAsync($"The guid value is {guid.ToString()}");
    }
}
