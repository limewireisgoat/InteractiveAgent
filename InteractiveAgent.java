import java.util.Scanner;

public class InteractiveAgent {
	
	static Scanner in = new Scanner(System.in);
	static String response;
	static boolean end_conversation = false;
	
	public static void main(String[] args) {
		
		printGreetings();
		while(!end_conversation) {
			getResponse();
			to_Leave();
		}
	}
	
	private static void to_Leave() {
		// TODO Auto-generated method stub
		if (response.contains("bye")) {
			end_conversation = true;
			printFarewell();
		}else
			respond();
	}

	private static void respond() {
		// TODO Auto-generated method stub
		System.out.println("xyz");
	}

	private static void printFarewell() {
		// TODO Auto-generated method stub
		System.out.println(pickFarewell());
	}

	private static String pickFarewell() {
		// TODO Auto-generated method stub
		String [] arr = {"Bye", "See you later"};
		return getString(arr);
	}

	private static void getResponse() {
		// TODO Auto-generated method stub
		response= in.nextLine();
	}

	public static void printGreetings() {
		System.out.println(pickGreetings());
	}

	private static String pickGreetings() {
		// TODO Auto-generated method stub
		String [] arr = {"Hi", "What's up?"};
		return getString(arr);
	}

	private static String getString(String[] arr) {
		// TODO Auto-generated method stub
		int length = arr.length;
		int random_value = (int)(Math.random() * length);
		return arr[random_value];
	}

}
