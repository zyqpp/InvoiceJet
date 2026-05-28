import { Component, OnInit } from "@angular/core";
import { IDashboardStats } from "src/app/models/IDashboardStats";
import { IMonthlyTotal } from "src/app/models/IMonthlyTotal";
import { DocumentService } from "src/app/services/document.service";
import { ChartOptions, ChartType } from "chart.js";

@Component({
  selector: "app-dashboard",
  templateUrl: "./dashboard.component.html",
  styleUrls: ["./dashboard.component.scss"],
})
export class DashboardComponent implements OnInit {
  documentTypes = [
    { id: 1, name: "Factura" },
    { id: 2, name: "Factura Proforma" },
    { id: 3, name: "Factura Storno" },
  ];

  years = Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - i);
  selectedYear: number = new Date().getFullYear();
  selectedDocumentType: number = 1;

  dashboardStats: IDashboardStats = {
    totalDocuments: 0,
    totalClients: 0,
    totalProducts: 0,
    totalBankAccounts: 0,
    monthlyTotals: [],
  };

  public lineChartOptions: ChartOptions = {
    responsive: true,
    interaction: {
      mode: "index",
      intersect: false,
    },
    maintainAspectRatio: false,
    scales: {
      y: {
        type: "linear",
        display: true,
        position: "left",
        beginAtZero: true,
      },
      y1: {
        type: "linear",
        display: true,
        position: "right",
        grid: {
          drawOnChartArea: false,
        },
      },
    },
    plugins: {
      legend: {
        display: true,
      },
      tooltip: {
        enabled: true,
        mode: "index",
        intersect: true,
      },
    },
  };

  public lineChartLabels: string[] = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  public lineChartType: ChartType = "line";
  public lineChartLegend = true;
  public lineChartData: any[] = [];

  constructor(private documentService: DocumentService) {}

  ngOnInit(): void {
    this.getDashboardData();
  }

  onSelectionChange() {
    this.getDashboardData();
  }

  getDashboardData() {
    this.documentService
      .getDashboardData(this.selectedYear, this.selectedDocumentType)
      .subscribe((data) => {
        this.dashboardStats = data;
        this.updateChartData(data.monthlyTotals);
      });
  }

  updateChartData(monthlyTotals: IMonthlyTotal[]) {
    const invoiceAmounts = new Array(12).fill(0);
    const incomeAmounts = new Array(12).fill(0);

    monthlyTotals.forEach((total) => {
      const index = total.month - 1;
      invoiceAmounts[index] = total.invoiceAmount;
      incomeAmounts[index] = total.incomeAmount;
    });

    console.log(invoiceAmounts);
    console.log(incomeAmounts);

    this.lineChartData = [
      { data: invoiceAmounts, label: "Invoice Amount", yAxisID: "y" },
      { data: incomeAmounts, label: "Income Amount", yAxisID: "y1" },
    ];
  }
}
