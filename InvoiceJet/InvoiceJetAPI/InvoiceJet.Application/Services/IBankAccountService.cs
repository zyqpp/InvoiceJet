using InvoiceJet.Application.DTOs;

namespace InvoiceJet.Application.Services;

public interface IBankAccountService
{
    Task<ICollection<BankAccountDto>> GetUserFirmBankAccounts();
    Task<BankAccountDto> AddUserFirmBankAccount(BankAccountDto bankAccountDto);
    Task<BankAccountDto> EditUserFirmBankAccount(BankAccountDto bankAccountDto);
    Task DeleteUserFirmBankAccounts(int[] bankAccountIds);
    Task DeactivateOtherBankAccounts(int userFirmId, int? excludeAccountId);
}