using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Infrastructure.Persistence;

public class InvoiceJetDbContext : DbContext
{
    public InvoiceJetDbContext(DbContextOptions<InvoiceJetDbContext> options) : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>()
            .HasOne(u => u.ActiveUserFirm)
            .WithMany()
            .HasForeignKey(u => u.ActiveUserFirmId)
            .IsRequired(false);

        modelBuilder.Entity<Product>()
            .HasIndex(p => p.Name)
            .IsUnique();
    }

    public DbSet<User> User { get; set; }
    public DbSet<Firm> Firm { get; set; }
    public DbSet<BankAccount> BankAccount { get; set; }
    public DbSet<UserFirm> UserFirm { get; set; }
    public DbSet<Product> Product { get; set; }
    public DbSet<DocumentType> DocumentType { get; set; }
    public DbSet<DocumentSeries> DocumentSeries { get; set; }
    public DbSet<Document> Document { get; set; }
    public DbSet<DocumentProduct> DocumentProduct { get; set; }
    public DbSet<DocumentStatus> DocumentStatus { get; set; }
}