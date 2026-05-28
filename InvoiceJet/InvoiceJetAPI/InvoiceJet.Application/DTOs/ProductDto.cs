using System.ComponentModel.DataAnnotations.Schema;

namespace InvoiceJet.Application.DTOs;

public class ProductDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    [Column(TypeName = "decimal(18,2)")] public decimal Price { get; set; }
    public bool ContainsTva { get; set; } = false;
    public string? UnitOfMeasurement { get; set; } = string.Empty;
    public int TvaValue { get; set; } = 19;
}