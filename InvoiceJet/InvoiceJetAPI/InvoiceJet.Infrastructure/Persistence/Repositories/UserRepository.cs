using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class UserRepository : GenericRepository<User>, IUserRepository
{
    public UserRepository(InvoiceJetDbContext context) : base(context)
    {
    }

    public async Task<int?> GetUserFirmIdAsync(Guid userId)
    {
        var user = await _dbSet
            .Where(u => u.Id == userId)
            .Include(u => u.ActiveUserFirm)
            .SingleOrDefaultAsync();

        if (user == null)
        {
            return null;
        }

        return user.ActiveUserFirm?.UserFirmId;
    }

    public async Task<UserFirm?> GetUserFirmAsync(Guid userId)
    {
        var userFirm = await _dbSet
            .Where(u => u.Id == userId)
                .Include(uf => uf.ActiveUserFirm)
                    .ThenInclude(uf => uf.Firm)
                .Include(uf => uf.ActiveUserFirm)
                    .ThenInclude(u => u.User)
            .Select(uf => uf.ActiveUserFirm)
            .SingleOrDefaultAsync();

        return userFirm;
    }

    public Task<User?> GetUserByIdAsync(Guid userId)
    {
        var user = _dbSet
            .Where(u => u.Id == userId)
                .Include(uf => uf.ActiveUserFirm)
            .SingleOrDefaultAsync();

        return user;
    }
}