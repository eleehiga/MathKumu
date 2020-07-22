using System;
using System.IO;
using Foundation;
using MathKumu.iOS;
using MathKumu.Services;
using UIKit;
using Xamarin.Forms;

[assembly: Dependency(typeof(SaveToAlbum))]
namespace MathKumu.iOS
{
    public class SaveToAlbum : ISavePhotosToAlbum
    {
        public void SavePhotosWithStream(string name, Stream stream)
        {
            var imageData = NSData.FromStream(stream);
            var image = UIImage.LoadFromData(imageData);

            image.SaveToPhotosAlbum((img, error) =>
            {

            });
        }
    }
}
