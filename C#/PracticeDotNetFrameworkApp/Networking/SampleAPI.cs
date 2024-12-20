using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace PracticeApp.Networking
{
    public class SampleAPI
    {
        private IHttpClientFactory _factory;

       // private HttpClient _client;

        public async Task GetTodoIitemsWithClient()
        {
            try
            {
                using (var _client = new HttpClient())
                {
                    _client.BaseAddress = new Uri("https://jsonplaceholder.typicode.com");

                    _client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                    _client.Timeout = TimeSpan.FromSeconds(10);

                    var response = await _client.GetAsync("/todos/1").ConfigureAwait(false);

                    response.EnsureSuccessStatusCode();

                    string html = await response.Content.ReadAsStringAsync();
                }
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine($"Request error: {ex.Message}");
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }
    }

    public class TodoItem
    {
        public string Title { get; set;}
        public int UserId { get; set; }
        public int Id { get; set; }
        public bool IsCompleted { get; set; }
    }
}
