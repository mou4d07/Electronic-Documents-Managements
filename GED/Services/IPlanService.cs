using GED.Models.Data;
using GED.Models.ViewModels;

namespace GED.Services;

public interface IPlanService
{
    Task<(IEnumerable<PlanViewModel> plans, int totalCount)> GetPlansAsync(string searchTerm, int page, int pageSize);
    Task<ShowViewModel?> GetPlanDetailsAsync(int id);
}
