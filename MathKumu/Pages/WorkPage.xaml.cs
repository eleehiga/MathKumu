using System;
using System.Collections.Generic;
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
            StrokeWidth = 10,
            StrokeCap = SKStrokeCap.Round,
            StrokeJoin = SKStrokeJoin.Round
        };

        readonly MathKumuClient mathclient = new MathKumuClient();
        private string equationString = "Loading ..."; // Initially
        private string checkString;
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
        }

        protected override void OnAppearing()
        {
            base.OnAppearing();
            this.OnGetEquation();
        }

        // Communicate with HTTP Client
        private async void OnGetEquation()
        {
            var equation = await mathclient.GetEquation(topic.MathType);
            EquationString = equation.equation;
            numbers = equation.numbers;
        }

        private async void OnCheckAnswer()
        {
            CheckMessageString = await mathclient.CheckAnswer(numbers, int.Parse(entry.Text), Title);
            if(CheckMessageString.Equals("Correct"))
            {
                this.OnGetEquation();
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

        //SKPoint ConvertToPixel(TouchTrackingPoint location)
        //{
        //    return new SKPoint((float)(canvasView.CanvasSize.Width * location.X / canvasView.Width),
        //                       (float)(canvasView.CanvasSize.Height * location.Y / canvasView.Height));
        //}

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
