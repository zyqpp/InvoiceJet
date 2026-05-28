using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class DocumentStatusRepository : GenericRepository<DocumentStatus>, IDocumentStatusRepository
{
    public DocumentStatusRepository(InvoiceJetDbContext context) : base(context)
    {
    }
}
