namespace PlatformAndRouting.Middleware
{
    public interface IGuidService
    {
        string GetGuid();
        Task Format(HttpContext context);
    }
}
