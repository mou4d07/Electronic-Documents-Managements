namespace GED.Services;

public interface IUserService
{
    Task<bool> IsUserAuthorized(string userName);
}
