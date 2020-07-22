using System;
using System.IO;

namespace MathKumu.Services
{
        public interface ISavePhotosToAlbum
        {
            void SavePhotosWithStream(string name, Stream data);
        }
}
