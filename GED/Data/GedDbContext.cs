using GED.Models.Data;
using Microsoft.EntityFrameworkCore;

namespace GED.Data;

public class GedDbContext : DbContext
{
    public GedDbContext(DbContextOptions<GedDbContext> options) : base(options)
    {
    }

    public DbSet<Fichier> fichier { get; set; }
    public DbSet<Plan> plan { get; set; }
    public DbSet<GroupeUtilisateur> groupe_utilisateur { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Fichier>()
            .HasOne(f => f.Plan)
            .WithOne(p => p.Fichier)
            .HasForeignKey<Plan>(p => p.Id);

        base.OnModelCreating(modelBuilder);
    }
}
