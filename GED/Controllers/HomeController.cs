using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using GED.Models;
using GED.Services;
using GED.Infrastructure;
using System.IO; // Added for FileStream

namespace GED.Controllers;

[ServiceFilter(typeof(WindowsAuthFilter))]
public class HomeController : Controller
{
    private readonly IPlanService _planService;

    public HomeController(IPlanService planService)
    {
        _planService = planService;
    }

    public async Task<IActionResult> Index(string searchTerm = "", int page = 1)
    {
        const int pageSize = 15;
        var (plans, totalCount) = await _planService.GetPlansAsync(searchTerm, page, pageSize);

        ViewData["TotalCount"] = totalCount;
        ViewData["Page"] = page;
        ViewData["PageSize"] = pageSize;
        ViewData["SearchTerm"] = searchTerm;

        // For AJAX requests, return partial view with ViewData
        if (Request.Headers["X-Requested-With"] == "XMLHttpRequest")
        {
            // Add headers to prevent caching of the partial view
            Response.Headers.Append("Cache-Control", "no-cache, no-store, must-revalidate");
            Response.Headers.Append("Pragma", "no-cache");
            Response.Headers.Append("Expires", "0");
            // Pass ViewData to partial view
            return PartialView("_PlanTable", plans);
        }

        return View(plans);
    }

    // Optional: Separate AJAX endpoint for better separation
    public async Task<IActionResult> SearchPlans(string searchTerm = "", int page = 1)
    {
        const int pageSize = 15;
        var (plans, totalCount) = await _planService.GetPlansAsync(searchTerm, page, pageSize);

        ViewData["TotalCount"] = totalCount;
        ViewData["Page"] = page;
        ViewData["PageSize"] = pageSize;
        ViewData["SearchTerm"] = searchTerm;

        return PartialView("_PlanTable", plans);
    }

    public async Task<IActionResult> Show(int id)
    {
        var viewModel = await _planService.GetPlanDetailsAsync(id);
        if (viewModel == null)
        {
            return NotFound();
        }
        return View(viewModel);
    }

    public IActionResult GetJpegFile(string jpegName, bool download = false)
    {
        if (string.IsNullOrEmpty(jpegName))
        {
            return BadRequest();
        }

        var networkPath = Path.Combine(@"\\139.53.3.112\plansJpeg", jpegName);

        if (!System.IO.File.Exists(networkPath))
        {
            return NotFound();
        }

        var fileStream = new FileStream(networkPath, FileMode.Open, FileAccess.Read);
        
        if (download)
        {
            return File(fileStream, "image/jpeg", jpegName);
        }

        return File(fileStream, "image/jpeg");
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}