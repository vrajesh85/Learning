namespace DesignPatterns.Structural.Decorator
{
    public abstract class Dosa
    {
        protected string Description = "Unknown Dosa";
        public virtual string GetDescription() => this.Description;
        public abstract int GetCost();
    }
}
