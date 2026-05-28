using InvoiceJet.Domain.Models;

namespace InvoiceJet.Application.DTOs;

public class DocumentAutofillDto
{
    public List<FirmDto> Clients { get; set; } = null!;
    public List<DocumentSeriesDto> DocumentSeries { get; set; } = null!;
    public List<DocumentStatusDto> DocumentStatuses { get; set; } = null!;
    public List<ProductDto> Products { get; set; } = null!;
}