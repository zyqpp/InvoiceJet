using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Models;

namespace InvoiceJet.Application.MappingProfiles;

public class DocumentProductProfile : Profile
{
    public DocumentProductProfile()
    {
        CreateMap<DocumentProductRequestDto, Product>()
            .ForMember(dest => dest.Price, opt => opt.MapFrom(src => src.UnitPrice))
            .ForMember(dest => dest.UserFirm, opt => opt.Ignore())
            .ForMember(dest => dest.UserFirmId, opt => opt.Ignore());
    }
}