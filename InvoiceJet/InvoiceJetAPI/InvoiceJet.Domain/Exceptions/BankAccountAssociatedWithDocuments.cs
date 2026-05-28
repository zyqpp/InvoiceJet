namespace InvoiceJet.Domain.Exceptions
{
    public class BankAccountAssociatedWithDocumentsException : Exception
    {
        public BankAccountAssociatedWithDocumentsException(string message) : base(message)
        {
        }
    }
}