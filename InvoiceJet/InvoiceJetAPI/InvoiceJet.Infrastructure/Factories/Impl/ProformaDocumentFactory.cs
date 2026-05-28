using InvoiceJet.Application.DTOs;
using InvoiceJet.Infrastructure.Services.IQuestPDFDocument;
using QuestPDF.Infrastructure;

namespace InvoiceJet.Infrastructure.Factories.Impl;

public class ProformaDocumentFactory : IDocumentFactory
{
    public IDocument CreateDocument(DocumentRequestDto invoiceData)
    {
        return new ProformaInvoice(invoiceData);
    }
}