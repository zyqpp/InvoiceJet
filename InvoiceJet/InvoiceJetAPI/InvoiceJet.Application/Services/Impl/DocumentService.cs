using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Enums;
using InvoiceJet.Domain.Exceptions;
using InvoiceJet.Domain.Interfaces;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Application.Services.Impl;

public class DocumentService : IDocumentService
{
    private readonly IMapper _mapper;
    private readonly IUserService _userService;
    private readonly IPdfGenerationService _pdfGenerationService;
    private readonly IUnitOfWork _unitOfWork;

    public DocumentService(IMapper mapper, IPdfGenerationService pdfGenerationService, IUnitOfWork unitOfWork,
        IUserService userService)
    {
        _mapper = mapper;
        _pdfGenerationService = pdfGenerationService;
        _unitOfWork = unitOfWork;
        _userService = userService;
    }

    private async Task UpdateDocumentProducts(int documentId, List<DocumentProductRequestDto> documentProductsDto,
        int userFirmId)
    {
        decimal totalInvoicePrice = 0;
        decimal totalInvoicePriceWithTva = 0;

        var existingDocumentProducts = _unitOfWork.DocumentProducts.GetAllDocumentProductsForDocument(documentId);
        await _unitOfWork.DocumentProducts.RemoveRangeAsync(existingDocumentProducts);

        foreach (var documentProductDto in documentProductsDto)
        {
            Product product;

            if (documentProductDto.Id > 0)
            {
                product = await _unitOfWork.Products.Query()
                    .FirstOrDefaultAsync(product => product.Name == documentProductDto.Name && product.UserFirmId == userFirmId);
                if (product == null)
                {
                    throw new Exception("Product not found.");
                }
            }
            else
            {
                product = _mapper.Map<Product>(documentProductDto);
                product.UserFirmId = userFirmId;
                await _unitOfWork.Products.AddAsync(product);
            }

            var documentProduct = new DocumentProduct
            {
                Quantity = documentProductDto.Quantity,
                Product = product,
                DocumentId = documentId,
                UnitPrice = documentProductDto.UnitPrice,
                TotalPrice = documentProductDto.TotalPrice,
            };

            totalInvoicePrice += documentProductDto.UnitPrice * documentProductDto.Quantity;
            totalInvoicePriceWithTva += documentProductDto.TotalPrice;

            await _unitOfWork.DocumentProducts.AddAsync(documentProduct);
        }

        var document = await _unitOfWork.Documents.GetByIdAsync(documentId);
        if (document != null)
        {
            document.UnitPrice = totalInvoicePrice;
            document.TotalPrice = totalInvoicePriceWithTva;
            await _unitOfWork.Documents.UpdateAsync(document);
        }
    }

    public async Task<DocumentRequestDto> AddDocument(DocumentRequestDto documentRequestDto)
    {
        var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
        if (!userFirmId.HasValue)
        {
            throw new UserHasNoAssociatedFirmException();
        }

        var document = new Document
        {
            Id = documentRequestDto.Id,
            DocumentNumber = documentRequestDto.DocumentSeries?.SeriesName +
                             documentRequestDto.DocumentSeries?.CurrentNumber.ToString("D4"),
            IssueDate = documentRequestDto.IssueDate,
            DueDate = documentRequestDto.DueDate,
            DocumentTypeId = documentRequestDto.DocumentSeries?.DocumentType?.Id,
            DocumentStatusId = (int)DocumentStatusEnum.Unpaid,
            BankAccount = await _unitOfWork.BankAccounts.Query()
                .Where(ba => ba.UserFirmId == userFirmId && ba.IsActive)
                .FirstOrDefaultAsync() ?? throw new NoBankAccountAddedException(),
            ClientId = documentRequestDto.Client.Id,
            UserFirmId = userFirmId
        };

        await _unitOfWork.Documents.AddAsync(document);
        await _unitOfWork.CompleteAsync();

        await UpdateDocumentProducts(document.Id, documentRequestDto.Products, userFirmId.Value);
        if (documentRequestDto.DocumentSeries != null)
            await IncreaseDocumentSeriesNumber(documentRequestDto.DocumentSeries.Id);

        await _unitOfWork.CompleteAsync();
        return documentRequestDto;
    }

    private async Task IncreaseDocumentSeriesNumber(int documentSeriesId)
    {
        var docSeries = await _unitOfWork.DocumentSeries.GetByIdAsync(documentSeriesId);
        docSeries!.CurrentNumber++;
        await _unitOfWork.DocumentSeries.UpdateAsync(docSeries);
    }

    public async Task<DocumentRequestDto> EditDocument(DocumentRequestDto documentRequestDto)
    {
        var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
        if (!userFirmId.HasValue)
        {
            throw new UserHasNoAssociatedFirmException();
        }

        var document = await _unitOfWork.Documents.GetByIdAsync(documentRequestDto.Id);

        if (document == null)
        {
            throw new Exception("Document not found.");
        }

        document.IssueDate = documentRequestDto.IssueDate;
        document.DueDate = documentRequestDto.DueDate;
        document.DocumentTypeId = documentRequestDto.DocumentType?.Id;
        document.DocumentStatusId = documentRequestDto.DocumentStatus?.Id;
        document.ClientId = documentRequestDto.Client.Id;
        document.UserFirmId = userFirmId;

        await _unitOfWork.Documents.UpdateAsync(document);

        await UpdateDocumentProducts(document.Id, documentRequestDto.Products, userFirmId.Value);

        await _unitOfWork.CompleteAsync();
        return documentRequestDto;
    }

    public async Task<DocumentRequestDto> GeneratePdfDocument(DocumentRequestDto documentRequestDto)
    {
        var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
        if (activeUserFirm is null)
            throw new UserHasNoAssociatedFirmException();

        documentRequestDto.Seller = _mapper.Map<FirmDto>(activeUserFirm.Firm);

        //include invoice document class and generate pdf
        _pdfGenerationService.GenerateInvoicePdf(documentRequestDto);

        return documentRequestDto;
    }

    public async Task<DocumentStreamDto> GetInvoicePdfStream(DocumentRequestDto documentRequestDto)
    {
        var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
        if (activeUserFirm is null)
            throw new UserHasNoAssociatedFirmException();

        var documentBankAccount = await _unitOfWork.Documents.Query()
            .Where(d => d.UserFirmId == activeUserFirm.UserFirmId)
            .Select(d => d.BankAccount)
            .FirstOrDefaultAsync();

        documentRequestDto.Seller = _mapper.Map<FirmDto>(activeUserFirm.Firm);
        documentRequestDto.BankAccount = _mapper.Map<BankAccountDto>(documentBankAccount);

        var pdfContent = _pdfGenerationService.GetInvoicePdfStream(documentRequestDto);

        return new DocumentStreamDto
        {
            DocumentNumber = documentRequestDto.DocumentNumber ??
                             documentRequestDto.DocumentSeries!.CurrentNumber.ToString(),
            PdfContent = pdfContent
        };
    }

    public async Task<DocumentAutofillDto> GetDocumentAutofillInfo(int documentTypeId)
    {
        var userId = _userService.GetCurrentUserId();
        var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(userId);
        if (!userFirmId.HasValue) return new DocumentAutofillDto();

        var clients = await _unitOfWork.Firms.Query()
            .Where(f => f.UserFirms!.Any(uf => uf.UserId == userId && uf.IsClient))
            .ToListAsync();
        var documentSeries = await _unitOfWork.DocumentSeries.Query()
            .Where(ds => ds.UserFirmId == userFirmId && ds.DocumentTypeId == documentTypeId)
            .Include(ds => ds.DocumentType)
            .ToListAsync();
        var documentStatuses = await _unitOfWork.DocumentStatuses.Query().ToListAsync();
        var products = await _unitOfWork.Products.Query()
            .Where(p => p.UserFirmId == userFirmId)
            .ToListAsync();

        var dto = new DocumentAutofillDto
        {
            Clients = _mapper.Map<List<FirmDto>>(clients),
            DocumentSeries = _mapper.Map<List<DocumentSeriesDto>>(documentSeries),
            DocumentStatuses = _mapper.Map<List<DocumentStatusDto>>(documentStatuses),
            Products = _mapper.Map<List<ProductDto>>(products)
        };

        return dto;
    }

    public async Task<List<DocumentTableRecordDto>> GetDocumentTableRecords(int documentTypeId)
    {
        var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
        if (activeUserFirm is null)
            return new List<DocumentTableRecordDto>();

        var documents = await _unitOfWork.Documents.GetAllDocumentsByType(activeUserFirm.UserFirmId, documentTypeId);
        return _mapper.Map<List<DocumentTableRecordDto>>(documents);
    }

    public async Task<DocumentRequestDto> GetDocumentById(int documentId)
    {
        var document = await _unitOfWork.Documents.GetDocumentWithAllInfo(documentId);
        return _mapper.Map<DocumentRequestDto>(document);
    }

    public async Task DeleteDocuments(int[] documentIds)
    {
        var documents = await _unitOfWork.Documents.Query()
            .Include(dp => dp.DocumentProducts)
            .Where(d => documentIds.Contains(d.Id))
            .ToListAsync();

        await _unitOfWork.DocumentProducts.RemoveRangeAsync(documents.SelectMany(d => d.DocumentProducts!));
        await _unitOfWork.Documents.RemoveRangeAsync(documents);

        await _unitOfWork.CompleteAsync();
    }

    public async Task<DashboardStatsDto> GetDashboardStats(int year, int documentType)
    {
        var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
        if (activeUserFirm is null)
            return new DashboardStatsDto();

        var totalDocumentsTask = await GetTotalDocumentsAsync(activeUserFirm.UserFirmId, year, documentType);
        var totalClientsTask = await _unitOfWork.Firms.GetTotalClientsAsync(activeUserFirm.UserId);
        var totalProductsTask = await _unitOfWork.Products.GetTotalProductsAsync(activeUserFirm.UserFirmId);
        var totalBankAccountsTask = await _unitOfWork.BankAccounts.GetTotalBankAccountsAsync(activeUserFirm.UserFirmId);
        var monthlyTotalsTask = await GetMonthlyTotalsAsync(activeUserFirm.UserFirmId, year, documentType);

        return new DashboardStatsDto
        {
            TotalDocuments = totalDocumentsTask,
            TotalClients = totalClientsTask,
            TotalProducts = totalProductsTask,
            TotalBankAccounts = totalBankAccountsTask,
            MonthlyTotals = monthlyTotalsTask
        };
    }

    private async Task<List<MonthlyTotalDto>> GetMonthlyTotalsAsync(int userFirmId, int year, int documentType)
    {
        return await _unitOfWork.Documents.Query()
            .Where(d => d.UserFirmId == userFirmId && d.IssueDate.Year == year && d.DocumentType!.Id == documentType)
            .GroupBy(d => new { month = d.IssueDate.Month })
            .Select(group => new MonthlyTotalDto
            {
                Month = group.Key.month,
                InvoiceAmount = group.Sum(d => d.TotalPrice),
                IncomeAmount = group.Sum(d => d.DocumentStatusId == (int)DocumentStatusEnum.Paid ? d.TotalPrice : 0)
            })
            .OrderBy(x => x.Month)
            .ToListAsync();
    }

    public async Task<int> GetTotalDocumentsAsync(int userFirmId, int year, int documentType)
    {
        return await _unitOfWork.Documents.Query()
            .Where(d => d.UserFirmId == userFirmId && d.IssueDate.Year == year && d.DocumentType!.Id == documentType)
            .CountAsync();
    }

    public async Task TransformToStorno(int[] documentIds)
    {
        var activeUserFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
        if (activeUserFirmId == null)
            throw new Exception("User firm not found.");

        foreach (var documentId in documentIds)
        {
            var document = await _unitOfWork.Documents.Query()
                .Where(d => d.Id == documentId && d.UserFirmId == activeUserFirmId)
                .FirstOrDefaultAsync();

            if (document == null)
                throw new Exception("Document not found.");

            document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice;
            await _unitOfWork.Documents.UpdateAsync(document);
            await _unitOfWork.CompleteAsync();
        }
    }
}