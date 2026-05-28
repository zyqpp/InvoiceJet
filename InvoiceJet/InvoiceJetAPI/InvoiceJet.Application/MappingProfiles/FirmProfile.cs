using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Models;

public class FirmProfile : Profile
{
    public FirmProfile()
    {
        CreateMap<Firm, FirmDto>().ReverseMap(); 
    }
}