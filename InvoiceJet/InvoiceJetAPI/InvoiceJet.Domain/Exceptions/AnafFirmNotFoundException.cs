namespace InvoiceJet.Domain.Exceptions;

public class AnafFirmNotFoundException : Exception
{
    public AnafFirmNotFoundException(string cui) : base($"Firm with CUI {cui} not found in ANAF database.")
    {
    }
}