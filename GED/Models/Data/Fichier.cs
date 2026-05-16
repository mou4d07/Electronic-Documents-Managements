using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GED.Models.Data;

[Table("fichier", Schema = "webeda3acier")]
public class Fichier
{
    [Key]
    [Column("id")]
    public int Id { get; set; }

    [Column("fichier")]
    public string? FileName { get; set; }

    [Column("chemin")]
    public string? Path { get; set; }

    [Column("xref")]
    public int? Xref { get; set; }

    [Column("indice")]
    public int? Indice { get; set; }

    public Plan? Plan { get; set; }
}
