using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Web;
using TestProject.Models;

namespace TestProject.Models.DAL
{
    public class ItemContext : DbContext
    {
        public DbSet<Item> Items { get; set; }
    }
}