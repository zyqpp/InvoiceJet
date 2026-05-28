using InvoiceJet.Domain.Models;

namespace InvoiceJet.Domain.Interfaces.Repositories;

public interface IProductRepository : IGenericRepository<Product>
{
    Task<int> GetTotalProductsAsync(int firmId);
    Task<List<Product>> GetUserFirmProductsAsync(Guid userId);
    Task<Product?> FindUserFirmProductByName(Guid userId, string name);
}