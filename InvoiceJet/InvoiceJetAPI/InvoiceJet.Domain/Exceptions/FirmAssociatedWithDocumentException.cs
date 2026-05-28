namespace InvoiceJet.Domain.Exceptions;

public class FirmAssociatedWithDocumentException : Exception
{
    public FirmAssociatedWithDocumentException(string firmName) : base($"Can't delete. Firm {firmName} is associated with a document.")
    {
    }
}