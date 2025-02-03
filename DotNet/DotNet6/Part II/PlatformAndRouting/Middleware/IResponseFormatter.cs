namespace PlatformAndRouting.Middleware
{
    public interface IResponseFormatter
    {
        Task Format(HttpContext context, string content);
    }
}
