using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GED.Models.Data;

[Table("plan", Schema = "webeda3acier")]
public class Plan
{
    [Key]
    [Column("id")]
    public int Id { get; set; }

    [Column("est_marque")]
    public short? IsMarked { get; set; }

    [Column("DESIGNATION")]
    public string? Designation { get; set; }

    [Column("SOUS_TITRE")]
    public string? Subtitle { get; set; }

    [Column("NUMERO_PLAN_CONSTRUCTEUR")]
    public string? ConstructorPlanNumber { get; set; }

    [Column("NUMERO_PLAN_PROJET")]
    public string? ProjectPlanNumber { get; set; }

    [Column("DECOUPAGE_ZONAL")]
    public string? ZonalCutting { get; set; }

    [Column("DECOUPAGE_MACHINE")]
    public string? MachineCutting { get; set; }

    [Column("DECOUPAGE_SOUS_ENSEMBLE")]
    public string? SubAssemblyCutting { get; set; }

    [Column("DATE_DESSIN")]
    public DateTime? DrawingDate { get; set; }

    [Column("FORMAT_DE_FICHIER")]
    public int? FileFormat { get; set; }

    [Column("SPECIALITE")]
    public string? Specialty { get; set; }

    [Column("NUMERO_PLAN_SIDER")]
    public string? SiderPlanNumber { get; set; }

    [Column("NUMERO_PLAN_BM")]
    public string? BmPlanNumber { get; set; }

    [Column("DESSINATEUR")]
    public string? Drawer { get; set; }

    [Column("NUMERO_NOTICE_TECHNIQUE")]
    public string? TechnicalNoticeNumber { get; set; }

    [Column("NATURE_DOCUMENT")]
    public int? DocumentNature { get; set; }

    [Column("COB_UNITE")]
    public int? CobUnit { get; set; }

    [ForeignKey(nameof(Id))]
    public Fichier? Fichier { get; set; }
}
