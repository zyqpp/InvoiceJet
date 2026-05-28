using InvoiceJet.Domain.Models;

namespace InvoiceJet.Application.DTOs;

public class DocumentTableRecordDto
{
    public int Id { get; set; }
    public string DocumentNumber { get; set; } = string.Empty;
    public string ClientName { get; set; } = string.Empty;
    public DateTime IssueDate { get; set; }
    public DateTime? DueDate { get; set; }
    public decimal TotalValue { get; set; }
    public DocumentStatus? DocumentStatus { get; set; }
}