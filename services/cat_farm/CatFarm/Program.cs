using System.Text;
using Microsoft.AspNetCore.Builder;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", async (c) =>
{
    await c.Response.Body.WriteAsync(Encoding.UTF8.GetBytes("Meow World!"));
});

app.Run();