using Microsoft.AspNetCore.Mvc;
using Networking.Helpers;
using System.Net;

namespace Networking.Controllers.ClientFactory
{
    [ApiController]
    [Route("[controller]")]
    public class CRUDController : ControllerBase
    {
        private IHttpClientFactory _httpClientFactory;
        private MyAPITypeClient _typeClient;
        private const string BASEADDRESS = "https://api.restful-api.dev/";
        public CRUDController(IHttpClientFactory httpClientFactory, MyAPITypeClient typeClient)
        {
            _httpClientFactory = httpClientFactory;
            _typeClient = typeClient;
        }

        [HttpGet("SimpleGetPath", Name = "SimpleGet")]
        public async Task<IActionResult> SimpleGet()
        {
            foreach (IPAddress a in Dns.GetHostAddresses("google.co.in"))
                Console.WriteLine(a.ToString());

            var httpClient = _httpClientFactory.CreateClient();
            httpClient.BaseAddress = new Uri(BASEADDRESS);
            var result = await httpClient.GetAsync("objects");
            var content = await result.Content.ReadFromJsonAsync<object>();
            return Ok(content);
        }

        [HttpGet("NamedClientGetPath", Name = "NamedClientGet")]
        public async Task<IActionResult> GetNamedClient()
        {
            var httpClient = _httpClientFactory.CreateClient("SingleObject");
            var result = await httpClient.GetFromJsonAsync<object>("objects/7");
            return Ok(result);
        }

        [HttpGet("TypeClientGetPath", Name = "TypeClientGet")]
        public async Task<IActionResult> GetTypedClient()
        {
            var result = await _typeClient.GetJsonAsync("collections");
            return Ok(result);
        }

        [HttpGet("GetAllPath", Name = "GetAll")]
        public IActionResult GetAllValues()
        {
            return RedirectToRoute("SimpleGet", null);
        }

        #region Authenticated
        [HttpGet("GetCollectionsPath", Name = "GetCollections")]
        public async Task<IActionResult> GetCollections()
        {
            var httpClient = _httpClientFactory.CreateClient("CollectionsObject");
            var result = await httpClient.GetFromJsonAsync<object>("collections");
            return Ok(result);
        }

        [HttpPost("PostCollectionsPath", Name = "PostCollections")]
        public async Task<IActionResult> PostCollections(string collectionName)
        {
            var httpClient = _httpClientFactory.CreateClient("CollectionsObject");
            HttpRequestMessage request = new HttpRequestMessage();
            request.Method = HttpMethod.Post;
            request.Content = JsonContent.Create(new
            {
                collectionName = collectionName,
                objectCount = new Random().Next(100)
            });
            request.RequestUri = new Uri("/collections/Phone/objects", UriKind.Relative);
            var result = await httpClient.SendAsync(request);
            return Ok(result);
        }

        #endregion

         
    }
}
