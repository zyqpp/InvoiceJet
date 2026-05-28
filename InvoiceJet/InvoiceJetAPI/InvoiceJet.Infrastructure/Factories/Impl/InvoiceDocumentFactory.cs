using QuestPDF.Infrastructure;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Infrastructure.Services.IQuestPDFDocument;

namespace InvoiceJet.Infrastructure.Factories.Impl;

public class InvoiceDocumentFactory : IDocumentFactory
{
    public IDocument CreateDocument(DocumentRequestDto invoiceData)
    {
        return new InvoiceDocument(invoiceData);
    }
}