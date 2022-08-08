namespace CatFarm;

public class FarmRegistry
{
    public FarmRegistry() => 
        Directory.CreateDirectory(Constants.FarmsDir);

    public async Task AddFarm(Farm farm)
    {
        Directory.CreateDirectory(
            Path.Combine(Constants.FarmsDir, farm.FarmId.ToString()));
        await File.WriteAllTextAsync(
            Path.Combine(Constants.FarmsDir, farm.FarmId.ToString(), Constants.FarmNameFile), farm.FarmName);
        await File.WriteAllTextAsync(
            Path.Combine(Constants.FarmsDir, farm.FarmId.ToString(), Constants.CatsRegistryName),
            string.Join(Constants.Separator, farm.Cats.Select(x => x.Genome.ToString())));
    }

    public async Task<string> ObtainFarmCatsInfo(string farmId) =>
        await File.ReadAllTextAsync(Path.Combine(Constants.FarmsDir, farmId));
}