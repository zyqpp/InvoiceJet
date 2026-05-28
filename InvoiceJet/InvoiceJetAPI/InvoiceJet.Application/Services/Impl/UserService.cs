using System.Security.Claims;
using Microsoft.AspNetCore.Http;

namespace InvoiceJet.Application.Services.Impl;

public class UserService : IUserService
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public UserService(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public Guid GetCurrentUserId()
    {
        var httpContext = _httpContextAccessor.HttpContext;
        if (httpContext.User.Identity is not { IsAuthenticated: true })
            return Guid.Empty;

        var userIdString = httpContext.User.FindFirst("userId")?.Value;
        return Guid.TryParse(userIdString, out var userId) ? userId : Guid.Empty;
    }
}