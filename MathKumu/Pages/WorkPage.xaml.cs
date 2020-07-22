using System;
using System.Collections.Generic;
using System.IO;
using MathKumu.Services;
using SkiaSharp;
using SkiaSharp.Views.Forms;
using TouchTracking;
using Xamarin.Forms;


namespace MathKumu.Pages
{
    public partial class WorkPage : ContentPage
    {
        Dictionary<long, SKPath> inProgressPaths = new Dictionary<long, SKPath>();
        List<SKPath> completedPaths = new List<SKPath>();

        SKPaint paint = new SKPaint
        {
            Style = SKPaintStyle.Stroke,
            Color = SKColors.Black,
            //StrokeWidth = 10,
            StrokeWidth = 5,
            StrokeCap = SKStrokeCap.Round,
            StrokeJoin = SKStrokeJoin.Round
        };

        readonly MathKumuClient mathclient = new MathKumuClient();
        private string equationString = "Loading ..."; // Initially
        private string checkString = " ";
        private string workString = " ";
        private string resultString = " ";
        private IList<int> numbers;
        private TopicsData topic;

        public WorkPage(TopicsData topic)
        {
            BindingContext = this;
            InitializeComponent();

            this.topic = topic;

            Title = topic.MathType;
            btnHelp.Clicked += (s, e) => Navigation.PushAsync(new HelpPage());
            btnCheck.Clicked += (s, e) => this.OnCheckAnswer();
            btnAnalyze.Clicked += (s, e) => this.OnAnalyze();
            //btnAnalyze.Clicked += (s, e) => this.SavePhoto();
            btnClear.Clicked += (s, e) => this.OnClear();
        }
        // Remove This Later
        private void SavePhoto()
        {
            var surface = SKSurface.Create(new SKImageInfo((int)canvasView.CanvasSize.Width,
                                            (int)canvasView.CanvasSize.Height));
            var canvas = surface.Canvas;
            //canvas.Clear();
            canvas.Clear(SKColors.White);

            foreach (SKPath path in completedPaths)
                canvas.DrawPath(path, paint);

            foreach (SKPath path in inProgressPaths.Values)
                canvas.DrawPath(path, paint);

            canvas.Flush();

            var snap = surface.Snapshot();
            var pngImage = snap.Encode(SKEncodedImageFormat.Png, 100);
            Stream stream = new MemoryStream(pngImage.ToArray());
            DependencyService.Get<ISavePhotosToAlbum>().SavePhotosWithStream("test.jpg", stream);
        }
        //
        
        protected override void OnAppearing()
        {
            base.OnAppearing();
            this.OnGetEquation();
        }

        private void OnClear()
        {
            inProgressPaths.Clear();
            completedPaths.Clear();
            canvasView.InvalidateSurface(); // Redraws canvasView 
        }

        // Communicate with HTTP Client
        private async void OnGetEquation()
        {
            try
            {
                var equation = await mathclient.GetEquation(topic.MathType);
                EquationString = equation.equation;
                numbers = equation.numbers;
            }
            catch
            {
                EquationString = "Error";
            }
            
        }


        private async void OnCheckAnswer()
        {
            try
            {
                CheckMessageString = await mathclient.CheckAnswer(numbers, int.Parse(entry.Text), Title);
                if (CheckMessageString.Equals("Correct"))
                {
                    this.OnGetEquation();
                    entry.Text = "";
                }
            }
            catch { return; }
        }

        private async void OnAnalyze()
        {
            ResultString = "Loading...";
            WorkString = "Loading...";

            var surface = SKSurface.Create(new SKImageInfo((int)canvasView.CanvasSize.Width,
                                            (int)canvasView.CanvasSize.Height));
            var canvas = surface.Canvas;
            canvas.Clear(SKColors.White);

            foreach (SKPath path in completedPaths)
                canvas.DrawPath(path, paint);

            foreach (SKPath path in inProgressPaths.Values)
                canvas.DrawPath(path, paint);

            canvas.Flush();

            var snap = surface.Snapshot();
            var pngImage = snap.Encode(SKEncodedImageFormat.Png, 100);
            try
            {
                AnalyerResults analyerResults = mathclient.AnalyzeWork(pngImage);
                ResultString = analyerResults.message;

                //Displaying the work
                //WorkString = "  \n\n\n";
                WorkString = " \t";
                var rowSize = analyerResults.work.Count;
                var colSize = analyerResults.work[0].Count;
                for(int i = 0; i < colSize; i++)
                {
                    WorkString = WorkString + i + "\t";
                }
                WorkString = WorkString + "\n";
                for (int i = 0; i < rowSize; i++)
                {
                    WorkString = WorkString + "\n" + i + "\t";
                    foreach(string work in analyerResults.work[i])
                    {
                        WorkString = WorkString + work + "\t";
                    }
                }
                

            }
            catch
            {
                ResultString = "Error...";
                WorkString = "Error...";
            } 
        }

        // Binding variables
        public string EquationString
        {
            get { return equationString; }
            set
            {
                equationString = value;
                OnPropertyChanged(nameof(EquationString));
            }
        }

        public string CheckMessageString
        {
            get { return checkString; }
            set
            {
                checkString = value;
                OnPropertyChanged(nameof(CheckMessageString));
            }
        }

        public string WorkString
        {
            get { return workString; }
            set
            {
                workString = value;
                OnPropertyChanged(nameof(WorkString));
            }
        }

        public string ResultString
        {
            get { return resultString; }
            set
            {
                resultString = value;
                OnPropertyChanged(nameof(ResultString));
            }
        }

        // For drawing
        void OnTouchEffectAction(object sender, TouchActionEventArgs args)
        {
            switch (args.Type)
            {
                case TouchActionType.Pressed:
                    if (!inProgressPaths.ContainsKey(args.Id))
                    {
                        SKPath path = new SKPath();
                        path.MoveTo(ConvertToPixel(args.Location));
                        //path.MoveTo(ConvertToPixel(new Point(args.Location.X, args.Location.Y)));
                        inProgressPaths.Add(args.Id, path);
                        canvasView.InvalidateSurface();
                    }
                    break;

                case TouchActionType.Moved:
                    if (inProgressPaths.ContainsKey(args.Id))
                    {
                        SKPath path = inProgressPaths[args.Id];
                        path.LineTo(ConvertToPixel(args.Location));
                        //path.MoveTo(ConvertToPixel(new Point(args.Location.X, args.Location.Y)));
                        canvasView.InvalidateSurface();
                    }
                    break;

                case TouchActionType.Released:
                    if (inProgressPaths.ContainsKey(args.Id))
                    {
                        completedPaths.Add(inProgressPaths[args.Id]);
                        inProgressPaths.Remove(args.Id);
                        canvasView.InvalidateSurface();
                    }
                    break;

                case TouchActionType.Cancelled:
                    if (inProgressPaths.ContainsKey(args.Id))
                    {
                        inProgressPaths.Remove(args.Id);
                        canvasView.InvalidateSurface();
                    }
                    break;
            }
        }

        SKPoint ConvertToPixel(Point pt)
        {
            return new SKPoint((float)(canvasView.CanvasSize.Width * pt.X / canvasView.Width),
                               (float)(canvasView.CanvasSize.Height * pt.Y / canvasView.Height));
        }

        void OnCanvasViewPaintSurface(object sender, SKPaintSurfaceEventArgs args)
        {
            SKCanvas canvas = args.Surface.Canvas;
            canvas.Clear();

            foreach (SKPath path in completedPaths)
            {
                canvas.DrawPath(path, paint);
            }

            foreach (SKPath path in inProgressPaths.Values)
            {
                canvas.DrawPath(path, paint);
            }
        }
    }
}
