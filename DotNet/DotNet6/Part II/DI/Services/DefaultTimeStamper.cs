namespace DI.Services
{
    public class DefaultTimeStamper : ITimeStamper
    {
        public string TimeStamp 
        {
            get => DateTime.Now.ToString();
        }
    }
}
