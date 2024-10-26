using Microsoft.AspNetCore.Http;

namespace DotNet6.Middleware
{
    public class TestingDIMiddleWareOne
    {
        private IResponseFormatter _responseFormatter;
        private RequestDelegate _requestDelegate;

        public TestingDIMiddleWareOne(RequestDelegate requestDelegate , IResponseFormatter formatter)
        {
            _requestDelegate = requestDelegate;
            _responseFormatter = formatter;
        }

        public async Task Invoke(HttpContext context)
        {
            if (context.Request.Path == "/testing")
            await context.Response.WriteAsync(_responseFormatter.Format("testing DI middleware one"));
            await _requestDelegate(context);
        }
    }

    public class TestingDIMiddleWareTwo
    {
        private IResponseFormatter _responseFormatter;
        private RequestDelegate _requestDelegate;

        public TestingDIMiddleWareTwo(RequestDelegate requestDelegate, IResponseFormatter formatter)
        {
            _requestDelegate = requestDelegate;
            _responseFormatter = formatter;
        }

        public async Task Invoke(HttpContext context)
        {
            if (context.Request.Path == "/sample")
                await context.Response.WriteAsync(_responseFormatter.Format("testing DI middleware two"));
            // await _requestDelegate(context);
        }
    }
}
