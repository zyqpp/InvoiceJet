using InvoiceJet.Application.DTOs;
using InvoiceJet.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace InvoiceJet.Presentation.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize(Roles = "User")]
public class FirmController : ControllerBase
{
    private readonly IFirmService _firmService;

    public FirmController(IFirmService firmService)
    {
        _firmService = firmService;
    }

    [HttpGet("fromAnaf/{cui}")]
    public async Task<ActionResult<FirmDto>> GetFirmDataFromAnaf(string cui)
    {
        var firmDataDto = await _firmService.GetFirmDataFromAnaf(cui);
        return Ok(firmDataDto);
    }
    
    [HttpPost("AddFirm/{isClient}")]
    public async Task<ActionResult> AddFirm([FromBody] FirmDto firmDto, bool isClient)
    {
        var updatedOrNewFirm = await _firmService.AddFirm(firmDto, isClient);
        return Ok(updatedOrNewFirm);
    }
    
    [HttpPut("EditFirm/{isClient}")]
    public async Task<ActionResult> EditFirm([FromBody] FirmDto firmDto, bool isClient)
    {
        var updatedOrNewFirm = await _firmService.EditFirm(firmDto, isClient);
        return Ok(updatedOrNewFirm);
    }

    [HttpGet("GetUserActiveFirm")]
    public async Task<ActionResult> GetUserActiveFirm()
    {
        var firm = await _firmService.GetUserActiveFirm();
        return Ok(firm);
    }

    [HttpGet("GetUserClientFirms")]
    public async Task<ActionResult> GetUserClientFirms()
    {
        var clientFirms = await _firmService.GetUserClientFirms();
        return Ok(clientFirms);
    }
    
    [HttpPut("DeleteFirms")]
    public async Task<ActionResult> DeleteFirms(int[] firmIds)
    {
        await _firmService.DeleteFirms(firmIds);
        return Ok();
    }
}