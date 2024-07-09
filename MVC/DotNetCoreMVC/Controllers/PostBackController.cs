using DotNetCoreMVC.Models;
using Microsoft.AspNetCore.Mvc;

namespace DotNetCoreMVC.Controllers
{
    public class PostBackController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public string PostRequest()
        {
            return "Success";
        }
    }
}
