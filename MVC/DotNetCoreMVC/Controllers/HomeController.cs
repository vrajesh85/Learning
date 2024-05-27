using DotNetCoreMVC.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;

namespace DotNetCoreMVC.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private List<SelectListItem> lstStates = new List<SelectListItem>();
         
        
        private Person[] personData = {
            new Person {PersonId = 1, FirstName = "Adam", LastName = "Freeman",
                Role = Role.Admin},
            new Person {PersonId = 2, FirstName = "Jacqui", LastName = "Griffyth",
                Role = Role.User},
            new Person {PersonId = 3, FirstName = "John", LastName = "Smith",
                Role = Role.User},
            new Person {PersonId = 4, FirstName = "Anne", LastName = "Jones",
                Role = Role.Guest}
        };

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index(int id = 1)
        {
            Person dataItem = personData.Where(p => p.PersonId == id).First();
            dataItem.Country = GetCountry();
            return View("Index",dataItem);
        }

        [HttpPost]
        public IActionResult Index(Person values)
        {
            return RedirectToAction("Index");
        }

        public IActionResult Privacy(string name="Rajesh")
        {
            // return RedirectToAction("Index");
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }


        private List<SelectListItem> GetStates(string country)
        {
            var lstStates = new List<SelectListItem>();

            if(country == "US")
            {
                lstStates.Add(new SelectListItem("TG", "1"));
                lstStates.Add(new SelectListItem("AP", "2"));
                lstStates.Add(new SelectListItem("TN", "3"));
            }
            else
            {
                lstStates.Add(new SelectListItem("TX", "4"));
                lstStates.Add(new SelectListItem("AZ", "5"));
            }

            return lstStates;
        }

        private List<SelectListItem> GetCountry()
        {
            var lstCountries = new List<SelectListItem>();

            lstCountries.Add(new SelectListItem("IN", "1"));
            lstCountries.Add(new SelectListItem("US", "2"));

            return lstCountries;
        }
    }
}
