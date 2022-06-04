using System.Collections.Concurrent;
using System.Security.Cryptography;
using System.Text;
using Newtonsoft.Json;

namespace CatFarm;

public class CatField
{
    private ConcurrentDictionary<string, Cat> knownCats;

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
            var hashString = Encoding.UTF8.GetString(sha1.ComputeHash(Encoding.UTF8.GetBytes(key.ToString())));
            try
            {
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