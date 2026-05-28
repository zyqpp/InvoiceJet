namespace InvoiceJet.Domain.Models;

public sealed class Document : BaseEntity
{
    public string DocumentNumber { get; set; } = string.Empty;
    public DateTime IssueDate { get; set; }
    public DateTime? DueDate { get; set; }
    public decimal UnitPrice { get; set; }
    public decimal TotalPrice { get; set; }

    public int BankAccountId { get; set; }
    public BankAccount? BankAccount { get; set; }
    
    public int? DocumentTypeId { get; set; }
    public DocumentType? DocumentType { get; set; }

    public int? DocumentStatusId { get; set; }
    public DocumentStatus? DocumentStatus { get; set; }

    public int? ClientId { get; set; }
    public Firm? Client { get; set; }
    
    public int? UserFirmId { get; set; }
    public UserFirm? UserFirm { get; set; }

    public ICollection<DocumentProduct>? DocumentProducts { get; set; }
}