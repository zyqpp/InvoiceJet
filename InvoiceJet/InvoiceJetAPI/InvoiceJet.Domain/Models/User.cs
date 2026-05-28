namespace InvoiceJet.Domain.Models;

public sealed class User
{
    public Guid Id { get; set; }
    
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;

    public int? ActiveUserFirmId { get; set; }
    public UserFirm ActiveUserFirm { get; set; } = null!;
}