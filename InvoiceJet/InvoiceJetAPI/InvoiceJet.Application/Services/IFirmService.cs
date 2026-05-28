using InvoiceJet.Application.DTOs;

namespace InvoiceJet.Application.Services;

public interface IFirmService
{
    Task<FirmDto> GetFirmDataFromAnaf(string cui);
    Task<FirmDto> AddFirm(FirmDto firmDto, bool isClient);
    Task<FirmDto> EditFirm(FirmDto firmDto, bool isClient);
    Task<FirmDto> GetUserActiveFirm();
    Task<List<FirmDto>> GetUserClientFirms();
    Task DeleteFirms(int[] firmIds);
}