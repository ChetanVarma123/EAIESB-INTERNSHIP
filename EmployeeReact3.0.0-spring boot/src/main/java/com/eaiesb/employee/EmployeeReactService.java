package com.eaiesb.employee;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
public class EmployeeReactService {
	@Autowired
	public EmployeeReactRepository empRepo;
	public Mono<EmployeeReact> create(EmployeeReact emp){
		return empRepo.save(emp);
	}
	public Flux<EmployeeReact> getAll(){
		return empRepo.findAll();
	}
	public Mono<EmployeeReact> getById(String id){
		return empRepo.findById(id);
	}
	public Mono<EmployeeReact> update(String id, EmployeeReact emp){
		emp.setId(id);
		return empRepo.save(emp);
	}
	public Mono<Void> delete(String id){
		return empRepo.deleteById(id);
	}
}
