using InvoiceJet.Application.DTOs;
using InvoiceJet.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace InvoiceJet.Presentation.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize(Roles = "User")]
public class BankAccountController : ControllerBase
{
    private readonly IBankAccountService _bankAccountService;

    public BankAccountController(IBankAccountService bankAccountService)
    {
        _bankAccountService = bankAccountService;
    }

    [HttpGet("GetUserFirmBankAccounts")]
    public async Task<ActionResult<BankAccountDto>> GetUserFirmBankAccounts()
    {
        var bankAccountDto = await _bankAccountService.GetUserFirmBankAccounts();
        return Ok(bankAccountDto);
    }

    [HttpPost("AddUserFirmBankAccount")]
    public async Task<ActionResult<BankAccountDto>> AddUserFirmBankAccount([FromBody] BankAccountDto bankAccountDto)
    {
        var bankAccount = await _bankAccountService.AddUserFirmBankAccount(bankAccountDto);
        return Ok(bankAccount);
    }

    [HttpPut("EditUserFirmBankAccount")]
    public async Task<ActionResult<BankAccountDto>> EditUserFirmBankAccount([FromBody] BankAccountDto bankAccountDto)
    {
        var bankAccount = await _bankAccountService.EditUserFirmBankAccount(bankAccountDto);
        return Ok(bankAccount);
    }

    [HttpPut("DeleteUserFirmBankAccounts")]
    public async Task<ActionResult<BankAccountDto>> DeleteUserFirmBankAccounts([FromBody] int[] bankAccountIds)
    {
        await _bankAccountService.DeleteUserFirmBankAccounts(bankAccountIds);
        return Ok();
    }
}