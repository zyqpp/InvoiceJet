using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class FirmRepository : GenericRepository<Firm>, IFirmRepository
{
    public FirmRepository(InvoiceJetDbContext context) : base(context)
    {
    }
    
    public async Task<int> GetTotalClientsAsync(Guid userId)
    {
        return await _dbSet.CountAsync(f => f.UserFirms!.Any(uf => uf.UserId == userId && uf.IsClient));
    }
}