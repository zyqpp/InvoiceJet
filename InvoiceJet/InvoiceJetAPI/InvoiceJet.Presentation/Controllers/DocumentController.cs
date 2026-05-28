using InvoiceJet.Application.DTOs;
using InvoiceJet.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace InvoiceJet.Presentation.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize(Roles = "User")]
public class DocumentController : ControllerBase
{
    private readonly IDocumentService _documentService;

    public DocumentController(IDocumentService documentService)
    {
        _documentService = documentService;
    }

    [HttpGet("GetDocumentAutofillInfo/{documentTypeId}")]
    public async Task<ActionResult<DocumentAutofillDto>> GetDocumentAutofillInfo(int documentTypeId)
    {
        var documentAutofillDto = await _documentService.GetDocumentAutofillInfo(documentTypeId);
        return Ok(documentAutofillDto);
    }

    [HttpPost("AddDocument")]
    public async Task<ActionResult<DocumentRequestDto>> AddDocument(DocumentRequestDto documentRequestDto)
    {
        await _documentService.AddDocument(documentRequestDto);
        return Ok(documentRequestDto);
    }

    [HttpPut("EditDocument")]
    public async Task<ActionResult<DocumentRequestDto>> EditDocument(DocumentRequestDto documentRequestDto)
    {
        await _documentService.EditDocument(documentRequestDto);
        return Ok(documentRequestDto);

    }

    [HttpPost("GenerateDocumentPdf")]
    public async Task<ActionResult<DocumentRequestDto>> GenerateDocument(DocumentRequestDto documentRequestDTO)
    {
        try
        {
            await _documentService.GeneratePdfDocument(documentRequestDTO);
            return Ok();
        }
        catch (Exception ex)
        {
            return BadRequest(ex.Message);
        }
    }

    [HttpPost("GetInvoicePdfStream")]
    public async Task<IActionResult> GetInvoicePdfStream(DocumentRequestDto documentRequestDto)
    {
        var documentStreamDto = await _documentService.GetInvoicePdfStream(documentRequestDto);
        if (documentStreamDto.PdfContent == null)
        {
            return BadRequest("Failed to generate the PDF document.");
        }

        return File(documentStreamDto.PdfContent, "application/pdf",
            $"Invoice_{documentStreamDto.DocumentNumber}.pdf");
    }

    [HttpGet("GetDocumentTableRecords/{documentTypeId}")]
    public async Task<IActionResult> GetDocumentTableRecords(int documentTypeId)
    {
        var documents = await _documentService.GetDocumentTableRecords(documentTypeId);
        return Ok(documents);
    }

    [HttpGet("GetDocumentById/{documentId}")]
    public async Task<IActionResult> GetDocumentById(int documentId)
    {
        var document = await _documentService.GetDocumentById(documentId);
        return Ok(document);
    }

    [HttpPut("DeleteDocuments")]
    public async Task<IActionResult> DeleteDocuments([FromBody] int[] documentIds)
    {
        await _documentService.DeleteDocuments(documentIds);
        return Ok(new { Message = "Documents deleted successfully." });
    }

    [HttpGet("GetDashboardStats/{year}/{documentType}")]
    public async Task<IActionResult> GetDashboardStats(int year, int documentType)
    {
        var dashboardStats = await _documentService.GetDashboardStats(year, documentType);
        return Ok(dashboardStats);
    }

    [HttpPut("TransformToStorno")]
    public async Task<IActionResult> TransformToStorno([FromBody] int[] documentIds)
    {
        await _documentService.TransformToStorno(documentIds);
        return Ok();
    }
}