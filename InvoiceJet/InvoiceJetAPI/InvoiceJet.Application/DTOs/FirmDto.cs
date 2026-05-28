namespace InvoiceJet.Application.DTOs;

public class FirmDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Cui { get; set; } = string.Empty;
    public string? RegCom { get; set; }
    public string Address { get; set; } = string.Empty;
    public string County { get; set; } = string.Empty;
    public string City { get; set; } = string.Empty;
}