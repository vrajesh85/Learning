using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PracticeApp
{
    public class PriceChangedEventArgs : EventArgs
    {
       public decimal OldPrice;
       public decimal NewPrice;
        public PriceChangedEventArgs(decimal oldPrice , decimal newPrice)
        {
            this.OldPrice = oldPrice;
            this.NewPrice = newPrice;
        }
    }

    public class Stock
    {
        private decimal _price;
        public event EventHandler<PriceChangedEventArgs> PriceChangedHandler;
        protected void OnPriceChanged(PriceChangedEventArgs e)
        {
            PriceChangedHandler?.Invoke(this, e);
        }
        public decimal Price 
        { 
            get {  return _price; }
            set 
            {
                decimal oldPrice = _price;
                OnPriceChanged(new PriceChangedEventArgs(oldPrice, value));
            }
        }
    }
}
