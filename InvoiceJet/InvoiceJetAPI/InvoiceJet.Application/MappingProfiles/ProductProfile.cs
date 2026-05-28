using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Models;

public class ProductProfile : Profile
{
    public ProductProfile()
    {
        CreateMap<Product, ProductDto>().ReverseMap();
    }
}
