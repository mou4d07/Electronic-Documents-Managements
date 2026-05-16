using GED.Models.ViewModels;
using GED.Models.Data;
using Microsoft.EntityFrameworkCore;
using GED.Data;

namespace GED.Services;

public class PlanService : IPlanService
{
    private readonly GedDbContext _context;

    public PlanService(GedDbContext context)
    {
        _context = context;
    }

    public async Task<(IEnumerable<PlanViewModel> plans, int totalCount)> GetPlansAsync(string searchTerm, int page, int pageSize)
    {
        var query = from f in _context.fichier
                    join p in _context.plan on f.Id equals p.Id into planGroup
                    from p in planGroup.DefaultIfEmpty()
                    select new { Fichier = f, Plan = p };

        if (!string.IsNullOrEmpty(searchTerm))
        {
            query = query.Where(x =>
                (x.Fichier.FileName != null && x.Fichier.FileName.Contains(searchTerm)) ||
                (x.Plan != null && x.Plan.Designation != null && x.Plan.Designation.Contains(searchTerm))
            );
        }

        var totalCount = await query.CountAsync();

        var plans = await query
            .OrderBy(x => x.Fichier.FileName)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(x => new PlanViewModel
            {
                Id = x.Fichier.Id,
                FileName = x.Fichier.FileName,
                Designation = x.Plan != null ? x.Plan.Designation : "N/A"
            })
            .ToListAsync();

        return (plans, totalCount);
    }

    public async Task<ShowViewModel?> GetPlanDetailsAsync(int id)
    {
        var fichier = await _context.fichier
        .Include(f => f.Plan)
        .FirstOrDefaultAsync(f => f.Id == id);

        if (fichier == null)
            return null;

        return new ShowViewModel
        {
            Fichier = fichier,
            Plan = fichier.Plan
        };
    }
}
