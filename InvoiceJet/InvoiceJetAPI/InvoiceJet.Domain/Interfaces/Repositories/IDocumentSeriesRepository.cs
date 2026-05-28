using InvoiceJet.Domain.Models;

namespace InvoiceJet.Domain.Interfaces.Repositories;

public interface IDocumentSeriesRepository : IGenericRepository<DocumentSeries>
{
    Task<List<DocumentSeries>> GetAllDocumentSeriesForActiveUserFirm(Guid userId);
}