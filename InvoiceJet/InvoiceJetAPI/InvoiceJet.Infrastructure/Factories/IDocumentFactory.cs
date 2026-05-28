using InvoiceJet.Application.DTOs;
using QuestPDF.Infrastructure;

namespace InvoiceJet.Infrastructure.Factories;

public interface IDocumentFactory
{
    public IDocument CreateDocument(DocumentRequestDto invoiceData);
}
