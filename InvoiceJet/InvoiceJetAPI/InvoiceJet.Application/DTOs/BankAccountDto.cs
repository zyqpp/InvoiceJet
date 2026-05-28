using InvoiceJet.Domain.Enums;

namespace InvoiceJet.Application.DTOs;

public class BankAccountDto
{
    public int Id { get; set; }
    public string BankName { get; set; } = string.Empty;
    public string Iban { get; set; } = string.Empty;
    public CurrencyEnum Currency { get; set; }
    public bool IsActive { get; set; }
}