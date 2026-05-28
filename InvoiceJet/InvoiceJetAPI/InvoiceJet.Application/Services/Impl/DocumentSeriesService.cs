using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Exceptions;
using InvoiceJet.Domain.Interfaces;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Application.Services.Impl;

public class DocumentSeriesService : IDocumentSeriesService
{
    private readonly IUnitOfWork _unitOfWork;
    private readonly IMapper _mapper;
    private readonly IUserService _userService;

    public DocumentSeriesService(IMapper mapper, IUnitOfWork unitOfWork, IUserService userService)
    {
        _mapper = mapper;
        _unitOfWork = unitOfWork;
        _userService = userService;
    }

    public async Task<List<DocumentSeriesDto>> GetAllDocumentSeriesForUserId()
    {
        var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
        if (!userFirmId.HasValue)
        {
            return new List<DocumentSeriesDto>();
        }

        var documentSeries = await _unitOfWork.DocumentSeries.GetAllDocumentSeriesForActiveUserFirm(_userService.GetCurrentUserId());
        return _mapper.Map<List<DocumentSeries>, List<DocumentSeriesDto>>(documentSeries);
    }

    public async Task AddDocumentSeries(DocumentSeriesDto documentSeriesDto)
    {
        var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
        if (!userFirmId.HasValue)
        {
            throw new UserHasNoAssociatedFirmException();
        }

        var documentSeries = _mapper.Map<DocumentSeries>(documentSeriesDto);
        documentSeries.UserFirmId = userFirmId.Value;
        documentSeries.DocumentTypeId = documentSeriesDto.DocumentType!.Id; // Set the DocumentTypeId

        await _unitOfWork.DocumentSeries.AddAsync(documentSeries);
        await _unitOfWork.CompleteAsync();
    }

    public async Task UpdateDocumentSeries(DocumentSeriesDto documentSeriesDto)
    {
        var documentSeries = await _unitOfWork.DocumentSeries.Query()
            .FirstOrDefaultAsync(ds => ds.Id == documentSeriesDto.Id);

        if (documentSeries == null)
        {
            throw new Exception("Document Series not found");
        }

        _mapper.Map(documentSeriesDto, documentSeries);
        documentSeries.DocumentTypeId = documentSeriesDto.DocumentType!.Id;

        await _unitOfWork.DocumentSeries.UpdateAsync(documentSeries);
        await _unitOfWork.CompleteAsync();
    }

    public async Task DeleteDocumentSeries(int[] documentSeriesIds)
    {
        var documentSeries = await _unitOfWork.DocumentSeries.Query()
           .Where(d => documentSeriesIds.Contains(d.Id))
           .ToListAsync();

        await _unitOfWork.DocumentSeries.RemoveRangeAsync(documentSeries);
        await _unitOfWork.CompleteAsync();
    }

    public async Task AddInitialDocumentSeries(UserFirm userFirm)
    {
        var documentSeries = new List<DocumentSeries>
        {
            new()
            {
                SeriesName = DateTime.Now.Year.ToString(),
                FirstNumber = 1,
                CurrentNumber = 1,
                IsDefault = true,
                DocumentType = await _unitOfWork.DocumentTypes.Query()
                    .Where(d => d.Name.Equals("Factura"))
                    .FirstOrDefaultAsync(),
                UserFirm = userFirm
            },
            new()
            {
                SeriesName = DateTime.Now.Year.ToString(),
                FirstNumber = 1,
                CurrentNumber = 1,
                IsDefault = true,
                DocumentType = await _unitOfWork.DocumentTypes.Query()
                    .Where(d => d.Name.Equals("Factura Storno"))
                    .FirstOrDefaultAsync(),
                UserFirm = userFirm
            },
            new()
            {
                SeriesName = DateTime.Now.Year.ToString(),
                FirstNumber = 1,
                CurrentNumber = 1,
                IsDefault = true,
                DocumentType = await _unitOfWork.DocumentTypes.Query()
                    .Where(d => d.Name.Equals("Factura Proforma"))
                    .FirstOrDefaultAsync(),
                UserFirm = userFirm
            },
        };

        await _unitOfWork.DocumentSeries.AddRangeAsync(documentSeries);
        await _unitOfWork.CompleteAsync();
    }
}