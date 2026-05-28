using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InvoiceJet.Application.DTOs
{
    public class DocumentStatusDto
    {
        public int Id { get; set; }
        public string Status { get; set; } = string.Empty;
    }
}
