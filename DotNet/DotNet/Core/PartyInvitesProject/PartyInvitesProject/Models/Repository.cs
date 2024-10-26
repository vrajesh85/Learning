using System.Collections.Generic;

namespace PartyInvitesProject.Models
{
    public static class Repository
    {
        private static List<GuestResponse> _responses = new List<GuestResponse>();
        
        public static IEnumerable<GuestResponse> Responses => _responses;
        public static void AddResponse(this GuestResponse response)
        {
            _responses.Add(response);
        }
    }
}
