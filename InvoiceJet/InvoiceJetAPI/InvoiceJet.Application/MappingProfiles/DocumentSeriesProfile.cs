using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Models;

namespace InvoiceJet.Application.MappingProfiles;

public class DocumentSeriesProfile : Profile
{
    public DocumentSeriesProfile()
    {
        CreateMap<DocumentSeries, DocumentSeriesDto>();

        CreateMap<DocumentSeriesDto, DocumentSeries>().ForMember(dest => dest.DocumentTypeId, opt => opt.MapFrom(src => src.DocumentType!.Id))
                .ForMember(dest => dest.DocumentType, opt => opt.Ignore());
    }
}