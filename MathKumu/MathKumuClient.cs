using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace MathKumu
{
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
            var result = await client.PostAsync(Url + "equation", new StringContent(
                JsonConvert.SerializeObject(type), Encoding.UTF8, "application/json"));
            return JsonConvert.DeserializeObject<Equation>(await result.Content.ReadAsStringAsync());
        }


    }
}
