using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using System.Text.RegularExpressions;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Exceptions;
using InvoiceJet.Domain.Interfaces;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using BC = BCrypt.Net.BCrypt;

namespace InvoiceJet.Application.Services.Impl;

public class AuthService : IAuthService
{
    private readonly IConfiguration _configuration;
    private readonly IUnitOfWork _unitOfWork;

    public AuthService(IUnitOfWork unitOfWork, IConfiguration configuration)
    {
        _unitOfWork = unitOfWork;
        _configuration = configuration;
    }

    public async Task<string> RegisterUser(UserRegisterDto userDto)
    {
        var existingUser = await _unitOfWork.Users.Query()
            .FirstOrDefaultAsync(u => u.Email == userDto.Email);

        if (existingUser != null)
        {
            throw new UserAlreadyExistsException(userDto.Email);
        }

        var passwordRules = new Regex(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$");

        if (!passwordRules.IsMatch(userDto.Password))
        {
            throw new InvalidPasswordException();
        }

        if (userDto.Password != userDto.PasswordConfirmation)
        {
            throw new PasswordMismatchException();
        }

        var user = new User
        {
            Email = userDto.Email,
            PasswordHash = BC.HashPassword(userDto.Password),
            FirstName = userDto.FirstName,
            LastName = userDto.LastName,
            Role = "User"
        };

        await _unitOfWork.Users.AddAsync(user);
        await _unitOfWork.CompleteAsync();

        string token = CreateToken(user);
        return token;
    }

    public async Task<string> LoginUser(UserLoginDto userDto)
    {
        var user = await _unitOfWork.Users.Query()
            .FirstOrDefaultAsync(u => u.Email == userDto.Email);
        if (user == null || user.Email != userDto.Email)
        {
            throw new UserNotFoundException(userDto.Email);
        }

        if (!BC.Verify(userDto.Password, user.PasswordHash))
        {
            throw new IncorrectPasswordException();
        }

        string token = CreateToken(user);
        return token;
    }

    private string CreateToken(User user)
    {
        var claims = new List<Claim>
        {
            new("userId", user.Id.ToString()),
            new("firstName", user.FirstName),
            new("lastName", user.LastName),
            new("email", user.Email),
            new(ClaimTypes.Role, "User")
        };

        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(
            _configuration.GetSection("AppSettings:Token").Value!));

        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha512Signature);

        var token = new JwtSecurityToken(
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(10),
            signingCredentials: credentials
        );

        var jwt = new JwtSecurityTokenHandler().WriteToken(token);

        return jwt;
    }
}