using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class BankAccountRepository : GenericRepository<BankAccount>, IBankAccountRepository
{
    public BankAccountRepository(InvoiceJetDbContext context) : base(context)
    {
    }

    public async Task<int> GetTotalBankAccountsAsync(int firmId)
    {
        return await _dbSet.Where(ba => ba.UserFirmId == firmId).CountAsync();
    }

    public async Task<List<BankAccount>> GetUserFirmBankAccountsAsync(Guid userId)
    {
        return await _dbSet
            .Where(ba => ba.UserFirm.UserId == userId && ba.UserFirm.User.ActiveUserFirmId == ba.UserFirmId)
            .ToListAsync();
    }
    
    public async Task<BankAccount?> GetUserFirmActiveBankAccountAsync(Guid userId)
    {
        return await _dbSet
            .Where(ba => ba.UserFirm.UserId == userId && ba.UserFirm.User.ActiveUserFirmId == ba.UserFirmId && ba.IsActive)
            .FirstOrDefaultAsync();
    }
}