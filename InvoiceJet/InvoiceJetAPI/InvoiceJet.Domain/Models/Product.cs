using System.ComponentModel.DataAnnotations.Schema;

namespace InvoiceJet.Domain.Models;

public sealed class Product: BaseEntity
{
    public string Name { get; set; } = string.Empty;
    [Column(TypeName = "decimal(18,2)")] public decimal Price { get; set; }
    public bool ContainsTva { get; set; } = false;
    public string? UnitOfMeasurement { get; set; }
    public int TvaValue { get; set; } = 0;

    public int? UserFirmId { get; set; }
    public UserFirm? UserFirm { get; set; }
}