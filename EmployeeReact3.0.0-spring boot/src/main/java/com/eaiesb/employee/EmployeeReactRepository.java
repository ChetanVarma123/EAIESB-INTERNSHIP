package com.eaiesb.employee;

import org.springframework.data.mongodb.repository.ReactiveMongoRepository;

public interface EmployeeReactRepository extends ReactiveMongoRepository<EmployeeReact, String>{

}
