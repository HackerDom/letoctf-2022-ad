using System.Collections.Concurrent;
using System.Security.Cryptography;
using System.Text;
using Newtonsoft.Json;

namespace CatFarm;

public class CatField
{
    private readonly ConcurrentDictionary<string, Cat> knownCats = new();

    public CatField()
    {
        Task.Run(InitDumpRoutine);
    }

    public void AddCat(Cat cat) => knownCats[cat.Genome.ToString()] = cat;
    public bool TryGetCat(Guid catId, out Cat cat) => knownCats.TryGetValue(catId.ToString(), out cat);

    public void Dump()
    {
        Directory.CreateDirectory("cats");
        knownCats.Select((content, key) =>
        {
            using var sha1 = SHA1.Create();
            var hashString = string
                .Concat(
                    sha1.ComputeHash(Encoding.UTF8.GetBytes(key.ToString()))
                        .Select(x => x.ToString("X2")));
            try
            {
                Console.WriteLine(hashString);
                File.WriteAllText(Path.Combine("cats", hashString), JsonConvert.SerializeObject(content.Value));
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }
            return hashString;
        }).ToList();
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