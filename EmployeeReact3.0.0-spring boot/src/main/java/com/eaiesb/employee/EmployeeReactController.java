package com.eaiesb.employee;


import java.time.Duration;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
public class EmployeeReactController {
	@Autowired
	public EmployeeReactService service;
	
	@PostMapping("/employee")
	public Mono<EmployeeReact> createEmployee(@Validated @RequestBody EmployeeReact emp){
		return service.create(emp);
	}
	
	@GetMapping(value="/employees", produces=MediaType.TEXT_EVENT_STREAM_VALUE)
	public Flux<EmployeeReact> getAllEmployees(){
		return (Flux<EmployeeReact>) service.getAll().delayElements(Duration.ofSeconds(2));
	}
	
	@GetMapping("/employee/{id}")
	public Mono<EmployeeReact> getEmployee(@PathVariable String id){
		return service.getById(id);
	}
	
	@PutMapping("/employee/{id}")
	public Mono<EmployeeReact> updateEmployee(@PathVariable String id, @Validated @RequestBody EmployeeReact emp){
		return service.update(id, emp);
	}
	
	@DeleteMapping("/employee/{id}")
	public Mono<Void> deleteEmployee(@PathVariable String id){ 
		return service.delete(id);
	}
}
