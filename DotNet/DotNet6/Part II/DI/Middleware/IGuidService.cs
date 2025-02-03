namespace DI.Middleware
{
    public interface IGuidService
    {
        Task Format(HttpContext context,string content);
    }
}
