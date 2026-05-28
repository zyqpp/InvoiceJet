using InvoiceJet.Domain.Enums;

namespace InvoiceJet.Domain.Models;

public sealed class BankAccount : BaseEntity
{
    public string BankName { get; set; } = string.Empty;
    public string Iban { get; set; } = string.Empty;
    public CurrencyEnum Currency { get; set; }
    public bool IsActive { get; set; } = false;

    public int UserFirmId { get; set; }
    public UserFirm UserFirm { get; set; }
}