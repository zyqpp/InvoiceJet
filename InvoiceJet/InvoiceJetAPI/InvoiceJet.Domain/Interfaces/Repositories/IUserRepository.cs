using InvoiceJet.Domain.Models;

namespace InvoiceJet.Domain.Interfaces.Repositories;

public interface IUserRepository : IGenericRepository<User>
{
    public Task<User?> GetUserByIdAsync(Guid userId);
    public Task<int?> GetUserFirmIdAsync(Guid userId);
    public Task<UserFirm?> GetUserFirmAsync(Guid userId);
}