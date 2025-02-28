namespace DesignPatterns.Structural.Decorator
{
    public class MasalaDecorators : ToppingsDecortator
    {
        private Dosa _dosa;
        public MasalaDecorators(Dosa dosa)
        {
            _dosa = dosa;
        }
        public override int GetCost() => this._dosa.GetCost() + 70;
        public override string GetDescription() => $"{this._dosa.GetDescription()} with Masala Toppings";
    }
}
