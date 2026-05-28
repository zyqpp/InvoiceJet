using InvoiceJet.Application.DTOs;

namespace InvoiceJet.Application.Services;

public interface IPdfGenerationService
{
    string GenerateInvoicePdf(DocumentRequestDto invoiceData);
    byte[] GetInvoicePdfStream(DocumentRequestDto invoiceData);
}