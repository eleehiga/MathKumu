using System;
using System.Collections.Generic;

using Xamarin.Forms;

namespace MathKumu.Pages
{
    public partial class ArithmeticPage : ContentPage
    {
        public ArithmeticPage()
        {
            InitializeComponent();

            btnAddition.Clicked += (s, e) => Navigation.PushAsync(new WorkPage(TopicsData.Addition));
        }
    }
}
