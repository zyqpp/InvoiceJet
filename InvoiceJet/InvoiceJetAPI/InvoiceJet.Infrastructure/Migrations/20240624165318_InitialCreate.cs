using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace InvoiceJet.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "DocumentStatus",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Status = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_DocumentStatus", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "DocumentType",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_DocumentType", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Firm",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Cui = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    RegCom = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Address = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    County = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    City = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Firm", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "BankAccount",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    BankName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Iban = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Currency = table.Column<int>(type: "int", nullable: false),
                    IsActive = table.Column<bool>(type: "bit", nullable: false),
                    UserFirmId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_BankAccount", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Document",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    DocumentNumber = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    IssueDate = table.Column<DateTime>(type: "datetime2", nullable: false),
                    DueDate = table.Column<DateTime>(type: "datetime2", nullable: true),
                    UnitPrice = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    TotalPrice = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    BankAccountId = table.Column<int>(type: "int", nullable: false),
                    DocumentTypeId = table.Column<int>(type: "int", nullable: true),
                    DocumentStatusId = table.Column<int>(type: "int", nullable: true),
                    ClientId = table.Column<int>(type: "int", nullable: true),
                    UserFirmId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Document", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Document_BankAccount_BankAccountId",
                        column: x => x.BankAccountId,
                        principalTable: "BankAccount",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_Document_DocumentStatus_DocumentStatusId",
                        column: x => x.DocumentStatusId,
                        principalTable: "DocumentStatus",
                        principalColumn: "Id");
                    table.ForeignKey(
                        name: "FK_Document_DocumentType_DocumentTypeId",
                        column: x => x.DocumentTypeId,
                        principalTable: "DocumentType",
                        principalColumn: "Id");
                    table.ForeignKey(
                        name: "FK_Document_Firm_ClientId",
                        column: x => x.ClientId,
                        principalTable: "Firm",
                        principalColumn: "Id");
                });

            migrationBuilder.CreateTable(
                name: "DocumentProduct",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Quantity = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    UnitPrice = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    TotalPrice = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    DocumentId = table.Column<int>(type: "int", nullable: true),
                    ProductId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_DocumentProduct", x => x.Id);
                    table.ForeignKey(
                        name: "FK_DocumentProduct_Document_DocumentId",
                        column: x => x.DocumentId,
                        principalTable: "Document",
                        principalColumn: "Id");
                });

            migrationBuilder.CreateTable(
                name: "DocumentSeries",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    SeriesName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    FirstNumber = table.Column<int>(type: "int", nullable: false),
                    CurrentNumber = table.Column<int>(type: "int", nullable: false),
                    IsDefault = table.Column<bool>(type: "bit", nullable: false),
                    DocumentTypeId = table.Column<int>(type: "int", nullable: true),
                    UserFirmId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_DocumentSeries", x => x.Id);
                    table.ForeignKey(
                        name: "FK_DocumentSeries_DocumentType_DocumentTypeId",
                        column: x => x.DocumentTypeId,
                        principalTable: "DocumentType",
                        principalColumn: "Id");
                });

            migrationBuilder.CreateTable(
                name: "Product",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    Price = table.Column<decimal>(type: "decimal(18,2)", nullable: false),
                    ContainsTva = table.Column<bool>(type: "bit", nullable: false),
                    UnitOfMeasurement = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    TvaValue = table.Column<int>(type: "int", nullable: false),
                    UserFirmId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Product", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "User",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    FirstName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    LastName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Email = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    PasswordHash = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Role = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    ActiveUserFirmId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_User", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "UserFirm",
                columns: table => new
                {
                    UserFirmId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    UserId = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    FirmId = table.Column<int>(type: "int", nullable: false),
                    IsClient = table.Column<bool>(type: "bit", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_UserFirm", x => x.UserFirmId);
                    table.ForeignKey(
                        name: "FK_UserFirm_Firm_FirmId",
                        column: x => x.FirmId,
                        principalTable: "Firm",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_UserFirm_User_UserId",
                        column: x => x.UserId,
                        principalTable: "User",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_BankAccount_UserFirmId",
                table: "BankAccount",
                column: "UserFirmId");

            migrationBuilder.CreateIndex(
                name: "IX_Document_BankAccountId",
                table: "Document",
                column: "BankAccountId");

            migrationBuilder.CreateIndex(
                name: "IX_Document_ClientId",
                table: "Document",
                column: "ClientId");

            migrationBuilder.CreateIndex(
                name: "IX_Document_DocumentStatusId",
                table: "Document",
                column: "DocumentStatusId");

            migrationBuilder.CreateIndex(
                name: "IX_Document_DocumentTypeId",
                table: "Document",
                column: "DocumentTypeId");

            migrationBuilder.CreateIndex(
                name: "IX_Document_UserFirmId",
                table: "Document",
                column: "UserFirmId");

            migrationBuilder.CreateIndex(
                name: "IX_DocumentProduct_DocumentId",
                table: "DocumentProduct",
                column: "DocumentId");

            migrationBuilder.CreateIndex(
                name: "IX_DocumentProduct_ProductId",
                table: "DocumentProduct",
                column: "ProductId");

            migrationBuilder.CreateIndex(
                name: "IX_DocumentSeries_DocumentTypeId",
                table: "DocumentSeries",
                column: "DocumentTypeId");

            migrationBuilder.CreateIndex(
                name: "IX_DocumentSeries_UserFirmId",
                table: "DocumentSeries",
                column: "UserFirmId");

            migrationBuilder.CreateIndex(
                name: "IX_Product_Name",
                table: "Product",
                column: "Name",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Product_UserFirmId",
                table: "Product",
                column: "UserFirmId");

            migrationBuilder.CreateIndex(
                name: "IX_User_ActiveUserFirmId",
                table: "User",
                column: "ActiveUserFirmId");

            migrationBuilder.CreateIndex(
                name: "IX_UserFirm_FirmId",
                table: "UserFirm",
                column: "FirmId");

            migrationBuilder.CreateIndex(
                name: "IX_UserFirm_UserId",
                table: "UserFirm",
                column: "UserId");

            migrationBuilder.AddForeignKey(
                name: "FK_BankAccount_UserFirm_UserFirmId",
                table: "BankAccount",
                column: "UserFirmId",
                principalTable: "UserFirm",
                principalColumn: "UserFirmId",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_Document_UserFirm_UserFirmId",
                table: "Document",
                column: "UserFirmId",
                principalTable: "UserFirm",
                principalColumn: "UserFirmId");

            migrationBuilder.AddForeignKey(
                name: "FK_DocumentProduct_Product_ProductId",
                table: "DocumentProduct",
                column: "ProductId",
                principalTable: "Product",
                principalColumn: "Id");

            migrationBuilder.AddForeignKey(
                name: "FK_DocumentSeries_UserFirm_UserFirmId",
                table: "DocumentSeries",
                column: "UserFirmId",
                principalTable: "UserFirm",
                principalColumn: "UserFirmId");

            migrationBuilder.AddForeignKey(
                name: "FK_Product_UserFirm_UserFirmId",
                table: "Product",
                column: "UserFirmId",
                principalTable: "UserFirm",
                principalColumn: "UserFirmId");

            migrationBuilder.AddForeignKey(
                name: "FK_User_UserFirm_ActiveUserFirmId",
                table: "User",
                column: "ActiveUserFirmId",
                principalTable: "UserFirm",
                principalColumn: "UserFirmId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_User_UserFirm_ActiveUserFirmId",
                table: "User");

            migrationBuilder.DropTable(
                name: "DocumentProduct");

            migrationBuilder.DropTable(
                name: "DocumentSeries");

            migrationBuilder.DropTable(
                name: "Document");

            migrationBuilder.DropTable(
                name: "Product");

            migrationBuilder.DropTable(
                name: "BankAccount");

            migrationBuilder.DropTable(
                name: "DocumentStatus");

            migrationBuilder.DropTable(
                name: "DocumentType");

            migrationBuilder.DropTable(
                name: "UserFirm");

            migrationBuilder.DropTable(
                name: "Firm");

            migrationBuilder.DropTable(
                name: "User");
        }
    }
}
