using InvoiceJet.Domain.Models;

namespace InvoiceJet.Domain.Interfaces.Repositories;

public interface IDocumentRepository : IGenericRepository<Document>
{
    Task<int> GetTotalDocumentsAsync(int firmId);
    Task<Document?> GetDocumentWithAllInfo(int documentId);
    Task<List<Document>> GetAllDocumentsByType(int activeUserFirmId, int documentTypeId);
}