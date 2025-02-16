using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace RazorPages.Pages
{
    public class SupplierModel : PageModel
    {
        private ILogger<SupplierModel> _logger;
        public SupplierModel(ILogger<SupplierModel> logger)
        {
            _logger = logger;
        }
        public IActionResult OnGet()
        {
            return Page();
            //return RedirectToPage("Privacy");
        }

       
    }
}
