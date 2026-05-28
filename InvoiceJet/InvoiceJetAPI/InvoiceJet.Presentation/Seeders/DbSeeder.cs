using InvoiceJet.Domain.Models;
using InvoiceJet.Infrastructure.Persistence;

namespace InvoiceJet.Presentation.Seeders;

public static class DbSeeder
{
    public static async Task SeedDocumentTypes(IApplicationBuilder applicationBuilder)
    {
        using (var serviceScope = applicationBuilder.ApplicationServices.CreateScope())
        {
            var context = serviceScope.ServiceProvider.GetService<InvoiceJetDbContext>();
            context.Database.EnsureCreated();

            if (!context.DocumentType.Any())
            {
                var documentTypes = new List<DocumentType>
                {
                    new() { Name = "Factura" },
                    new() { Name = "Factura Proforma" },
                    new() { Name = "Factura Storno" }
                };

                context.DocumentType.AddRange(documentTypes);
                await context.SaveChangesAsync();
            }

            if (!context.DocumentStatus.Any())
            {
                var documentStatuses = new List<DocumentStatus>
                {
                    new() { Status = "Unpaid" },
                    new() { Status = "Paid" },
                };

                context.DocumentStatus.AddRange(documentStatuses);
                await context.SaveChangesAsync();
            }
        }
    }
}