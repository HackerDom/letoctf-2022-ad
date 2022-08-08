using System.Collections.Concurrent;

namespace CatFarm;

public class Farm
{
    public Cat[] Cats { get; init; }
    public Guid FarmId { get; init; }
    
    public string FarmName { get; init; }
}