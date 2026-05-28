using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InvoiceJet.Application.MappingProfiles
{
    public class DocumentStatusProfile : Profile
    {
        public DocumentStatusProfile()
        {
            CreateMap<DocumentStatus, DocumentStatusDto>().ReverseMap();
        }
    }
}
