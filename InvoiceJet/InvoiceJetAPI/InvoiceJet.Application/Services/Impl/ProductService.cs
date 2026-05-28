using AutoMapper;
using InvoiceJet.Application.DTOs;
using InvoiceJet.Domain.Exceptions;
using InvoiceJet.Domain.Interfaces;
using InvoiceJet.Domain.Models;
using Microsoft.EntityFrameworkCore;

namespace InvoiceJet.Application.Services.Impl;

public class ProductService : IProductService
{
    private readonly IUnitOfWork _unitOfWork;
    private readonly IMapper _mapper;
    private readonly IUserService _userService;

    public ProductService(IMapper mapper, IUnitOfWork unitOfWork, IUserService userService)
    {
        _mapper = mapper;
        _unitOfWork = unitOfWork;
        _userService = userService;
    }

    public async Task<ICollection<ProductDto>> GetUserFirmProducts()
    {
        var products = await _unitOfWork.Products.GetUserFirmProductsAsync(_userService.GetCurrentUserId());
        if (products.Count == 0)
        {
            return new List<ProductDto>();
        }

        var productDtos = _mapper.Map<ICollection<ProductDto>>(products);
        return productDtos;
    }

    public async Task<ProductDto> AddProduct(ProductDto productDto)
    {
        var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
        if(!userFirmId.HasValue)
        {
            throw new UserHasNoAssociatedFirmException();
        }
        
        var productWithSameName = await _unitOfWork.Products.FindUserFirmProductByName(_userService.GetCurrentUserId(), productDto.Name);
        if (productWithSameName != null)
        {
            throw new ProductWithSameNameExistsException(productDto.Name);
        }

        var product = _mapper.Map<Product>(productDto);
        product.UserFirmId = userFirmId.Value;

        await _unitOfWork.Products.AddAsync(product);
        await _unitOfWork.CompleteAsync();

        return _mapper.Map<ProductDto>(product);
    }

    public async Task<ProductDto> EditProduct(ProductDto productDto)
    {
        var product = await _unitOfWork.Products.GetByIdAsync(productDto.Id) ??
                      throw new Exception("Product not found.");

        _mapper.Map(productDto, product);
        await _unitOfWork.CompleteAsync();

        return _mapper.Map<ProductDto>(product);
    }

    public async Task DeleteProducts(int[] productIds)
    {
        foreach (var productId in productIds)
        {
            var product = await _unitOfWork.Products.GetByIdAsync(productId) ??
                              throw new Exception("Product not found.");

            bool isAssociatedWithDocumentProduct = await _unitOfWork.DocumentProducts.Query()
                .AnyAsync(dp => dp.ProductId == productId);

            if (isAssociatedWithDocumentProduct)
            {
                throw new ProductAssociatedWithInvoiceException(product.Name);
            }

            await _unitOfWork.Products.RemoveAsync(product);
        }

        await _unitOfWork.CompleteAsync();
    }
}