using InvoiceJet.Domain.Interfaces.Repositories;

namespace InvoiceJet.Domain.Interfaces;

public interface IUnitOfWork : IDisposable
{
    IBankAccountRepository BankAccounts { get; }
    IDocumentProductRepository DocumentProducts { get; }
    IDocumentRepository Documents { get; }
    IDocumentSeriesRepository DocumentSeries { get; }
    IDocumentStatusRepository DocumentStatuses { get; }
    IDocumentTypeRepository DocumentTypes { get; }
    IFirmRepository Firms { get; }
    IProductRepository Products { get; }
    IUserFirmRepository UserFirms { get; }
    IUserRepository Users { get; }

    Task<int> CompleteAsync();
}