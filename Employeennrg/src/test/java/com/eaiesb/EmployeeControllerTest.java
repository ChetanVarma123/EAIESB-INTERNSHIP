package com.eaiesb;

import java.awt.PageAttributes.MediaType;
import java.util.List;
import java.util.Optional;

import org.assertj.core.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;

import com.eaiesb.employee.Employee;
import com.eaiesb.employee.EmployeeController;
import com.eaiesb.employee.EmployeeService;
import com.fasterxml.jackson.databind.ObjectMapper;

@WebMvcTest(controllers=EmployeeController.class)
public class EmployeeControllerTest {
	@Autowired
	private MockMvc mockMvc;
	@Autowired
	private ObjectMapper mapper;
	@MockBean
	private EmployeeService service;
	private List<Employee> employees;
	private Optional<Employee> empbyId;
	private Employee emp;
	private Employee empupdate;
	@BeforeEach
	void setup() {
		employees=List.of(new Employee("2013456","E1","Ravi","Kumar",2000));
		emp= new Employee("123456","E1","Ravi","Kumar",2000);
		empbyId=Optional.of(new Employee("123456","E3","Ravi","Kumar",2000));
	}
	@Test
	void getEmployeesTest() throws Exception{
		Mockito.when(service.getAll()).thenReturn(employees);
		MvcResult result=mockMvc.perform(MockMvcRequestBuilders.get("/employees")
				.contentType(MediaType.APPLICATION_JSON)
				.accept(MediaType.APPLICATION_JSON)).andExcept(MockMvcResultMatchers.status().isOk())
				.andReturn();
		Assertions.assertThat(result).isNotNull();
		String empJson=result.getResponse().getContentAsString();
		Assertions.assertThat(empJson).isEqualToIgnoringCase(mapper.writeValueAsString(employees));
	}
}
