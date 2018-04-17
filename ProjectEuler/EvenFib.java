import java.util.ArrayList;
public class EvenFib {

	public static void main (String[] args) {
		int fibOne = 1;
		int fibTwo = 2;
		int fibSum = 0;
		int evenSum = 0;
		ArrayList<Integer> terms = new ArrayList<>();
		 do{
			fibSum = fibOne + fibTwo;
			if(fibSum > 4000000)
				break;
			fibOne = fibTwo;
			fibTwo = fibSum;
			if(fibSum % 2 == 0)
				evenSum += fibSum;
			
			System.out.println(fibSum);
		}while(fibSum < 3999999);
		System.out.println(evenSum);
	}
	
}