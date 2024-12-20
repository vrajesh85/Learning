using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;

namespace PracticeApp.Networking
{
    public class SampleAPI
    {
     //   private IHttpClientFactory _factory;

        // private HttpClient _client;

        public async Task<TodoItem?> GetTodoIitemsWithClient()  
        {
              using var _client = new HttpClient();          
              _client.BaseAddress = new Uri("https://jsonplaceholder.typicode.com");
              _client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
              _client.Timeout = TimeSpan.FromSeconds(10);
              var response = await _client.GetAsync("/todos/1");//.ConfigureAwait(false);
              response.EnsureSuccessStatusCode();
              TodoItem todoItem = await response.Content?.ReadFromJsonAsync<TodoItem>();
              return todoItem;                    
        }

        public async Task PostDummyRestApiExample()
        {
            var api = "https://api.restful-api.dev/objects";

            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, api);
            request.Content = new StringContent(JsonSerializer.Serialize<Item>(CreateItem()), Encoding.UTF8, "application/json");
            using var client = new HttpClient();
            client.DefaultRequestHeaders.Add("name", "value");
            var response = await client.SendAsync(request);
            response.EnsureSuccessStatusCode();
        }


        public async Task PostDummyRestApiExampleWithHandler()
        {
            var _api = "https://api.restful-api.dev/objects";

            var _handler = new HttpClientHandler();
           
            var _client = new HttpClient(_handler);

            var request = new HttpRequestMessage(HttpMethod.Post, _api);

            await _client.SendAsync(request);
        }
       
        public async Task<TodoItem> GetTodoItemsWithHandler()
        {
            using var handler = new LoggingHandler(new HttpClientHandler());
            using var client = new HttpClient(handler);
           
            var response = await client.GetAsync("https://jsonplaceholder.typicode.com/todos/1");
            response.EnsureSuccessStatusCode();

            TodoItem todo = await response.Content?.ReadFromJsonAsync<TodoItem>();
            return todo;
        }

        private Item CreateItem() => new Item 
                                     {
                                              Name = "Laptop", 
                                              Data = new Data 
                                              {
                                                 Model = "Intel Core",
                                                 Price = 1000M,
                                                 Year = 2019,
                                                 Size = "Large"
                                              }                
                                     };
         }

    public class TodoItem
    {
        public string Title { get; set; }
        public int UserId { get; set; }
        public int Id { get; set; }
        public bool IsCompleted { get; set; }
    }

    public class Item
    {
        public string Name { get; set; }
        public Data? Data {get; set; }
    }

    public class Data
    {
        public int Year { get; set; } 
        public decimal Price { get; set; }
        public string Model { get; set; }
        public string Size { get; set; }
    }
}
