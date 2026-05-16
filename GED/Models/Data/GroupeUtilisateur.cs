using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GED.Models.Data;

[Table("groupe_utilisateur", Schema = "webeda3acier")]
public class GroupeUtilisateur
{
    [Key]
    [Column("id")]
    public int Id { get; set; }

    [Column("groupe")]
    public string? Groupe { get; set; }

    [Column("utilisateur")]
    public string? Utilisateur { get; set; }
}
