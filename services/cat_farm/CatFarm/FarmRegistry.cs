namespace CatFarm;

public class FarmRegistry
{
    public FarmRegistry() => 
        Directory.CreateDirectory(Constants.FarmsDir);

    public async Task AddFarm(Farm farm)
    {
        await File.WriteAllTextAsync(
            Path.Combine(Constants.FarmsDir, $"{farm.FarmId}-{Constants.FarmNameFile}"), farm.FarmName);
        await File.WriteAllTextAsync(
            Path.Combine(Constants.FarmsDir, farm.FarmId.ToString()),
            string.Join(Constants.Separator, farm.Cats.Select(x => x.Genome.ToString())));
    }

    public async Task<string> ObtainFarmCatsInfo(string farmId) =>
        await File.ReadAllTextAsync(Path.Combine(Constants.FarmsDir, farmId));
}