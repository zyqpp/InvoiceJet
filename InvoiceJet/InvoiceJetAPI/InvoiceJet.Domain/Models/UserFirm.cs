namespace InvoiceJet.Domain.Models;

public sealed class UserFirm
{
    public int UserFirmId { get; set; } 

    public Guid UserId { get; set; }
    public int FirmId { get; set; }

    public bool IsClient { get; set; } = true;

    public User User { get; set; } = null!;
    public Firm Firm { get; set; } = null!;

    public ICollection<BankAccount>? BankAccounts { get; set; }
    public ICollection<Product>? Products { get; set; }
    public ICollection<DocumentSeries>? DocumentSeries { get; set; }
    public ICollection<Document>? Documents { get; set; }
}