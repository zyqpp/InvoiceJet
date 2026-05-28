using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Infrastructure.Persistence.Repositories;

public class DocumentRepository : GenericRepository<Document>, IDocumentRepository
{
    public DocumentRepository(InvoiceJetDbContext context) : base(context)
    {
    }

    public async Task<int> GetTotalDocumentsAsync(int firmId)
    {
        return await _dbSet.CountAsync(d => d.UserFirmId == firmId);
    }

    public Task<Document?> GetDocumentWithAllInfo(int documentId)
    {
        return _dbSet
            .Where(d => d.Id == documentId)
            .Include(d => d.DocumentStatus)
            .Include(d => d.DocumentProducts)!
            .ThenInclude(dp => dp.Product)
            .Include(d => d.Client)
            .FirstOrDefaultAsync();
    }

    public async Task<List<Document>> GetAllDocumentsByType(int activeUserFirmId, int documentTypeId)
    {
        return await _dbSet
            .Where(document => document.UserFirmId == activeUserFirmId && document.DocumentTypeId == documentTypeId)
            .Include(document => document.Client)
            .Include(document => document.DocumentStatus)
            .ToListAsync();
    }
}