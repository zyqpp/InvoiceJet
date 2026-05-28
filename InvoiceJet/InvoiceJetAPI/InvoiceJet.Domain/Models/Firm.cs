namespace InvoiceJet.Domain.Models;

public sealed class Firm : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public string Cui { get; set; } = string.Empty;
    public string RegCom { get; set; } = string.Empty;
    public string Address { get; set; } = string.Empty;
    public string County { get; set; } = string.Empty;
    public string City { get; set; } = string.Empty;

    public ICollection<UserFirm>? UserFirms { get; set; }
}