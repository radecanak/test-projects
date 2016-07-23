using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TestProject.Models.DAL;
using TestProject.Models.Interfaces;

namespace TestProject.Models
{
    public class ItemRepository : IItemRepository
    {
        private readonly ItemContext dbContext = new ItemContext();

        
        public IEnumerable<Item> ListAll()
        {
            return dbContext.Items.AsEnumerable();
        }

        public void Add(Item item)
        {
            dbContext.Items.Add(item);
            dbContext.SaveChanges();
        }

        public Item FindById(int? id)
        {
            return dbContext.Items.Find(id);
        }

        public void SaveChanges()
        {
            dbContext.SaveChanges();
        }

        public void RemoveById(int? id)
        {
            Item item = dbContext.Items.Find(id);
            dbContext.Items.Remove(item);
            dbContext.SaveChanges();
        }

        public void Dispose()
        {
            dbContext.Dispose();
        }
    }
}
