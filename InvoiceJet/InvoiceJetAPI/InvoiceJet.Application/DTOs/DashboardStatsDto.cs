namespace InvoiceJet.Application.DTOs;

public class DashboardStatsDto
{
    public int TotalDocuments { get; set; } = 0;
    public int TotalClients { get; set; } = 0;
    public int TotalProducts { get; set; } = 0;
    public int TotalBankAccounts { get; set; } = 0;
    public List<MonthlyTotalDto>? MonthlyTotals { get; set; } = new List<MonthlyTotalDto>();
}