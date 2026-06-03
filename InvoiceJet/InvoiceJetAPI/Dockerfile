FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ["InvoiceJet.Presentation/InvoiceJet.Presentation.csproj", "InvoiceJet.Presentation/"]
COPY ["InvoiceJet.Application/InvoiceJet.Application.csproj", "InvoiceJet.Application/"]
COPY ["InvoiceJet.Domain/InvoiceJet.Domain.csproj", "InvoiceJet.Domain/"]
COPY ["InvoiceJet.Infrastructure/InvoiceJet.Infrastructure.csproj", "InvoiceJet.Infrastructure/"]
RUN dotnet restore "InvoiceJet.Presentation/InvoiceJet.Presentation.csproj"

COPY . .
RUN dotnet publish "InvoiceJet.Presentation/InvoiceJet.Presentation.csproj" -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .
EXPOSE 8080
ENTRYPOINT ["dotnet", "InvoiceJet.Presentation.dll"]
