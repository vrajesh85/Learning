namespace MVCApp.Models
{
    public class PersonRepository
    {
        public List<Person> List { get; set; } = new();

        public void Add(Person person) {
            List.Add(person);
        }

        public List<Person> GetAll() => List;
    }
}
