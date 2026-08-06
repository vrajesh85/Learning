
namespace Networking.UnitTests.Mocking
{
    public class MockItemHandler : DelegatingHandler
    {
        private Func<HttpRequestMessage, HttpResponseMessage> _responseGenerator;
        public MockItemHandler(Func<HttpRequestMessage, HttpResponseMessage> responseGenerator)
        {
            _responseGenerator = responseGenerator;
        }

        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
           cancellationToken.ThrowIfCancellationRequested();
           var response = _responseGenerator(request);
           response.RequestMessage = request;
           return Task.FromResult(response);
        }
    }
}
