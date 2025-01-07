using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PracticeApp.Algorithms
{
    public class BubbleSort
    {
        public int[] Sort(int[] nums)
        {
            int arrayLength = nums.Length;

            for(int i = 0; i < arrayLength - 1; i++)
            {
                for (int j = 0; j < arrayLength - 1 - i; j++)
                {
                    if (nums[j] > nums[j + 1])
                    {
                        int temp = nums[j];
                        nums[j] = nums[j+1];
                        nums[j+1] = temp;
                    }
                }
            }
            return nums;
        }
    }
}
