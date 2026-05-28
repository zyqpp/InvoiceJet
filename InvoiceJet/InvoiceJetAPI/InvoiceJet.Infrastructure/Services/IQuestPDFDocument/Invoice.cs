using InvoiceJet.Application.DTOs;
using InvoiceJet.Infrastructure.Services.IQuestPDFDocument.Component;
using QuestPDF.Fluent;
using QuestPDF.Helpers;
using QuestPDF.Infrastructure;

namespace InvoiceJet.Infrastructure.Services.IQuestPDFDocument;

public class InvoiceDocument : IDocument
{
    public DocumentRequestDto Model { get; }

    public string FullDocumentNumber
    {
        get
        {
            if (Model.DocumentSeries != null)
            {
                string seriesName = Model.DocumentSeries.SeriesName;
                string formattedNumber = Model.DocumentSeries.CurrentNumber.ToString("D4");
                return seriesName + formattedNumber;
            }
            else
            {
                return Model.DocumentNumber;
            }
        }
    }

    public InvoiceDocument(DocumentRequestDto model)
    {
        Model = model;
    }

    public DocumentMetadata GetMetadata() => DocumentMetadata.Default;

    public void Compose(IDocumentContainer container)
    {
        container
            .Page(page =>
            {
                page.Margin(50);

                page.Header().Element(ComposeHeader);
                page.Content().Element(ComposeContent);

                page.Footer().AlignCenter().Text(text =>
                {
                    text.CurrentPageNumber();
                    text.Span(" / ");
                    text.TotalPages();
                });
            });
    }

    private void ComposeHeader(IContainer container)
    {
        container.Row(row =>
        {
            row.RelativeItem().Column(column =>
            {
                column
                    .Item().Text($"Invoice #{FullDocumentNumber}")
                    .FontSize(20).SemiBold().FontColor(Colors.Blue.Medium);

                column.Item().Text(text =>
                {
                    text.Span("Issue date: ").SemiBold();
                    text.Span($"{Model.IssueDate:d}");
                });

                if (Model.DueDate.HasValue)
                {
                    column.Item().Text(text =>
                    {
                        text.Span("Due date: ").SemiBold();
                        text.Span($"{Model.DueDate.Value:d}");
                    });
                }
            });
            
            row.ConstantItem(100).Element(e =>
            {
                // Check if the document status is "Paid"
                if (Model.DocumentStatus?.Status == "Paid")
                {
                    e.Background(Colors.Green.Medium) // Green background for paid
                        .AlignCenter()
                        .AlignMiddle()
                        .Padding(5)
                        .Text("Paid") // Display "Paid"
                        .FontSize(14)
                        .Bold();
                }
                else
                {
                    e.Background(Colors.Red.Medium) // Red background for unpaid
                        .AlignCenter()
                        .AlignMiddle()
                        .Padding(5)
                        .Text("Unpaid") // Display "Unpaid"
                        .FontSize(14)
                        .Bold();
                }
            });
            
            // Optional: Add company logo if available
            // row.ConstantItem(175).Image(LogoImage);
        });
    }

    private void ComposeContent(IContainer container)
    {
        container.PaddingVertical(40).Column(column =>
        {
            column.Spacing(20);

            column.Item().Row(row =>
            {
                row.RelativeItem().Component(new AddressComponent("From", Model.Seller, Model.BankAccount));
                row.ConstantItem(50);
                row.RelativeItem().Component(new AddressComponent("For", Model.Client));
            });

            column.Item().Element(ComposeTable);

            // Optional: Add comments or additional sections as needed
        });
    }

    private void ComposeTable(IContainer container)
    {
        container.Table(table =>
        {
            table.ColumnsDefinition(columns =>
            {
                columns.ConstantColumn(25);
                columns.RelativeColumn(3);
                columns.RelativeColumn();
                columns.RelativeColumn();
                columns.RelativeColumn();
                columns.RelativeColumn();
            });

            table.Header(header =>
            {
                header.Cell().Text("#");
                header.Cell().Text("Product").Style(TextStyle.Default.SemiBold());
                header.Cell().AlignRight().Text("Qt.").Style(TextStyle.Default.SemiBold());
                header.Cell().AlignRight().Text("Unit price").Style(TextStyle.Default.SemiBold());
                header.Cell().AlignRight().Text("Value").Style(TextStyle.Default.SemiBold());
                header.Cell().AlignRight().Text("Total TVA").Style(TextStyle.Default.SemiBold());
                
                header.Cell().ColumnSpan(6).PaddingVertical(5).BorderBottom(1).BorderColor(Colors.Black);
            });

            int index = 0;
            foreach (var item in Model.Products)
            {
                index++;
                var value = item.UnitPrice * item.Quantity;
                var totalTVAItem = item.TotalPrice - item.UnitPrice * item.Quantity;
                table.Cell().Text($"{index}");
                table.Cell().Text(item.Name);
                table.Cell().AlignRight().Text($"{item.Quantity}");
                table.Cell().AlignRight().Text($"{item.UnitPrice}");
                table.Cell().AlignRight().Text($"{value:F2}");
                table.Cell().AlignRight().Text($"{totalTVAItem:F2}");
                
                table.Cell().ColumnSpan(6).PaddingVertical(5).BorderBottom(1).BorderColor(Colors.Grey.Lighten2);
            }
            
            var subtotal = Model.Products.Sum(x => x.UnitPrice * x.Quantity);
            var totalTVA = Model.Products.Sum(x => x.TotalPrice - x.UnitPrice * x.Quantity);
            var grandTotal = subtotal + totalTVA;
            
            table.Footer(footer =>
            {
                footer.Cell().ColumnSpan(3);  // Empty columns to align the text
                footer.Cell().Element(cell => cell.BorderBottom(1).BorderColor(Colors.Grey.Lighten2).PaddingVertical(5))
                    .AlignRight().Text("Subtotal:");
                footer.Cell().Element(cell => cell.BorderBottom(1).BorderColor(Colors.Grey.Lighten2).PaddingVertical(5))
                    .AlignRight().Text($"{subtotal:F2}");
                footer.Cell().Element(cell => cell.BorderBottom(1).BorderColor(Colors.Grey.Lighten2).PaddingVertical(5))
                    .AlignRight().Text($"{totalTVA:F2}");
                
                footer.Cell().ColumnSpan(3);  // Empty columns to align the text
                footer.Cell().Element(cell => cell.BorderBottom(1).BorderColor(Colors.Grey.Lighten2).PaddingVertical(5))
                    .AlignRight().Text($"Total pay:");
                footer.Cell().ColumnSpan(2).Element(cell => cell.BorderBottom(1).BorderColor(Colors.Grey.Lighten2).PaddingVertical(5))
                    .AlignRight().Text($"{grandTotal:F2} lei").FontSize(16).Bold();
            });
        });
    }
}