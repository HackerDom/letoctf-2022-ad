FROM mcr.microsoft.com/dotnet/sdk:6.0 AS builder
LABEL stage=builder

COPY ./CatFarm /app

WORKDIR /app

RUN dotnet restore && dotnet publish -c Release -o publish

FROM mcr.microsoft.com/dotnet/aspnet:6.0

WORKDIR /app

COPY --from=0 /app ./

CMD ["dotnet", "publish/CatFarm.dll"]
