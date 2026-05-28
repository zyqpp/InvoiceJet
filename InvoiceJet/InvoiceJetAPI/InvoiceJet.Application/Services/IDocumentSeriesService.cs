using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Models;

namespace InvoiceJet.Application.Services;

public interface IDocumentSeriesService
{
    Task<List<DocumentSeriesDto>> GetAllDocumentSeriesForUserId();
    Task AddInitialDocumentSeries(UserFirm userFirm);
    Task AddDocumentSeries(DocumentSeriesDto documentSeriesDto);
    Task UpdateDocumentSeries(DocumentSeriesDto documentSeriesDto);
    Task DeleteDocumentSeries(int[] documentSeriesIds);
}