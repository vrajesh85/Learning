using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace PracticeApp.Regular_Expressions
{
    internal class Basics
    {
        public bool DoTheyMatch(string first, string second) => GetMatch(first, second).Success;

        public Match GetMatch(string first, string second) => Regex.Match(first, second,RegexOptions.Compiled);
    }
}
