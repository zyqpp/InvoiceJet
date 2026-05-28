namespace InvoiceJet.Domain.Models;

public sealed class DocumentSeries : BaseEntity
{
    public string SeriesName { get; set; } = string.Empty;
    public int FirstNumber { get; set; }
    public int CurrentNumber { get; set; }
    public bool IsDefault { get; set; }

    public int? DocumentTypeId { get; set; }
    public DocumentType? DocumentType { get; set; }

    public int? UserFirmId { get; set; }
    public UserFirm? UserFirm { get; set; }
}