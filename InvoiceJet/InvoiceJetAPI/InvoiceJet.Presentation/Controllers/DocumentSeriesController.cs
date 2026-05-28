using InvoiceJet.Application.DTOs;
using InvoiceJet.Application.Services;
using InvoiceJet.Application.Services.Impl;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace InvoiceJet.Presentation.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize(Roles = "User")]
public class DocumentSeriesController : ControllerBase
{
    private readonly IDocumentSeriesService _documentSeriesService;

    public DocumentSeriesController(IDocumentSeriesService documentSeriesService)
    {
        _documentSeriesService = documentSeriesService;
    }

    [HttpGet("GetAllDocumentSeriesForUserId")]
    public async Task<ActionResult<DocumentSeriesDto>> GetAllDocumentSeriesForUserId()
    {
        var bankAccountDto = await _documentSeriesService.GetAllDocumentSeriesForUserId();
        return Ok(bankAccountDto);
    }

    [HttpPost("AddDocumentSeries")]
    public async Task<ActionResult> AddDocumentSeries([FromBody] DocumentSeriesDto documentSeriesDto)
    {
        try
        {
            await _documentSeriesService.AddDocumentSeries(documentSeriesDto);
            return Ok();
        }
        catch (Exception ex)
        {
            return BadRequest(ex.Message);
        }
    }

    [HttpPut("UpdateDocumentSeries")]
    public async Task<ActionResult> UpdateDocumentSeries([FromBody] DocumentSeriesDto documentSeriesDto)
    {
        await _documentSeriesService.UpdateDocumentSeries(documentSeriesDto);
        return Ok();
    }

    [HttpPut("DeleteDocumentSeries")]
    public async Task<ActionResult> DeleteDocumentSeries(int[] documentSeriesIds)
    {
        await _documentSeriesService.DeleteDocumentSeries(documentSeriesIds);
        return Ok();
    }
}