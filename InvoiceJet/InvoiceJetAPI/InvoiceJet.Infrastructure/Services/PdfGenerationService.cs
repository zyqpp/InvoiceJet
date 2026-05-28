using InvoiceJet.Application.DTOs;
using InvoiceJet.Application.Services;
using InvoiceJet.Infrastructure.Factories;
using InvoiceJet.Infrastructure.Services.IQuestPDFDocument;
using QuestPDF.Fluent;
using QuestPDF.Infrastructure;

namespace InvoiceJet.Infrastructure.Services;

public class PdfGenerationService : IPdfGenerationService
{
    public string GenerateInvoicePdf(DocumentRequestDto invoiceData)
    {
        try
        {
            string filePath = GetInvoicePdfPath(invoiceData.DocumentSeries.CurrentNumber);

            IDocument document = new InvoiceDocument(invoiceData);

            document.GeneratePdf(filePath);

            return filePath;
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error generating PDF: " + ex.Message);
            return null;
        }
    }

    public byte[] GetInvoicePdfStream(DocumentRequestDto invoiceData)
    {
        try
        {
            using (var memoryStream = new MemoryStream())
            {
                DocumentFactoryProvider documentFactoryProvider = new DocumentFactoryProvider();
                IDocumentFactory documentFactory = documentFactoryProvider.GetDocumentFactory(invoiceData.DocumentType!.Id);
                IDocument document = documentFactory.CreateDocument(invoiceData);
                document.GeneratePdf(memoryStream);

                return memoryStream.ToArray();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error generating PDF: " + ex.Message);
            return null;
        }
    }

    private string GetInvoicePdfPath(int invoiceNumber)
    {
        string basePath = AppDomain.CurrentDomain.BaseDirectory;
        string documentsPath = Path.Combine(basePath, "Documents");
        if (!Directory.Exists(documentsPath))
        {
            Directory.CreateDirectory(documentsPath);
        }

        return Path.Combine(documentsPath, $"Invoice_{invoiceNumber}.pdf");
    }
}