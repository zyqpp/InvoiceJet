using System.Net.Http.Json;
using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Exceptions;
using InvoiceJet.Domain.Interfaces;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Newtonsoft.Json.Linq;

namespace InvoiceJet.Application.Services.Impl;

public class FirmService : IFirmService
{
    private readonly HttpClient _httpClient;
    private readonly IMapper _mapper;
    private readonly string _apiUrl;
    private readonly IUnitOfWork _unitOfWork;
    private readonly IUserService _userService;
    private readonly IDocumentSeriesService _documentSeriesService;

    public FirmService(IConfiguration config, IMapper mapper, IUnitOfWork unitOfWork, IUserService userService, IDocumentSeriesService documentSeriesService)
    {
        _httpClient = new HttpClient();
        _mapper = mapper;
        _unitOfWork = unitOfWork;
        _userService = userService;
        _documentSeriesService = documentSeriesService;
        _apiUrl = config.GetSection("AppSettings")?["AnafApiUrl"] ??
                  throw new ArgumentNullException("AnafApiUrl is not configured");
    }

    public async Task<FirmDto> AddFirm(FirmDto firmDto, bool isClient)
    {
        var firm = _mapper.Map<Firm>(firmDto);
        await _unitOfWork.Firms.AddAsync(firm);
        await _unitOfWork.CompleteAsync();
    
        await ManageUserFirmRelation(firm.Id, isClient);

        firmDto.Id = firm.Id;
        return firmDto;
    }
    
    public async Task<FirmDto> EditFirm(FirmDto firmDto, bool isClient)
    {
        var firm = await _unitOfWork.Firms.GetByIdAsync(firmDto.Id);
        if (firm == null)
        {
            throw new Exception("Firm not found.");
        }

        firm = _mapper.Map(firmDto, firm);
        await _unitOfWork.CompleteAsync();

        await ManageUserFirmRelation(firm.Id, isClient);
        
        return firmDto;
    }
    
    private async Task ManageUserFirmRelation(int firmId, bool isClient)
    {
        var userId = _userService.GetCurrentUserId();
        var existingUserFirm = await _unitOfWork.UserFirms.GetUserFirmById(userId, firmId);
        
        if (existingUserFirm == null)
        {
            var newUserFirm = new UserFirm
            {
                UserId = userId,
                FirmId = firmId,
                IsClient = isClient
            };

            await _unitOfWork.UserFirms.AddAsync(newUserFirm);

            var user = await _unitOfWork.Users.GetUserByIdAsync(_userService.GetCurrentUserId());
            if (user!.ActiveUserFirm == null)
            {
                user.ActiveUserFirm = newUserFirm;
                await _documentSeriesService.AddInitialDocumentSeries(newUserFirm);
            }
        }
        else
        {
            existingUserFirm.IsClient = isClient;
        }
        
        await _unitOfWork.CompleteAsync();
    }
    
    public async Task<FirmDto> GetUserActiveFirm()
    {
        var activeUserFirm = await _unitOfWork.Users.GetUserFirmAsync(_userService.GetCurrentUserId());
        return activeUserFirm == null ? new FirmDto() : _mapper.Map<FirmDto>(activeUserFirm.Firm);
    }
    
    public async Task<List<FirmDto>> GetUserClientFirms()
    {
        var clients = await _unitOfWork.UserFirms.GetUserFirmClients(_userService.GetCurrentUserId());
        if (clients.Count == 0)
        {
            return new List<FirmDto>();
        }

        var firms = clients.Select(u => u.Firm).ToList();
        return _mapper.Map<List<FirmDto>>(firms);
    }

    public async Task DeleteFirms(int[] firmIds)
    {
        foreach (var firmId in firmIds)
        {
            var firm = await _unitOfWork.Firms.GetByIdAsync(firmId) ??
                          throw new Exception("Product not found.");

            bool isAssociatedWithDocuments = await _unitOfWork.Documents.Query()
                .AnyAsync(d => d.ClientId == firmId);
            
            if (isAssociatedWithDocuments)
            {
                throw new FirmAssociatedWithDocumentException(firm.Name);
            }
            
            await _unitOfWork.Firms.RemoveAsync(firm);
        }

        await _unitOfWork.CompleteAsync();
    }

    public async Task<FirmDto> GetFirmDataFromAnaf(string cui)
    {
        var firmDto = new FirmDto();
        var currentDate = DateTime.Now.ToString("yyyy-MM-dd");
        try
        {
            var requestBody = new[]
            {
                new
                {
                    cui,
                    data = currentDate
                }
            };

            var response = await _httpClient.PostAsJsonAsync(_apiUrl, requestBody);

            if (!response.IsSuccessStatusCode)
                throw new AnafFirmNotFoundException(cui);

            var responseString = await response.Content.ReadAsStringAsync();
            var json = JObject.Parse(responseString);

            var dateGenerale = json["found"]?[0]?["date_generale"];
            if (dateGenerale != null)
            {
                string? name = dateGenerale["denumire"]?.ToString();
                string? cuiValue = dateGenerale["cui"]?.ToString();
                string? regCom = dateGenerale["nrRegCom"]?.ToString();
                string? address = dateGenerale["adresa"]?.ToString();

                string[] addressPrefixes = { "STR.", "ŞOS.", "BLD.", "CAL." };
                if (address != null)
                {
                    foreach (var prefix in addressPrefixes)
                    {
                        var startIndex = address.IndexOf(prefix, StringComparison.Ordinal);
                        if (startIndex != -1)
                            firmDto.Address = address.Substring(startIndex);
                    }

                    if (name != null && cuiValue != null && regCom != null)
                    {
                        firmDto.Name = name;
                        firmDto.RegCom = regCom;
                        firmDto.Cui = cuiValue;
                    }
                }
            }

            var adrDomiciliuFiscal = json["found"]?[0]?["adresa_domiciliu_fiscal"];
            if (adrDomiciliuFiscal == null) return firmDto;

            var county = adrDomiciliuFiscal["ddenumire_Judet"]?.ToString();
            var city = adrDomiciliuFiscal["ddenumire_Localitate"]?.ToString();

            if (county == null || city == null) return firmDto;
            firmDto.County = county;
            firmDto.City = city;

            return firmDto;
        }
        catch (Exception)
        {
            throw new AnafFirmNotFoundException(cui);
        }
    }
}