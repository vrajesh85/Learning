using Microsoft.AspNetCore.Mvc;

namespace Networking.Helpers
{
    public class MyAPITypeClient
    {
        private readonly HttpClient _httpClient;
        public MyAPITypeClient(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<object?> GetJsonAsync(string route)
        {
           return await _httpClient.GetFromJsonAsync<object>(route);
        }
    }
}
