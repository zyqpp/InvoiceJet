namespace InvoiceJet.Domain.Models;

public sealed class DocumentStatus: BaseEntity
{
    public string Status { get; set; } = string.Empty;
}