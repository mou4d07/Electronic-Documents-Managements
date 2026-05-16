using GED.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

namespace GED.Infrastructure;

public class WindowsAuthFilter : IAsyncActionFilter
{
    private readonly IUserService _userService;
    private readonly ILogger<WindowsAuthFilter> _logger;

    public WindowsAuthFilter(IUserService userService, ILogger<WindowsAuthFilter> logger)
    {
        _userService = userService;
        _logger = logger;
    }

    public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
    {
        var userName = context.HttpContext.User.Identity?.Name;
        _logger.LogInformation("Checking authorization for user: {UserName}", userName);

        if (!await _userService.IsUserAuthorized(userName!))
        {
            _logger.LogWarning("Unauthorized user access attempt: {UserName}", userName);
            context.Result = new RedirectToActionResult("AccessDenied", "Error", null);
            return;
        }

        _logger.LogInformation("User {UserName} is authorized.", userName);
        await next();
    }
}
