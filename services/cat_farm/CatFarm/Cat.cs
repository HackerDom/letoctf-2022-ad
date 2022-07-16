using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Drawing;
using SixLabors.ImageSharp.Drawing.Processing;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;

namespace CatFarm;

public record Cat
{
    public Guid Genome { get; init; } = Guid.NewGuid();
    public string Name { get; init; }

    public byte[] GetImage()
    {
        using var img = new Image<Rgba32>(15, 15);
        var genome = Genome.ToByteArray();

        var leftEar = new RectangularPolygon(2, 0, 3, 3);
        var rightEar = new RectangularPolygon(10, 0, 3, 3);

        var earColor = Color.FromRgb(genome[0], genome[1], genome[2]);

        var head = new RectangularPolygon(0, 3, 16, 3);
        
        var headColor = Color.FromRgb(genome[3], genome[4], genome[5]);
        
        var betweenEyes = new RectangularPolygon(6, 6, 3, 3);

        var leftEye = new RectangularPolygon(3, 6, 3, 3);
        var rightEye = new RectangularPolygon(9, 6, 3, 3);

        var leftEyeSecondaryZone = new RectangularPolygon(0, 6, 3, 3);
        var rightEyeSecondaryZone = new RectangularPolygon(12, 6, 3, 3);

        var secondaryEyesColor = Color.FromRgb(genome[7], genome[8], genome[9]);

        var primaryGen =
            genome[7..10]
                .Select(Convert.ToInt32)
                .Select(x => x >> 1)
                .Select(Convert.ToByte).ToArray();
        var primaryEyesColor = Color.FromRgb(primaryGen[0], primaryGen[1], primaryGen[2]);

        var nose = new RectangularPolygon(6, 9, 3, 3);
        var noseColor = Color.FromRgb(genome[10], genome[11], genome[12]);

        var leftCheek = new RectangularPolygon(0, 9, 3, 6);
        var rightCheek = new RectangularPolygon(12, 9, 3, 6);

        var meowth = new RectangularPolygon(3, 12, 9, 3);
        var meowthColor = Color.FromRgb(genome[13], genome[14], genome[15]);
        
        img.Mutate(x =>
            x
            //.Fill(genomeColor, rect)
            .Fill(earColor, rightEar)
            .Fill(earColor, leftEar)
            .Fill(headColor, head)
            .Fill(headColor, betweenEyes)
            
            .Fill(primaryEyesColor, leftEye)
            .Fill(primaryEyesColor, rightEye)
            .Fill(secondaryEyesColor, leftEyeSecondaryZone)
            .Fill(secondaryEyesColor, rightEyeSecondaryZone)
            
            .Fill(noseColor, nose)
            
            .Fill(headColor, leftCheek)
            .Fill(headColor, rightCheek)
            
            .Fill(meowthColor, meowth)
        );
        
        var ms = new MemoryStream();
        img.SaveAsPng(ms);

        return ms.GetBuffer();
    }
}