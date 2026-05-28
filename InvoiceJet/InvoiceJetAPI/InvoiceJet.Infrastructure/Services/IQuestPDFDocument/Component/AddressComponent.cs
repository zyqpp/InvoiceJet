using InvoiceJet.Application.DTOs;
using QuestPDF.Fluent;
using QuestPDF.Infrastructure;

namespace InvoiceJet.Infrastructure.Services.IQuestPDFDocument.Component;

public class AddressComponent : IComponent
{
    private string Title { get; }
    private FirmDto Address { get; set; }
    private BankAccountDto BankAccount { get; }

    public AddressComponent(string title, FirmDto address, BankAccountDto bankAccount = null)
    {
        Title = title;
        Address = address;
        BankAccount = bankAccount;
    }

    public void Compose(IContainer container)
    {
        container.ShowEntire().Column(column =>
        {
            column.Spacing(2);

            column.Item().Text(Title).SemiBold();
            column.Item().PaddingBottom(5).LineHorizontal(1);

            column.Item().Text(Address.Name);
            column.Item().Text(Address.Address);
            column.Item().Text($"{Address.City}, {Address.County}");
            if (!string.IsNullOrEmpty(Address.Cui))
            {
                column.Item().Text($"CUI: {Address.Cui}");
            }

            if (!string.IsNullOrEmpty(Address.RegCom))
            {
                column.Item().Text($"Reg. Com: {Address.RegCom}");
            }

            if (BankAccount != null)
            {
                if (!string.IsNullOrEmpty(BankAccount.BankName))
                {
                    column.Item().Text($"Bank: {BankAccount.BankName}");
                }
                if (!string.IsNullOrEmpty(BankAccount.Iban))
                {
                    column.Item().Text($"IBAN: {BankAccount.Iban}");
                }
            }
        });
    }
}