using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InvoiceJet.Domain.Exceptions
{
    public class NoBankAccountAddedException : Exception
    {
        public NoBankAccountAddedException() : base($"Please add a bank account, before generating a document.")
        {
        }
    }
}
