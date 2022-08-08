using System.Text;
using CatFarm;


var app = WebApplication.CreateBuilder(args).Build();
var catField = new CatField();

// todo: guid -> str, id is just a genome, but not the key, key is in the fs!
app.MapGet("/cat/{cat:guid}",async (HttpContext c, Guid cat) =>
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

app.MapPost("/cat/{catGenome:guid}", async (HttpContext c, Guid catGenome) =>
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

// add meow-meow method 

app.Run();