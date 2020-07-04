using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace MathKumu
{
    public class Type
    {
        public string type { get; set; }
    }

    public class Answer
    {
        public IList<int> numbers { get; set; }
        public int answer { get; set; }
        public string type { get; set; }
    }

    public class Equation
    {
        public string equation { get; set; }
        public IList<int> numbers {get; set;}
    }

    public class AnalyerResults
    {
        public IList<string> work { get; set; }
        public string message { get; set; }
    }

    public class MathKumuClient
    {
        const string Url = "https://mathkumu.wn.r.appspot.com/";

        private async Task<HttpClient> GetClient()
        {
            HttpClient client = new HttpClient();
            return client;
        }

        public async Task<Equation> GetEquation(string type)
        {
            HttpClient client = await GetClient();
            Type Type1 = new Type();
            Type1.type = type;
            var result = await client.PostAsync(Url + "equation", new StringContent(
                JsonConvert.SerializeObject(Type1), Encoding.UTF8, "application/json"));
            return JsonConvert.DeserializeObject<Equation>(await result.Content.ReadAsStringAsync());
        }

        public async Task<string> CheckAnswer(IList<int> numbers, int answer, string type)
        {
            HttpClient client = await GetClient();
            Answer Answer1 = new Answer();
            Answer1.answer= answer;
            Answer1.numbers = numbers;
            Answer1.type = type;
            var result = await client.PostAsync(Url + "check", new StringContent(
                JsonConvert.SerializeObject(Answer1), Encoding.UTF8, "application/json"));
            return await result.Content.ReadAsStringAsync();
        }
    }
}
