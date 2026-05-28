namespace InvoiceJet.Application.DTOs;

public class DocumentStreamDto
{
    public string DocumentNumber { get; set; } = string.Empty;
    public byte[] PdfContent { get; set; } = Array.Empty<byte>();
}