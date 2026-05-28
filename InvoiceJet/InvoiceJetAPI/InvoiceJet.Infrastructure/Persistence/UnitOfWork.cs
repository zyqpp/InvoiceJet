using InvoiceJet.Domain.Interfaces;
using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Infrastructure.Persistence.Repositories;

namespace InvoiceJet.Infrastructure.Persistence;

public class UnitOfWork(InvoiceJetDbContext context) : IUnitOfWork
{
    private readonly InvoiceJetDbContext _context = context;

    public IBankAccountRepository BankAccounts { get; } = new BankAccountRepository(context);
    public IDocumentProductRepository DocumentProducts { get; } = new DocumentProductRepository(context);
    public IDocumentRepository Documents { get; } = new DocumentRepository(context);
    public IDocumentSeriesRepository DocumentSeries { get; } = new DocumentSeriesRepository(context);
    public IDocumentStatusRepository DocumentStatuses { get; } = new DocumentStatusRepository(context);
    public IDocumentTypeRepository DocumentTypes { get; } = new DocumentTypeRepository(context);
    public IFirmRepository Firms { get; } = new FirmRepository(context);
    public IProductRepository Products { get; } = new ProductRepository(context);
    public IUserFirmRepository UserFirms { get; } = new UserFirmRepository(context);
    public IUserRepository Users { get; } = new UserRepository(context);

    public async Task<int> CompleteAsync()
    {
        return await _context.SaveChangesAsync();
    }

    public void Dispose()
    {
        _context.Dispose();
    }
}