namespace DesignPatterns.Structural.Decorator
{
    public class ButterDosa : Dosa
    {
        public ButterDosa()
        {
            Description = "Butter Dosa";
        }

        public override int GetCost() => 50;
    }
}
