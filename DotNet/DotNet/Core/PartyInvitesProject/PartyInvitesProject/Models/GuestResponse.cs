using System.ComponentModel.DataAnnotations;
namespace PartyInvitesProject.Models
{
    public class GuestResponse
    {
        [Required(ErrorMessage = "Please enter your name")]
        public string? Name { get; set; }
        [Required(ErrorMessage = "Please enter your email")]
        public string? Email { get; set; }
        [Required(ErrorMessage = "Please enter your phone number")]
        public long? Phone { get; set; }
        [Required(ErrorMessage = "Please say if you can attend or not")]
        public bool? WillAttend { get; set; }
    }
}
