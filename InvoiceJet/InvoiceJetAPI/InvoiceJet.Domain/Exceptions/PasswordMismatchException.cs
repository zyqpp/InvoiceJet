using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InvoiceJet.Domain.Exceptions
{
    public class PasswordMismatchException : Exception
    {
        public PasswordMismatchException()
            : base($"Password confirmation doesn't match.")
        {
        }
    }
}
