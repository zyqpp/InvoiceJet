using InvoiceJet.Domain.Models;

namespace InvoiceJet.Domain.Interfaces.Repositories;

public interface IDocumentProductRepository : IGenericRepository<DocumentProduct>
{
    IEnumerable<DocumentProduct> GetAllDocumentProductsForDocument(int documentId);
}