using InvoiceJet.Domain.Models;

namespace InvoiceJet.Application.DTOs;

public class DocumentRequestDto
{
    public int Id { get; set; }
    public string? DocumentNumber { get; set; }
    public FirmDto? Seller { get; set; }
    public FirmDto Client { get; set; } = null!;
    public DateTime IssueDate { get; set; }
    public DateTime? DueDate { get; set; }
    public BankAccountDto? BankAccount { get; set; }
    public DocumentSeriesDto? DocumentSeries { get; set; }
    public DocumentType? DocumentType { get; set; }
    public DocumentStatus? DocumentStatus { get; set; }
    public List<DocumentProductRequestDto> Products { get; set; } = null!;
}