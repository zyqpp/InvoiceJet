using InvoiceJet.Application.DTOs;

namespace InvoiceJet.Application.Services;

public interface IDocumentService
{
    Task<DocumentAutofillDto> GetDocumentAutofillInfo(int documentTypeId);
    Task<DocumentRequestDto> AddDocument(DocumentRequestDto documentRequestDto);
    Task<DocumentRequestDto> EditDocument(DocumentRequestDto documentRequestDto);
    Task<DocumentRequestDto> GeneratePdfDocument(DocumentRequestDto documentRequestDto);
    Task<DocumentStreamDto> GetInvoicePdfStream(DocumentRequestDto documentRequestDto);
    Task<List<DocumentTableRecordDto>> GetDocumentTableRecords(int documentTypeId);
    Task<DocumentRequestDto> GetDocumentById(int documentId);
    Task DeleteDocuments(int[] documentIds);
    Task<DashboardStatsDto> GetDashboardStats(int year, int documentType);
    Task TransformToStorno(int[] documentIds);
}