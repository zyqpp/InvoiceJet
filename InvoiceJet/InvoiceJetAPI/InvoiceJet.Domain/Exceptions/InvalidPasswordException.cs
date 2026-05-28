using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace InvoiceJet.Domain.Exceptions
{
    public class InvalidPasswordException : Exception
    {
        public InvalidPasswordException()
             : base("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
        {
        }
    }
}
