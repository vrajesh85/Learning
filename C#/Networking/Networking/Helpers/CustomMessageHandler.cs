namespace Networking.Helpers
{
    public class CustomMessageHandler : DelegatingHandler
    {
        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            request.Headers.Add("x-api-key", "0cc8bc57-111a-470d-bb17-0f5f281c7182");
            return await base.SendAsync(request, cancellationToken);
        }
    }
}
