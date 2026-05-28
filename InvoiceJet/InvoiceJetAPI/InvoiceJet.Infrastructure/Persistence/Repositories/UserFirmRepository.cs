using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class UserFirmRepository : GenericRepository<UserFirm>, IUserFirmRepository
{
    public UserFirmRepository(InvoiceJetDbContext context) : base(context)
    {
    }
    
    public async Task<UserFirm?> GetUserFirmById(Guid userId, int userFirmId)
    {
        return await _dbSet
            .Where(uf => uf.UserId == userId && uf.FirmId == userFirmId)
            .FirstOrDefaultAsync();
    }
    
    public async Task<List<UserFirm>> GetUserFirmClients(Guid userId)
    {
        return await _dbSet
            .Where(u => u.UserId.Equals(userId) && u.IsClient)
                .Include(f => f.Firm)
            .ToListAsync();
    }
}