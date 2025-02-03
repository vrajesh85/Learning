namespace PlatformAndRouting.Middleware
{
    public class WeatherMiddleware
    {
        private IGuidService _guidService;
        private RequestDelegate _requestDelegate;
        public WeatherMiddleware(IGuidService guidService, RequestDelegate requestDelegate)
        {
            _guidService = guidService;
            _requestDelegate = requestDelegate;
        }

        public async Task Invoke(HttpContext context)
        {
            if (context.Request.Method == HttpMethod.Get.ToString())
            {
                await _guidService.Format(context);
            }
            else
            {
                await _requestDelegate.Invoke(context);
            }
        }
    }
}
