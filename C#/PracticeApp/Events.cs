using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PracticeApp
{
    public class Stock
    {
        decimal _price;
        public event EventHandler<PriceChangedEventArgs> PriceChanged;

        protected void OnPriceChanged(PriceChangedEventArgs e)
        {
            PriceChanged?.Invoke(this, e);
        }
        public decimal Price
        {
            get => _price;
            set
            {
                decimal oldValue = _price;
                _price = value;
                OnPriceChanged(new PriceChangedEventArgs(oldValue, _price));
            }
        }
    }


    public class PriceChangedEventArgs : EventArgs
    {
        public readonly decimal oldPrice;
        public readonly decimal newPrice;

        public PriceChangedEventArgs(decimal oldPrice, decimal newPrice)
        {
            this.oldPrice = oldPrice;
            this.newPrice = newPrice;
        }
    }
}
