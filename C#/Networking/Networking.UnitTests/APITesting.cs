using Networking.UnitTests.Mocking;
using System.Net;

namespace Networking.UnitTests
{
    [TestClass]
    public sealed class APITesting
    {
        [TestMethod]
        public async Task GivenObject_Should_Return_Data()
        {
            var httpClient = new HttpClient(CreateMocker());
        }


        private MockItemHandler CreateMocker() => new MockItemHandler(request => new HttpResponseMessage(HttpStatusCode.OK)
                                                  {
                                                      Content = new StringContent($"Request entered with URI {request.RequestUri}")
                                                  });
    }
}
