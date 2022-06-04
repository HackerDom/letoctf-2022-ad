using CatFarm;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

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
        await c.Response.Body.WriteAsync(foundCat.GetImage());
    }
});


// add meow-meow method 

app.Run();