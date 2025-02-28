namespace DesignPatterns.Structural.Decorator
{
    public class PlainDosa : Dosa
    {
        public PlainDosa()
        {
            Description = "Plain Dosa";
        }
        public override int GetCost() => 40;
    }
}
