namespace DI.Middleware
{
    public class CityMiddleware
    {
       // private IGuidService _guidService;
        private RequestDelegate _requestDelegate;
        public CityMiddleware(RequestDelegate requestDelegate) //IGuidService guidService,
        {
           // _guidService = guidService;
            _requestDelegate = requestDelegate;
        }

        public async Task Invoke(HttpContext context, IGuidService guidService)
        {
            if (context.Request.Method == "GET")
            {
                await guidService.Format(context,"CityMiddleware");
            }
            else 
            await _requestDelegate(context);
        }
    }
}
