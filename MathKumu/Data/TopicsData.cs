using System;
namespace MathKumu
{
    public class TopicsData
    {
        public string MathType { get; set; }
        public static TopicsData Addition = new TopicsData()
        {
            MathType = "Addition"
        };
    }
}
