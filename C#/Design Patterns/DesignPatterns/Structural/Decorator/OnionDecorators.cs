namespace DesignPatterns.Structural.Decorator
{
    public class OnionDecorators : ToppingsDecortator
    {
        private Dosa _dosa;
        public OnionDecorators(Dosa dosa)
        {
            _dosa = dosa;
        }
        public override int GetCost() => this._dosa.GetCost() + 50;
        public override string GetDescription() => $"{this._dosa.GetDescription()} with Onion Toppings";
    }
}
