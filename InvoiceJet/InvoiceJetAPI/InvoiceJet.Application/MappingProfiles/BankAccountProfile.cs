using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Models;

public class BankAccountProfile : Profile
{
    public BankAccountProfile()
    {
        CreateMap<BankAccount, BankAccountDto>().ReverseMap();
    }
}