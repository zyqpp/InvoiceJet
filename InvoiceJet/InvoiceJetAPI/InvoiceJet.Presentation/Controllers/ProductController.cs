using InvoiceJet.Application.DTOs;
using InvoiceJet.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace InvoiceJet.Presentation.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize(Roles = "User")]
public class ProductController : ControllerBase
{
    private readonly IProductService _productService;

    public ProductController(IProductService productService)
    {
        _productService = productService;
    }

    [HttpGet("GetAllProductsForUserId")]
    public async Task<ActionResult<ICollection<ProductDto>>> GetAllProductsForUserId()
    {
        var productsDto = await _productService.GetUserFirmProducts();
        return Ok(productsDto);
    }

    [HttpPost("AddProduct")]
    public async Task<ActionResult<ProductDto>> AddProduct(ProductDto product)
    {
        var productDto = await _productService.AddProduct(product);
        return Ok(productDto);
    }

    [HttpPut("EditProduct")]
    public async Task<ActionResult<ProductDto>> EditProduct(ProductDto product)
    {
        var productDto = await _productService.EditProduct(product);
        return Ok(productDto);
    }

    [HttpPut("DeleteProducts")]
    public async Task<ActionResult<ProductDto>> DeleteProducts(int[] productIds)
    {
        await _productService.DeleteProducts(productIds);
        return Ok();
    }
}