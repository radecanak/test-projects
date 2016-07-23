using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TestProject.Models.Interfaces
{
    public interface IItemRepository : IDisposable
    {
        IEnumerable<Item> ListAll();
        void Add(Item item);
        Item FindById(int? id);
        void SaveChanges();
        void RemoveById(int? id);
    }
}
