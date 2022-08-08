using System.Text;
using CatFarm;


var app = WebApplication.CreateBuilder(args).Build();
var catField = new CatField();
var farmsRegistry = new FarmRegistry();


app.MapGet("/cat/{cat}",async (HttpContext c, Guid cat) =>
{
    if (!catField.TryGetCat(cat, out var foundCat))
    {
        c.Response.StatusCode = StatusCodes.Status404NotFound;
    }
    else
    {
        c.Response.Headers.ContentType = "image/png";
        c.Response.Headers["Name"] = foundCat.Name;
        await c.Response.Body.WriteAsync(foundCat.GetImage());
    }
});

app.MapPost("/cat/{catGenome}", async (HttpContext c, Guid catGenome) =>
{
    var requiredHeaders = new List<string> { "Name", "x", "y" };
    if (requiredHeaders.Any(x => !c.Request.Headers.ContainsKey(x)))
    {
        c.Response.StatusCode = StatusCodes.Status400BadRequest;
        await c.Response.Body.WriteAsync(Encoding.UTF8.GetBytes("Bad request, fix headers"));
    }
    else
    {
        var cat = new Cat
        {
            Genome = catGenome,
            Name = c.Request.Headers["Name"]
        };
        
        catField.AddCat(cat);
    }
});

app.MapGet("/farm/", async c =>
{
    var requiredHeaders = new List<string> { "FarmId" };
    if (requiredHeaders.Any(x => !c.Request.Headers.ContainsKey(x)))
    {
        c.Response.StatusCode = StatusCodes.Status400BadRequest;
        await c.Response.Body.WriteAsync(Encoding.UTF8.GetBytes("Bad request, fix headers"));
    }
    else
    {
        await c.Response.Body.WriteAsync(
            Encoding.UTF8.GetBytes(
                await farmsRegistry.ObtainFarmCatsInfo(c.Request.Headers["FarmId"]))
        );
    }
});

app.MapPost("/farm/{farmId}", async (HttpContext c, Guid farmId) =>
{
    var requiredHeaders = new List<string> { "Cats", "Name" };
    if (requiredHeaders.Any(x => !c.Request.Headers.ContainsKey(x)))
    {
        c.Response.StatusCode = StatusCodes.Status400BadRequest;
        await c.Response.Body.WriteAsync(Encoding.UTF8.GetBytes("Bad request, fix headers"));
    }
    else
    {
        var approvedCats = new List<Cat>();
        foreach (var val in c.Request.Headers["Cats"])
            if (Guid.TryParse(val, out var catId) && catField.TryGetCat(catId, out var cat))
                approvedCats.Add(cat);

        var farm = new Farm
        {
            FarmId = farmId,
            FarmName = c.Request.Headers["Name"],
            Cats = approvedCats.ToArray()
        };
        
        await farmsRegistry.AddFarm(farm);
    }
});

// add meow-meow method 

app.Run();