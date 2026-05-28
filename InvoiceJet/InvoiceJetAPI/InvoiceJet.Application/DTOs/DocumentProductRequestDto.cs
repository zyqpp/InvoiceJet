namespace InvoiceJet.Application.DTOs;

public class DocumentProductRequestDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal UnitPrice { get; set; }
    public decimal TotalPrice { get; set; }
    public bool ContainsTva { get; set; } = false;
    public string UnitOfMeasurement { get; set; } = string.Empty;
    public int TvaValue { get; set; } = 19;
    public int Quantity { get; set; }
}