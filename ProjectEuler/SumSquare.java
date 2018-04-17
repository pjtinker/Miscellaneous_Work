import java.lang.Math;
public class SumSquare {
	public static void main(String[] args) {
		int sum = 0;
		double squareSum = 0;
		
		for(int i = 1; i <= 100; i++) {
			sum += i;
			squareSum += Math.pow((double)i, 2);
		}
		System.out.println(Math.pow((double)sum, 2) - squareSum);
	}
}