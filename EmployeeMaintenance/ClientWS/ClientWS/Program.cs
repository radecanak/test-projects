using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace ClientWS
{
    public class Person
    {
        public int person_id
        {
            get;set;
        }

        public string last_name
        {
            get; set;
        }

        public string first_name
        {
            get; set;
        }

        public string birth_date
        {
            get; set;
        }

        public override string ToString()
        {
            return $"PersonID: {person_id}, FirstName: {first_name}, LastName: {last_name}, BirthDate: {birth_date}";
        }

    }

    public class Employee
    {
        public int employee_id
        {
            get; set;
        }

        public int person_id
        {
            get; set;
        }

        public int employee_num
        {
            get; set;
        }

        public string employed_date
        {
            get; set;
        }

        public string terminated_date
        {
            get; set;
        }


        public override string ToString()
        {
            return $"EmployeeID: {employee_id}, PersonID: {person_id}, EmployeeNum: {employee_num}, EmployedDate: {employed_date}, TerminatedDate: {terminated_date}";
        }

    }

    class Program
    {
        static HttpClient client = new HttpClient();

        static void Main(string[] args)
        {
            RunAsync().Wait();
        }
        
        static async Task<Person> GetPersonAsync(int personId)
        {
            HttpResponseMessage response = await client.GetAsync($"api/person/{personId}");
            response.EnsureSuccessStatusCode();
            HttpContent requestContent = response.Content;
            string jsonContent = requestContent.ReadAsStringAsync().Result;
            Person person = JsonConvert.DeserializeObject<Person>(jsonContent);
            Console.WriteLine($"Person details: {person}");
            return person;
        }

        static async Task<Person> DeletePersonAsync(int personId)
        {
            HttpResponseMessage response = await client.DeleteAsync($"api/person/{personId}");
            response.EnsureSuccessStatusCode();
            HttpContent requestContent = response.Content;
            string jsonContent = requestContent.ReadAsStringAsync().Result;
            Person person = JsonConvert.DeserializeObject<Person>(jsonContent);
            Console.WriteLine($"Person with ID {personId} deleted");
            return person;
        }

        static async Task<Person> AddPersonAsync(string firstName, string lastName, string birthDate)
        {
            return await SetPersonAsync(0, firstName, lastName, birthDate);
        }

        static async Task<Person> UpdatePersonAsync(Person person)
        {
            return await SetPersonAsync(person.person_id, person.first_name, person.last_name, person.birth_date);
        }

        static async Task<Person> SetPersonAsync(int personId, string firstName, string lastName, string birthDate)
        {
            var formContent = new FormUrlEncodedContent(new[]
            {
                new KeyValuePair<string, string>("person_id", personId.ToString()),
                new KeyValuePair<string, string>("last_name", firstName),
                new KeyValuePair<string, string>("last_name", firstName),
                new KeyValuePair<string, string>("first_name", lastName),
                new KeyValuePair<string, string>("birth_date", birthDate)
            });
            HttpResponseMessage response;
            if (personId != 0)
                response = await client.PostAsync("api/person", formContent);
            else
                response = await client.PutAsync("api/person", formContent);
            response.EnsureSuccessStatusCode();
            HttpContent requestContent = response.Content;
            string jsonContent = requestContent.ReadAsStringAsync().Result;
            Person person = JsonConvert.DeserializeObject<Person>(jsonContent);
            if (personId == 0)
                Console.WriteLine($"Person {person.first_name},  {person.last_name} added.");
            else
                Console.WriteLine($"Person {person.first_name},  {person.last_name} updated.");
            return person;
        }

        static async Task<Employee> GetEmployeeAsync(int employeeId)
        {
            HttpResponseMessage response = await client.GetAsync($"api/employee/{employeeId}");
            response.EnsureSuccessStatusCode();
            HttpContent requestContent = response.Content;
            string jsonContent = requestContent.ReadAsStringAsync().Result;
            Employee employee = JsonConvert.DeserializeObject<Employee>(jsonContent);
            Console.WriteLine($"Employee details: {employee}");
            return employee;
        }

        static async Task<Employee> AddEmployeeAsync(int person_id, int employee_num, string employed_date, string terminated_date)
        {
            return await SetEmployeeAsync(0, person_id, employee_num, employed_date, terminated_date);
        }

        static async Task<Employee> UpdateEmployeeAsync(Employee employee)
        {
            return await SetEmployeeAsync(employee.employee_id, employee.person_id, employee.employee_num, employee.employed_date, employee.terminated_date);
        }

        static async Task<Employee> SetEmployeeAsync(int employee_id, int person_id, int employee_num, string employed_date, string terminated_date)
        {
            var formContent = new FormUrlEncodedContent(new[]
            {
                new KeyValuePair<string, string>("employee_id", employee_id.ToString()),
                new KeyValuePair<string, string>("person_id", person_id.ToString()),
                new KeyValuePair<string, string>("employee_num", employee_num.ToString()),
                new KeyValuePair<string, string>("employed_date", employed_date),
                new KeyValuePair<string, string>("terminated_date", terminated_date),
            });
            HttpResponseMessage response;
            if (employee_id != 0)
                response = await client.PostAsync("api/employee", formContent);
            else
                response = await client.PutAsync("api/employee", formContent);
            response.EnsureSuccessStatusCode();
            HttpContent requestContent = response.Content;
            string jsonContent = requestContent.ReadAsStringAsync().Result;
            Employee employee = JsonConvert.DeserializeObject<Employee>(jsonContent);
            if (employee_id == 0)
                Console.WriteLine($"Employed added.");
            else
                Console.WriteLine($"Employed updated.");
            return employee;
        }

        static async Task<Employee> DeleteEmployeeAsync(int employeeId)
        {
            HttpResponseMessage response = await client.DeleteAsync($"api/employee/{employeeId}");
            response.EnsureSuccessStatusCode();
            HttpContent requestContent = response.Content;
            string jsonContent = requestContent.ReadAsStringAsync().Result;
            Employee employee = JsonConvert.DeserializeObject<Employee>(jsonContent);
            Console.WriteLine($"Employee with ID {employeeId} deleted");
            return employee;
        }

        static async Task RunAsync()
        {
            client.BaseAddress = new Uri("http://127.0.0.1:5000/");
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            try
            {
                string firstName = "test first name";
                string lastName = "test last name";
                var person = await AddPersonAsync(firstName, lastName, "1982-04-26");
                person = await GetPersonAsync(person.person_id);
                person.first_name = "test first name 2";
                person.last_name = "test last name 2";
                person.birth_date = "1982-06-26";
                person = await UpdatePersonAsync(person);
                person = await GetPersonAsync(person.person_id);

                var employee1 = await AddEmployeeAsync(person.person_id, 1, "2016-04-26", "2017-04-26");
                employee1 = await GetEmployeeAsync(employee1.employee_id);
                employee1.terminated_date = "2017-04-28";
                await UpdateEmployeeAsync(employee1);
                await GetEmployeeAsync(employee1.employee_id);

                var employee2 = await AddEmployeeAsync(person.person_id, 2, "2013-04-26", "2013-04-26");
                employee2 = await GetEmployeeAsync(employee2.employee_id);
                employee2.terminated_date = "2017-02-28";
                await UpdateEmployeeAsync(employee2);
                await GetEmployeeAsync(employee2.employee_id);

                await DeleteEmployeeAsync(employee2.employee_id);
                try
                {
                    await GetEmployeeAsync(employee2.employee_id);
                    throw new Exception($"Employee with id {employee2.employee_id} still exists.");
                }
                catch
                {
                }

                await GetEmployeeAsync(employee1.employee_id);
                await DeletePersonAsync(person.person_id);
                try
                {
                    await GetEmployeeAsync(employee1.employee_id);
                    throw new Exception($"Employee with id {employee2.employee_id} still exists.");
                }
                catch
                {
                }

                try
                {
                    await GetPersonAsync(person.person_id);
                    throw new Exception($"Person with id {person.person_id} still exists.");
                }
                catch
                {
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }

            Console.ReadLine();
        }
    }
}
