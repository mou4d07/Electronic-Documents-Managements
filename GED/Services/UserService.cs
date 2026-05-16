using GED.Data;
using Microsoft.EntityFrameworkCore;

namespace GED.Services;

public class UserService : IUserService
{
    private readonly GedDbContext _context;

    public UserService(GedDbContext context)
    {
        _context = context;
    }

    public async Task<bool> IsUserAuthorized(string userName)
    {
        if (string.IsNullOrEmpty(userName))
        {
            return false;
        }

        // The username in Windows might be in the format DOMAIN\user, so we take the user part.
        var userOnly = userName.Contains("\\") ? userName.Split('\\')[1] : userName;
        return await _context.groupe_utilisateur
                        .AnyAsync(u => u.Utilisateur != null &&
                                  u.Utilisateur.ToLower() == userOnly.ToLower()); ;
    }
}
