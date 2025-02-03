using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using MVCApp.Models;

namespace MVCApp.Controllers
{
    //  [Route("api/[controller]")]
   // [ApiController]
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly PersonRepository _personRepository;

        public HomeController(ILogger<HomeController> logger, PersonRepository repository)
        {
            _logger = logger;
            _personRepository = repository;
        }

        public IActionResult Index()
        {
            return View();
        }

        [HttpGet("{id:int}")]
        public IActionResult GetId(string id)
        {
            return View("Index");
        }

        [HttpGet("Person")]
        public IActionResult GetPerson() => Ok(_personRepository.GetAll());

        [HttpPost("AddPerson")]
        public IActionResult AddPerson([FromBody]Person person)
        {
            if (ModelState.IsValid)
            {
                _personRepository.Add(person);
            }
            else return BadRequest(ModelState);

            return Ok();
        }

        public IActionResult GetResult(bool id)
        {
            return Ok(id);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
