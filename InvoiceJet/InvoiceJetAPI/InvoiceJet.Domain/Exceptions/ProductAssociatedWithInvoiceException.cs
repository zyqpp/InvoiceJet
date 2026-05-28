namespace InvoiceJet.Domain.Exceptions;

public class ProductAssociatedWithInvoiceException : Exception
{
    public ProductAssociatedWithInvoiceException(string productName) 
        : base($"Can't delete. Product {productName} is associated with an invoice.")
    {
    }
}