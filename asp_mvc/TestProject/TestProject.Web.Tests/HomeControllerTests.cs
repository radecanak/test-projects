using System;
using System.Text;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using TestProject.Web.Controllers;
using System.Web.Mvc;
using TestProject.Models.DAL;
using System.Linq;

namespace TestProject.Web.Tests
{
    /// <summary>
    /// Summary description for HomeControllerTests
    /// </summary>
    [TestClass]
    public class HomeControllerTests
    {
        private HomeController controller;
        

        public HomeControllerTests()
        {
              controller = new HomeController(new Models.ItemRepository());
        }
            


        private TestContext testContextInstance;

        /// <summary>
        ///Gets or sets the test context which provides
        ///information about and functionality for the current test run.
        ///</summary>
        public TestContext TestContext
        {
            get
            {
                return testContextInstance;
            }
            set
            {
                testContextInstance = value;
            }
        }

        #region Additional test attributes
        //
        // You can use the following additional attributes as you write your tests:
        //
        // Use ClassInitialize to run code before running the first test in the class
        // [ClassInitialize()]
        // public static void MyClassInitialize(TestContext testContext) { }
        //
        // Use ClassCleanup to run code after all tests in a class have run
        // [ClassCleanup()]
        // public static void MyClassCleanup() { }
        //
        // Use TestInitialize to run code before running each test 
        [TestInitialize()]
        public void MyTestInitialize()
        {
            DeleteAll();
            Create();
        }

        // Use TestCleanup to run code after each test has run
        [TestCleanup()]
        public void MyTestCleanup()
        {
           
        }
        
        #endregion
        
        [TestMethod]
        [TestProperty("currentFilter", "CF")]
        public void IndexWithDefaultPageTest()
        {
            IndexTest();
        }

        [TestMethod]
        [TestProperty("currentFilter", "CF")]
        [TestProperty("page", "2")]
        public void IndexWithSecondPageTest()
        {
            IndexTest();
        }

        [TestMethod]
        [TestProperty("sortOrder", "Name")]
        public void IndexWithSortOrderNameTest()
        {
            IndexTest();
        }

        [TestMethod]
        [TestProperty("sortOrder", "name_desc")]
        public void IndexWithSortOrderNameDescTest()
        {
            IndexTest();
        }

        [TestMethod]
        [TestProperty("sortOrder", "Value")]
        public void IndexWithSortOrderValueTest()
        {
            IndexTest();
        }

        [TestMethod]
        [TestProperty("sortOrder", "value_desc")]
        public void IndexWithSortOrderValueDescTest()
        {
            IndexTest();
        }

        [TestMethod]
        [TestProperty("currentFilter", "CF")]
        [TestProperty("searchString", "CF")]
        public void IndexWithDefaultPageAndSearchStringTest()
        {
            IndexTest();
        }

        [TestMethod]     
        [TestProperty("currentFilter", "CF")]
        [TestProperty("page", "2")]
        [TestProperty("searchString", "CF")]
        public void IndexWithSecondPageAndSearchStringTest()
        {
            IndexTest();
        }

        [TestMethod]
        public void DetailsTest()
        {
            ActionResult result = controller.Details(controller.Items.ElementAt(0).Id);
            Assert.IsInstanceOfType(result, typeof(ViewResult), "Result type should be ViewResult");
            result = controller.Details(null);
            Assert.IsInstanceOfType(result, typeof(HttpStatusCodeResult), "Result type should be HttpStatusCodeResult when id is null.");

            result = controller.Details(-1);
            Assert.IsInstanceOfType(result, typeof(HttpNotFoundResult), "Result type should be HttpNotFoundResult when id does not exist.");

        }

        [TestMethod]
        public void EditTest()
        {
            ActionResult result = controller.Edit(controller.Items.ElementAt(0).Id);
            Assert.IsInstanceOfType(result, typeof(ViewResult), "Result type should be ViewResult");
            result = controller.Edit(null);
            Assert.IsInstanceOfType(result, typeof(HttpStatusCodeResult), "Result type should be HttpStatusCodeResult when id is null.");

            result = controller.Edit(-1);
            Assert.IsInstanceOfType(result, typeof(HttpNotFoundResult), "Result type should be HttpNotFoundResult when id does not exist.");

        }

        [TestMethod]
        public void DeleteTest()
        {
            ActionResult result = controller.Delete(controller.Items.ElementAt(0).Id);
            Assert.IsInstanceOfType(result, typeof(RedirectToRouteResult), "Result type should be RedirectToRouteResult");
            Assert.AreEqual(((RedirectToRouteResult)result).RouteValues.ElementAt(0).Value, "Index", "Route value should be Index");
            result = controller.Delete(null);
            Assert.IsInstanceOfType(result, typeof(HttpStatusCodeResult), "Result type should be HttpStatusCodeResult when id is null.");
        }

        private void IndexTest()
        {
            string sortOrder = testContextInstance.Properties.Contains("sortOrder") ? testContextInstance.Properties["sortOrder"].ToString() : null;
            string currentFilter = testContextInstance.Properties.Contains("currentFilter") ? testContextInstance.Properties["currentFilter"].ToString() : null;
            string searchString = testContextInstance.Properties.Contains("searchString") ? testContextInstance.Properties["searchString"].ToString() : null;
            int? page;
            int page1;
            if (!testContextInstance.Properties.Contains("page") || !int.TryParse(testContextInstance.Properties["page"].ToString(), out page1))
            {
                page = null;
            }
            else
            {
                page = page1;
            }

            ViewResult result = controller.Index(sortOrder, currentFilter, searchString, page);

            Assert.IsInstanceOfType(result.Model, typeof(PagedList.PagedList<TestProject.Models.Item>));
                        PagedList.PagedList<TestProject.Models.Item> model = (PagedList.PagedList<TestProject.Models.Item>)result.Model;
            Assert.AreEqual(model.PageSize, 3, "The page size should be 3");
            
            if (sortOrder != null)
            {
                var controllerItems = ((PagedList.PagedList<TestProject.Models.Item>)result.ViewData.Model);
                //var controllerItems = result.ViewData.Values.OfType<Models.Item>().ToList();
                Assert.AreEqual(controllerItems.Count, 2, "Should be 2 items.");
                if (sortOrder == "name_desc")
                {
                    Assert.AreEqual(controllerItems[0].Name, "test2", "Item name should be test2.");
                    Assert.AreEqual(controllerItems[1].Name, "test1", "Item name should be test1.");
                }
                else if (sortOrder == "Value")
                {
                    Assert.AreEqual(controllerItems[0].Value, 1, "Item value should be 1.");
                    Assert.AreEqual(controllerItems[1].Value, 2, "Item value should be 2.");
                }
                else if (sortOrder == "value_desc")
                {
                    Assert.AreEqual(controllerItems[0].Value, 2, "Item value should be 2.");
                    Assert.AreEqual(controllerItems[1].Value, 1, "Item value should be 1.");
                }
                else
                {
                    Assert.AreEqual(controllerItems[0].Name, "test1", "Item name should be test1.");
                    Assert.AreEqual(controllerItems[1].Name, "test2", "Item name should be test2.");
                }

            }

            if (searchString != null)
            {
                Assert.AreEqual(model.PageNumber, 1, string.Format("The page should be {0}", page ?? 1));
            }
            else
            {
                Assert.AreEqual(model.PageNumber, page ?? 1, string.Format("The page should be {0}", page ?? 1));
            }

            

        }

        private void Create()
        {
            Models.Item item = new Models.Item()
            {
                Name = "test2",
                Value = 2,
            };

            controller.Create(item);

            Models.Item item2 = new Models.Item()
            {
                Name = "test1",
                Value = 1,
            };

            controller.Create(item2);
        }

        private void DeleteAll()
        {
            foreach (var item in controller.Items.Select(p => p.Id))
            {
                controller.Delete(item);
            }
        }


    }
}
