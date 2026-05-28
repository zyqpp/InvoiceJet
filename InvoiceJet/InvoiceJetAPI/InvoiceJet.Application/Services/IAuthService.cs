using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Models;

namespace InvoiceJet.Application.Services;

public interface IAuthService
{
    Task<string> RegisterUser(UserRegisterDto userDto);
    Task<string> LoginUser(UserLoginDto userDto);
}