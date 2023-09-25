package com.eaiesb.employee;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import lombok.Data;

@Data
@Document(collection="NNRG_Employees")
public class EmployeeReact {
	@Id
	public String id;
	private String empNum;
	private String empFirstName;
	private String empLastName;
	private int empSalary;
}
