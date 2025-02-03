using System.Net.Mime;
using DI.Services;

namespace DI.Middleware
{
    public class GuidService : IGuidService
    {
        private ITimeStamper _timeStamper;
        private Guid _guid = Guid.NewGuid();
        public GuidService(ITimeStamper timeStamper)
        {
            _timeStamper = timeStamper;
        }
        public async Task Format(HttpContext context, string content) =>
            await context.Response.WriteAsync($"The time now is {_timeStamper.TimeStamp} and it is {content} and the guid value is {_guid.ToString()} \n");
    }
}
