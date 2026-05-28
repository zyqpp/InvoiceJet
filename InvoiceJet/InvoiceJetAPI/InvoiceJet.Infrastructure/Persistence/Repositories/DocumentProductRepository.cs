using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class DocumentProductRepository : GenericRepository<DocumentProduct>, IDocumentProductRepository
{
    public DocumentProductRepository(InvoiceJetDbContext context) : base(context)
    {
    }

    public IEnumerable<DocumentProduct> GetAllDocumentProductsForDocument(int documentId)
    {
        return _dbSet
            .Where(dp => dp.DocumentId == documentId);
    }
}