package com.atlassian;

import java.io.IOException;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;

import org.junit.runner.notification.RunNotifier;
import org.junit.runners.BlockJUnit4ClassRunner;
import org.junit.runners.model.InitializationError;

public class LocalstackTestRunner extends BlockJUnit4ClassRunner {

	private static final AtomicReference<Process> INFRA_STARTED = new AtomicReference<Process>();

	public LocalstackTestRunner(Class<?> klass) throws InitializationError {
		super(klass);
		System.out.println("create test runner");
	}

	@Override
	public void run(RunNotifier notifier) {
		System.out.println("run");
		setupInfrastructure();
		super.run(notifier);
		System.out.println("done");
		teardownInfrastructure();
	}

	private void setupInfrastructure() {
		synchronized (INFRA_STARTED) {
			if(INFRA_STARTED.get() != null) return;
			String cmd = "make infra";
			Process proc;
			try {
				proc = Runtime.getRuntime().exec(new String[]{"bash", "-c", cmd});
				INFRA_STARTED.set(proc);
			} catch (IOException e) {
				throw new RuntimeException(e);
			}
		}
	}

	private void teardownInfrastructure() {
		Process proc = INFRA_STARTED.get();
		if(proc == null) {
			return;
		}
		proc.destroy();
	}
}
