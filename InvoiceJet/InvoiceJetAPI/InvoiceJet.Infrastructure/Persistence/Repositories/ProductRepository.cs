using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class ProductRepository : GenericRepository<Product>, IProductRepository
{
    public ProductRepository(InvoiceJetDbContext context) : base(context)
    {
    }
    
    public async Task<int> GetTotalProductsAsync(int firmId)
    {
        return await _dbSet.Where(p => p.UserFirmId == firmId).CountAsync();
    }

    public async Task<List<Product>> GetUserFirmProductsAsync(Guid userId)
    {
        return await _dbSet
            .Where(p => p.UserFirm!.UserId == userId && p.UserFirm.User.ActiveUserFirmId == p.UserFirmId)
            .ToListAsync();
    }

    public async Task<List<Product>> GetProductsByIds(int[] productIds)
    {
       return await _dbSet
            .Where(p => productIds.Contains(p.Id))
            .ToListAsync();
    }
    
    public async Task<Product?> FindUserFirmProductByName(Guid userId, string name)
    {
        return await _dbSet
            .Where(p => p.UserFirm!.UserId == userId && p.UserFirm.User.ActiveUserFirmId == p.UserFirmId)
            .FirstOrDefaultAsync(p => p.Name == name);
    }
}