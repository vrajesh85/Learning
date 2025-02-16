using System;
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

        public IActionResult Cubed() => View();

        public IActionResult Cube(double num)
        {
            TempData["Value"] = num.ToString();
            TempData["result"] = Math.Pow(num, 3).ToString();
           
            return RedirectToAction(nameof(Cubed));
        }

        [HttpGet("{id:int}")]
        public IActionResult GetId(string id)
        {
            ViewBag.Title = "Id";
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

            //return View("ViewPerson", person);
            return RedirectToAction("DisplayPerson",new { person });
        }

        public IActionResult DisplayPerson(Person person) =>                   
             View("ViewPerson", person?.Name == null ? new Person { Age = 39, Name = "Default", Address = "Not Available"} : null);
        
       
        public IActionResult GetResult(bool id)
        {
            return Ok(id);
        }

        public IActionResult Html() => View("ViewHtml", (object)"<h3> This is a <b> string </b> </h3>");

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
