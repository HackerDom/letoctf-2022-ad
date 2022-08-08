using System.Text;
using CatFarm;

var app = WebApplication.CreateBuilder(args).Build();
var catField = new CatField();
var farmsRegistry = new FarmRegistry();

app.MapGet("/", async (c) =>
{
    c.Response.ContentType = "text/html";
    
});

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
        if (!long.TryParse(c.Request.Headers["x"], out var x) || !long.TryParse(c.Request.Headers["y"], out var y))
        {
            c.Response.StatusCode = StatusCodes.Status400BadRequest;
            await c.Response.Body.WriteAsync(Encoding.UTF8.GetBytes("Bad request, fix ur longs!"));
        }
        else
        {
            var cat = new Cat
            {
                Genome = catGenome,
                Name = c.Request.Headers["Name"],
                KnownX = x,
                KnownY = y
            };
        
            catField.AddCat(cat);   
        }
    }
});

app.MapGet("/meow-meow", async c =>
{
    if (!long.TryParse(c.Request.Headers["x"], out var x) || !long.TryParse(c.Request.Headers["y"], out var y))
    {
        c.Response.StatusCode = StatusCodes.Status400BadRequest;
        await c.Response.Body.WriteAsync(Encoding.UTF8.GetBytes("Bad request, fix ur longs!"));
    }
    else
    {
        var foundCats = await catField.MeowMeow(x, y);
        if (foundCats.Count > 0)
        {
            await c.Response.Body.WriteAsync(
                Encoding.UTF8.GetBytes(
                    string.Join(",", foundCats.Select(x => x.ToString()))));
        }
        else
        {
            c.Response.StatusCode = StatusCodes.Status404NotFound;
        }
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
        foreach (var val in c.Request.Headers["Cats"].First().Split(",", StringSplitOptions.RemoveEmptyEntries))
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

app.Run();