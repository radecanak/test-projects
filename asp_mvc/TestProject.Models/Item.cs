using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace TestProject.Models
{
    public class Item
    {
        public int Id { get; set; }

        [MaxLength(100, ErrorMessage ="Field must have less than 100 characters.")]
        public string Name { get; set; }

        [Range(typeof(decimal), "-1000000000", "1000000000", ErrorMessage = "The field must be in range (-1000000000, 1000000000)")]
        [DisplayFormat(DataFormatString = "{0:F1}")]
        public decimal Value { get; set; }
    }
}
