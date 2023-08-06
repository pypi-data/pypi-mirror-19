package com.atlassian;

import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(LocalstackTestRunner.class)
public class TestRunnerTest {

	@Test
	public void test1() {
		System.out.println("test method 1");
	}

	@Test
	public void test2() {
		System.out.println("test method 2");
	}

}
