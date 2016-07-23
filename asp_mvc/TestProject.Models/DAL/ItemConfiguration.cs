using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Data.Entity.SqlServer;
using System.Linq;
using System.Web;
using TestProject.Models;

namespace TestProject.Models.DAL
{
    public class ItemConfiguration : DbConfiguration
    {
        public ItemConfiguration()
        {
            SetExecutionStrategy("System.Data.SqlClient", () => new SqlAzureExecutionStrategy());
        }
    }
}