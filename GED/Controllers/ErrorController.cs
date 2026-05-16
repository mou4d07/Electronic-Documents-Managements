using Microsoft.AspNetCore.Mvc;

namespace GED.Controllers;

public class ErrorController : Controller
{
    [HttpGet("/Error/AccessDenied")]
    public IActionResult AccessDenied()
    {
        return View();
    }
}
