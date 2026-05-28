namespace InvoiceJet.Domain.Exceptions;

public class ProductWithSameNameExistsException : Exception
{
    public ProductWithSameNameExistsException(string productName) 
        : base($"Product with name {productName} already exists.")
    {
    }
}