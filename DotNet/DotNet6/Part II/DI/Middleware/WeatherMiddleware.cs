namespace DI.Middleware
{
    public class WeatherMiddleware
    {
      //  private IGuidService _guidService;
    //    private IGuidService _guidService2;
        private RequestDelegate _requestDelegate;
        private ILogger<WeatherMiddleware> _logger;

        public WeatherMiddleware(RequestDelegate requestDelegate, ILogger<WeatherMiddleware> logger)  //, IGuidService guidService2,
        {
            //_guidService = guidService;
        //    _guidService2 = guidService2;
            _requestDelegate = requestDelegate;
            _logger = logger;
        }

        public async Task Invoke(HttpContext context, IGuidService guidService)
        {
            if (context.Request.Method == "GET")
            {
                _logger.LogDebug($"We are inside the GET call");
                await guidService.Format(context,"WeatherMiddleware");
              //  await _guidService2.Format(context, "WeatherMiddleware");
            }
           // else
            await _requestDelegate(context);
        }
    }
}
