using InvoiceJet.Domain.Models;

namespace InvoiceJet.Domain.Interfaces.Repositories;

public interface IBankAccountRepository : IGenericRepository<BankAccount>
{
    Task<int> GetTotalBankAccountsAsync(int firmId);
    Task<List<BankAccount>> GetUserFirmBankAccountsAsync(Guid userId);
    Task<BankAccount?> GetUserFirmActiveBankAccountAsync(Guid userId);
}