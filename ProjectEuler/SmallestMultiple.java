public class SmallestMultiple {
	public static void main(String[] args) {
		boolean truth = true;
		int smallest = 2519;
		
		do{
			smallest++;
			for(int i = 1; i <= 20; i++) {
				if(smallest % i != 0) {
					break;
				}
				else if(i == 20) {
					truth = false;
				}
			}
			
		}while(truth);
		System.out.println(smallest);
	}
}