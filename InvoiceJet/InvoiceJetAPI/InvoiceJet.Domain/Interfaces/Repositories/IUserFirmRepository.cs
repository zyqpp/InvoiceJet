using InvoiceJet.Domain.Models;

namespace InvoiceJet.Domain.Interfaces.Repositories;

public interface IUserFirmRepository : IGenericRepository<UserFirm>
{
    Task<UserFirm?> GetUserFirmById(Guid userId, int userFirmId);
    Task<List<UserFirm>> GetUserFirmClients(Guid userId);
}