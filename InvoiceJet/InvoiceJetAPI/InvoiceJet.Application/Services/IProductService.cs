using InvoiceJet.Application.DTOs;

namespace InvoiceJet.Application.Services;

public interface IProductService
{
    Task<ICollection<ProductDto>> GetUserFirmProducts();
    Task<ProductDto> AddProduct(ProductDto productDto);
    Task<ProductDto> EditProduct(ProductDto productDto);
    Task DeleteProducts(int[] productIds);
}