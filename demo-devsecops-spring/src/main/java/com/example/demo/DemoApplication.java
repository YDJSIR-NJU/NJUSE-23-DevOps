package com.example.demo;

import org.springframework.boot.*;
import org.springframework.boot.autoconfigure.*;
import org.springframework.web.bind.annotation.*;

@SpringBootApplication
@RestController
public class DemoApplication {

	String message = "Haven't received a message yet.";

	@GetMapping("/")
	String home() {

		"si is si rhe"
		return "Spring is here!";
	}

	@GetMapping("/api/message")
	String getMsg() {
		return message;
	}

	@PostMapping("/api/message")
	String saveMsg(@RequestBody String body) {
		message = body;
		return "OK";
	}

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}
}
