using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.Filters;
using System.Text;
using InvoiceJet.Application.Services;
using InvoiceJet.Application.Services.Impl;
using InvoiceJet.Domain.Interfaces;
using InvoiceJet.Domain.Interfaces.Repositories;
using InvoiceJet.Infrastructure.Factories;
using InvoiceJet.Infrastructure.Factories.Impl;
using InvoiceJet.Infrastructure.Persistence;
using InvoiceJet.Infrastructure.Persistence.Repositories;
using InvoiceJet.Infrastructure.Services;
using InvoiceJet.Presentation.Middleware;
using InvoiceJet.Presentation.Seeders;
using QuestPDF.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddDbContext<InvoiceJetDbContext>(options =>
{
    options.UseSqlServer(builder.Configuration.GetConnectionString("ProdConnection"));
});

QuestPDF.Settings.License = LicenseType.Community;
builder.Services.AddHttpContextAccessor();

//repositories
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
builder.Services.AddScoped(typeof(IGenericRepository<>), typeof(GenericRepository<>));

//services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IFirmService, FirmService>();
builder.Services.AddScoped<IBankAccountService, BankAccountService>();
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<IDocumentSeriesService, DocumentSeriesService>();
builder.Services.AddScoped<IDocumentService, DocumentService>();
builder.Services.AddScoped<IPdfGenerationService, PdfGenerationService>();

//factories
// builder.Services.AddSingleton<IDocumentFactory, InvoiceDocumentFactory>();
// builder.Services.AddSingleton<IDocumentFactory, ProformaDocumentFactory>();
// builder.Services.AddSingleton<DocumentFactoryProvider>();

builder.Services.AddAutoMapper(AppDomain.CurrentDomain.GetAssemblies());
builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.AddSecurityDefinition("oauth2", new OpenApiSecurityScheme
    {
        Description = "Standard Authorization header using the Bearer scheme (\"bearer {token}\")",
        In = ParameterLocation.Header,
        Name = "Authorization",
        Type = SecuritySchemeType.ApiKey
    });

    options.OperationFilter<SecurityRequirementsOperationFilter>();
});
builder.Services.AddAuthentication(
    JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8
            .GetBytes(builder.Configuration.GetSection("AppSettings:Token").Value!)),
            ValidateIssuer = false,
            ValidateAudience = false,
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };
        options.MapInboundClaims = false;
    });

builder.Services.AddCors(options => options.AddPolicy(name: "NgOrigins", 
    policy =>
    {
        policy.WithOrigins("http://localhost:4200", "https://localhost:4200").AllowAnyMethod().AllowAnyHeader();
    }));

var app = builder.Build();

app.UseMiddleware<ExceptionMiddleware>();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

await DbSeeder.SeedDocumentTypes(app);

app.UseCors("NgOrigins");

app.UseHttpsRedirection();

app.UseAuthentication();

app.UseAuthorization();

app.MapControllers();

app.Run();
