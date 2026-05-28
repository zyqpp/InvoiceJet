using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class DocumentTypeRepository : GenericRepository<DocumentType>, IDocumentTypeRepository
{
    public DocumentTypeRepository(InvoiceJetDbContext context) : base(context)
    {
    }
}