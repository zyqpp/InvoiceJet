namespace InvoiceJet.Domain.Exceptions;

public class UserHasNoAssociatedFirmException : Exception
{
    public UserHasNoAssociatedFirmException() : base("User has no associated firm. Add a firm in Firm Details page.")
    {
    }
}
