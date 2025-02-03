using System.ComponentModel.DataAnnotations;

namespace MVCApp.Models
{
    public class Person
    {
        [Required]
        public string Name { get; set; }
        [Range(0,100)]
        public int Age { get; set; }
        public string Address { get; set; }
        public string City { get; set; }
        public bool IsMarried { get; set; }
    }
}
