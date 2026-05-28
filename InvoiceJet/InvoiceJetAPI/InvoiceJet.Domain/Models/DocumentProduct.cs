using System.ComponentModel.DataAnnotations.Schema;

namespace InvoiceJet.Domain.Models;

public sealed class DocumentProduct : BaseEntity
{
    [Column(TypeName = "decimal(18,2)")]
    public decimal Quantity { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal TotalPrice { get; set; }

    public int? DocumentId { get; set; }
    public Document? Document { get; set; }

    public int? ProductId { get; set; }
    public Product? Product { get; set; }
}