using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using RestSharp;
using SkiaSharp;

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
        public string message { get; set; }
        //public IList<string> work { get; set; }
        public IList<IList<string>> work { get; set; }
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

        /*public async Task<AnalyerResults> AnalyzeWork(SKData pngImage)
        {
            HttpClient client = await GetClient();
            var result = await client.PostAsync(Url + "analyzer", new ByteArrayContent(pngImage.ToArray()));
            //var result = await client.PostAsync(Url + "analyzer", new StringContent(Encoding.UTF8.GetString(pngImage.ToArray()), Encoding.UTF8));
            return JsonConvert.DeserializeObject<AnalyerResults>(await result.Content.ReadAsStringAsync());
        }*/

        public AnalyerResults AnalyzeWork(SKData pngImage)
        {
            var client = new RestClient(Url + "analyzer");
            client.Timeout = -1;
            var request = new RestRequest(Method.POST);
            request.AddHeader("Content-Type", "image/png");
            //request.AddParameter("image/png", Convert.ToBase64String(pngImage.ToArray()), ParameterType.RequestBody);
            //request.AddParameter("image/png", Encoding.UTF32.GetString(pngImage.ToArray()), ParameterType.RequestBody);
            //request.AddParameter("image/png", Convert.ToString(pngImage.ToArray(), 2), ParameterType.RequestBody);
            request.AddParameter("image/png", pngImage.ToArray(), ParameterType.RequestBody);
            IRestResponse response = client.Execute(request);
            System.Console.WriteLine(response.StatusCode);
            return JsonConvert.DeserializeObject<AnalyerResults>(response.Content);
        }

        public static string ByteArrayToString(byte[] ba)
        {
            StringBuilder hex = new StringBuilder(ba.Length * 2);
            foreach (byte b in ba)
                hex.AppendFormat("{0:x2}", b);
            return hex.ToString();
        }
    }
}
