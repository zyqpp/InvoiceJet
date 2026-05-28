using InvoiceJet.Domain.Models;

namespace InvoiceJet.Domain.Interfaces.Repositories;

public interface IFirmRepository : IGenericRepository<Firm>
{
    Task<int> GetTotalClientsAsync(Guid userId);
}