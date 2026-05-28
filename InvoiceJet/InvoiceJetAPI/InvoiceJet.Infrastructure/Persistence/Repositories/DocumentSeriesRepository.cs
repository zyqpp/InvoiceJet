using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class DocumentSeriesRepository : GenericRepository<DocumentSeries>, IDocumentSeriesRepository
{
    public DocumentSeriesRepository(InvoiceJetDbContext context) : base(context)
    {
    }

    public Task<List<DocumentSeries>> GetAllDocumentSeriesForActiveUserFirm(Guid userId)
    {
        return _dbSet
            .Include(ds => ds.UserFirm)
            .ThenInclude(uf => uf!.User)
            .Include(ds => ds.DocumentType)
            .Where(ds => ds.UserFirm!.UserId.Equals(userId) && ds.UserFirm.User.ActiveUserFirmId == ds.UserFirmId)
            .ToListAsync();
    }
}