using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Exceptions;
using InvoiceJet.Domain.Interfaces;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Application.Services.Impl;

public class BankAccountService : IBankAccountService
{
    private readonly IUnitOfWork _unitOfWork;
    private readonly IMapper _mapper;
    private readonly IUserService _userService;

    public BankAccountService(IMapper mapper, IUnitOfWork unitOfWork, IUserService userService)
    {
        _mapper = mapper;
        _unitOfWork = unitOfWork;
        _userService = userService;
    }

    public async Task<ICollection<BankAccountDto>> GetUserFirmBankAccounts()
    {
        var bankAccounts = await _unitOfWork.BankAccounts.GetUserFirmBankAccountsAsync(_userService.GetCurrentUserId());
        if (bankAccounts.Count == 0)
        {
            return new List<BankAccountDto>();
        }

        var bankAccountDtos = _mapper.Map<List<BankAccountDto>>(bankAccounts);
        return bankAccountDtos;
    }

    public async Task<BankAccountDto> AddUserFirmBankAccount(BankAccountDto bankAccountDto)
    {
        var bankAccount = _mapper.Map<BankAccount>(bankAccountDto);
        
        var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
        if (!userFirmId.HasValue)
        {
            throw new UserHasNoAssociatedFirmException();
        }
        bankAccount.UserFirmId = userFirmId.Value;

        if (bankAccount.IsActive)
        {
            await DeactivateOtherBankAccounts(bankAccount.UserFirmId);
        }

        await _unitOfWork.BankAccounts.AddAsync(bankAccount);
        await _unitOfWork.CompleteAsync();

        return _mapper.Map<BankAccountDto>(bankAccount);
    }

    public async Task<BankAccountDto> EditUserFirmBankAccount(BankAccountDto bankAccountDto)
    {
        var bankAccount = await _unitOfWork.BankAccounts.GetByIdAsync(bankAccountDto.Id) ?? throw new Exception("Bank account not found.");
        _mapper.Map(bankAccountDto, bankAccount);

        if (bankAccount.IsActive)
        {
            await DeactivateOtherBankAccounts(bankAccount.UserFirmId, bankAccount.Id);
        }

        await _unitOfWork.CompleteAsync();
        return _mapper.Map<BankAccountDto>(bankAccount);
    }

    public async Task DeleteUserFirmBankAccounts(int[] bankAccountIds)
    {
        foreach (var bankAccountId in bankAccountIds)
        {
            var bankAccount = await _unitOfWork.BankAccounts.GetByIdAsync(bankAccountId) ?? throw new Exception("Bank account not found.");

            bool isAssociatedWithDocuments = await _unitOfWork.Documents.Query()
               .AnyAsync(d => d.BankAccountId == bankAccountId);

            if (isAssociatedWithDocuments)
            {
                throw new BankAccountAssociatedWithDocumentsException($"Can't delete. Bank account is associated with documents.");
            }

            await _unitOfWork.BankAccounts.RemoveAsync(bankAccount);
        }
        await _unitOfWork.CompleteAsync();
    }

    public async Task DeactivateOtherBankAccounts(int userFirmId, int? excludeAccountId = null)
    {
        var otherAccounts = await _unitOfWork.BankAccounts.Query()
            .Where(ba => ba.UserFirmId == userFirmId && ba.Id != excludeAccountId)
            .ToListAsync();

        foreach (var account in otherAccounts)
        {
            account.IsActive = false;
            await _unitOfWork.BankAccounts.UpdateAsync(account);
        }
    }
}