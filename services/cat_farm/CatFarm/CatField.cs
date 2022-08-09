using System.Collections.Concurrent;
using System.Security.Cryptography;
using System.Text;
using Newtonsoft.Json;

namespace CatFarm;

public class CatField
{
    private readonly TimeSpan CatLifetime = TimeSpan.FromMinutes(20);
    private readonly ConcurrentDictionary<string, Cat> knownCats = new();

    public CatField()
    {
        WarmUp()
            .GetAwaiter()
            .GetResult();
        
        Task.Run(InitDumpRoutine);
        Task.Run(KillOldCats);
    }

    public async Task<List<Guid>> MeowMeow(long x, long y)
    {
        var foundCats = new List<Guid>();
        foreach (var cat in knownCats.Select(x => x.Value))
        {
            if (Math.Pow(cat.KnownX - x, 2) + Math.Pow(cat.KnownY - y, 2) <= Math.Pow(Constants.MeowMeowRadius, 2))
            {
                foundCats.Add(cat.Genome);
            } 
        }

        return foundCats;
    }

    public void AddCat(Cat cat) => knownCats[cat.Genome.ToString()] = cat;
    public bool TryGetCat(Guid catId, out Cat cat) => knownCats.TryGetValue(catId.ToString(), out cat);

    public void Dump()
    {
        Directory.CreateDirectory(Constants.CatsDir);
        var dumpedCats = knownCats.Select((content, key) =>
        {
            using var sha1 = SHA1.Create();
            var hashString = string
                .Concat(
                    sha1.ComputeHash(Encoding.UTF8.GetBytes(key.ToString()))
                        .Select(x => x.ToString("X2")));
            var expectingDump = Path.Combine(Constants.CatsDir, hashString);
            try
            {
                if (!File.Exists(expectingDump))
                {
                    File.WriteAllText(expectingDump, JsonConvert.SerializeObject(content.Value));
                }
            }
            catch (Exception) { }
            return expectingDump;
        }).ToHashSet();
        
        foreach (var dump in Directory.EnumerateFiles(Constants.CatsDir))
        {
            if (!dumpedCats.Contains(dump))
            {
                try
                {
                    File.Delete(dump);
                }
                catch (Exception) { }
            }
        }
    }

    private async Task WarmUp()
    {
        if (!Directory.Exists(Constants.CatsDir))
            return;
        await Parallel.ForEachAsync(Directory.EnumerateFiles(Constants.CatsDir), async (catFile, ct) =>
        {
            try
            {
                var fileContents = await File.ReadAllTextAsync(catFile, ct);
                var deserializedCatObj = JsonConvert.DeserializeObject<Cat>(fileContents);
                if (deserializedCatObj is null) return;
                
                knownCats.TryAdd(deserializedCatObj.Genome.ToString(), deserializedCatObj);
            }
            catch (Exception) { }
        });
    }

    private async Task KillOldCats()
    {
        while (true)
        {
            try
            {
                foreach (var cat in knownCats.Select(x => x.Value))
                    if (cat.CreationDate + CatLifetime < DateTimeOffset.UtcNow)
                        knownCats.TryRemove(cat.Genome.ToString(), out _);
            }
            finally
            {
                await Task.Delay(TimeSpan.FromMinutes(1));
            }
        }
    }

    private async Task InitDumpRoutine()
    {
        while (true)
        {
            try
            {
                Dump();
            }
            finally
            {
                await Task.Delay(TimeSpan.FromSeconds(10));
            }
        }
    }
}